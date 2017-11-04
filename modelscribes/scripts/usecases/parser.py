# coding=utf-8


#FIXME: Check if line patterns are too permissive at the end

from __future__ import unicode_literals, print_function, absolute_import, division
from typing import Text
import re

from modelscribes.base.symbols import (
    Symbol
)

from modelscribes.megamodels.sources import ModelSourceFile

from modelscribes.scripts.megamodels.parser import (
    isMegamodelStatement
)
from modelscribes.scripts.usecases.printer import (
    UsecaseModelPrinter
)
from modelscribes.base.issues import (
    Issue,
    LocalizedIssue,
    Levels,
    FatalError,
)
from modelscribes.metamodels.usecases import (
    UsecaseModel,
    System,
    Actor,
    Usecase,
    METAMODEL
)


__all__=(
    'UsecaseModelSource'
)
DEBUG=0


class UsecaseModelSource(ModelSourceFile):
    def __init__(self, usecaseFileName):
        #type: (Text) -> None
        super(UsecaseModelSource, self).__init__(
            fileName=usecaseFileName,
        )


    @property
    def usecaseModel(self):
        #type: () -> UsecaseModel
        m=self.model #type: UsecaseModel
        return m


    @property
    def metamodel(self):
        return METAMODEL

    def parseToFillModel(self):

        def _checkSystemExist(isLast=False):
            if self.usecaseModel.system is None:
                LocalizedIssue(
                    sourceFile=self,
                    level=Levels.Fatal,
                    message='System is not defined %s' %
                            (' yet.' if not isLast else '!'),
                    line=line_no,
                )

        def _ensureActor(name):
            _checkSystemExist(isLast=False)
            if name in self.usecaseModel.actorNamed:
                return self.usecaseModel.actorNamed[name]
            else:
                return Actor(self.usecaseModel, name)

        def _ensureUsecase(name):
            _checkSystemExist(isLast=False)
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
            r = '^ *-- *[^@].*$'
            m = re.match(r, line)
            if m:
                continue
            # TODO: add proper comment management

            #--- megamodel statements -------------
            is_mms=isMegamodelStatement(
                lineNo=line_no,
                modelSourceFile=self)
            if is_mms:
                # megamodel statements have already been
                # parse so silently ignore them
                continue


            #--- system X -------------------------
            r = begin(0)+r'system +(?P<name>\w+)'+end
            m = re.match(r, line)
            if m:
                if self.usecaseModel.system is not None:
                    LocalizedIssue(
                        sourceFile=self,
                        level=Levels.Warning,
                        message='System defined twice',
                        line=line_no,
                    )
                name=m.group('name')
                System(
                    usecaseModel=self.usecaseModel,
                    name=name,
                    lineNo=line_no,
                )
                if not Symbol.is_CamlCase(name):
                    LocalizedIssue(
                        sourceFile=self,
                        level=Levels.Warning,
                        message=(
                            '"%s" should be in CamlCase.'
                            % name),
                        line=line_no
                    )
                continue

            #--- actor X --------------------------
            r = begin(0)+r'(?P<kind>(human|system))? *actor +(?P<name>\w+)'+end
            m = re.match(r, line)
            if m:
                current_usecase=None
                name=m.group('name')
                current_actor=_ensureActor(name)
                current_actor.kind=m.group('kind'),
                current_actor.lineNo=line_no
                current_section='actor'
                if not Symbol.is_CamlCase(name):
                    LocalizedIssue(
                        sourceFile=self,
                        level=Levels.Warning,
                        message=(
                            '"%s" should be in CamlCase.'
                            % name),
                        line=line_no
                    )
                continue

            #--- usecase X --------------------------
            r = begin(0)+r'usecase +(?P<name>\w+)'+end
            m = re.match(r, line)
            if m:
                name=m.group('name')
                current_usecase=_ensureUsecase(name)
                current_usecase.lineNo = line_no
                current_section='usecase'
                if not Symbol.is_CamlCase(name):
                    LocalizedIssue(
                        sourceFile=self,
                        level=Levels.Warning,
                        message=(
                            '"%s" should be in CamlCase.'
                            % name),
                        line=line_no
                    )
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


            LocalizedIssue(
                sourceFile=self,
                level=Levels.Error,
                message=(
                    'Syntax error. Line ignored.'),
                line=line_no
            )

        # End of file
        line_no=len(self.sourceLines)
        _checkSystemExist(isLast=True)

    # def printStatus(self):
    #     """
    #     Print the status of the file:
    #
    #     * the list of errors if the file is invalid,
    #     * a short summary of entities (classes, attributes, etc.) otherwise
    #     """
    #
    #     if self.isValid:
    #         p=UsecaseModelPrinter(self.usecaseModel, displayLineNos=True)
    #         print(p.do())
    #     else:
    #         print('%s error(s) in the usecase model' % len(self.issueBox))
    #         for e in self.issueBox:
    #             print(e)

METAMODEL.registerSource(UsecaseModelSource)
