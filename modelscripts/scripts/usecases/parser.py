# coding=utf-8
from __future__ import unicode_literals, print_function, absolute_import, division
from typing import Text
import os
import re



from modelscripts.source.sources import SourceFile
from modelscripts.scripts.usecases.printer import (
    Printer
)

from modelscripts.metamodels.usecases import (
    UsecaseModel,
    System,
    Actor,
    Usecase,
)
DEBUG=0

class UsecaseModelSource(SourceFile):
    def __init__(self, usecaseFileName):
        #type: (Text) -> None
        super(UsecaseModelSource, self).__init__()
        if not os.path.isfile(usecaseFileName):
            raise Exception('File "%s" not found' % usecaseFileName)
        self.fileName = usecaseFileName
        self.sourceLines = (
            line.rstrip()
            for line in open(self.fileName, 'rU'))
        self.directory = os.path.dirname(usecaseFileName)
        self.isValid = None
        self.errors = []
        self.lines = None
        self.ignoredLines = []
        self.usecaseModel = UsecaseModel(source=self)
        self._parse()
        self.isValid=True # Todo, check errors, etc.

    def _parse(self):

        def _ensureActor(name):
            if name in self.usecaseModel.actorNamed:
                return self.usecaseModel.actorNamed[name]
            else:
                return Actor(self.usecaseModel, name)

        def _ensureUsecase(name):
            if name in self.usecaseModel.system.usecaseNamed:
                return self.usecaseModel.system.usecaseNamed[name]
            else:
                return Usecase(self.usecaseModel.system, name)

        def begin(n): return '^'+'    '*n
        end = ' *$'

        if DEBUG>=1:
            print('\nParsing %s\n' % self.fileName)

        current_actor=None
        current_usecase=None
        current_section=None

        for (line_index, line) in enumerate(self.sourceLines):
            original_line = line
            # replace tabs by spaces
            line = line.replace('\t',' ')
            line_no = line_index+1

            if DEBUG>=2:
                print ('#%i : %s' % (line_no, original_line))

            #---- blank lines ---------------------------------------------
            r = '^ *$'
            m = re.match(r, line)
            if m:
                continue

            #---- comments -------------------------------------------------
            r = '^ *--.*$'
            m = re.match(r, line)
            if m:
                continue

            #--- system X -------------------------
            r = begin(0)+r'system +(?P<name>\w+)'+end
            m = re.match(r, line)
            if m:
                if self.usecaseModel.system is not None:
                    raise SyntaxError(
                        'Error at line #%i: system defined twice'
                        % line_no
                    )
                System(
                    usecaseModel=self.usecaseModel,
                    name=m.group('name'),
                    lineNo=line_no,
                )

                continue

            #--- actor X --------------------------
            r = begin(0)+r'(?P<kind>(human|system))? *actor +(?P<name>\w+)'+end
            m = re.match(r, line)
            if m:
                current_usecase=None
                if self.usecaseModel.system is None:
                    raise SyntaxError(
                        'Error at line #%i: system not defined'
                        % line_no
                    )
                n=m.group('name')
                current_actor=_ensureActor(n)
                current_actor.kind=m.group('kind'),
                current_actor.lineNo=line_no
                current_section='actor'
                continue

            #--- usecase X --------------------------
            r = begin(0)+r'usecase +(?P<name>\w+)'+end
            m = re.match(r, line)
            if m:
                current_actor=None
                if self.usecaseModel.system is None:
                    raise SyntaxError(
                        'Error at line #%i: system not defined'
                        % line_no
                    )
                n=m.group('name')
                current_usecase=_ensureUsecase(n)
                current_usecase.lineNo = line_no
                current_section='usecase'
                continue

            if current_actor:

                # --- ....usecases ------------------------
                r = begin(1)+r'usecases'+end
                m = re.match(r, line)
                if m:
                    current_section='actor.usecases'
                    continue

                if current_section=='actor.usecases':
                    r = begin(2)+r'(?P<name>\w+)'+end
                    m = re.match(r, line)
                    if m:
                        uc=_ensureUsecase(m.group('name'))
                        current_actor.addUsecase(uc)
                        uc.lineNo=line_no
                    continue

            raise SyntaxError(
                'Error at line #%i: syntax error'
                % line_no
            )

        if self.usecaseModel.system is None:
            raise SyntaxError(
                'Error: no system defined'
            )

    def printStatus(self):
        """
        Print the status of the file:

        * the list of errors if the file is invalid,
        * a short summary of entities (classes, attributes, etc.) otherwise
        """

        if self.isValid:
            p=Printer(self.usecaseModel, displayLineNos=True)
            print(p.do())
        else:
            print('%s error(s) in the usecase model'  % len(self.errors))
            for e in self.errors:
                print(e)