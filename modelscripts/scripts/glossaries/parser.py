# coding=utf-8
from __future__ import unicode_literals, print_function, absolute_import, division
from typing import Text, Union, Optional, Dict, List
import os
import io
import re

from modelscripts.sources.sources import (
    ModelSourceFile,
)
from modelscripts.sources.issues import (
    Issue,
    Level,
)

from modelscripts.metamodels.glossaries import (
    GlossaryModel,
    Domain,
    Entry,
)
from modelscripts.metamodels.texts import (
    TextBlock,
    Line,
)
from modelscripts.scripts.texts.parser import TextSourceFragment


DEBUG=0

class GlossaryModelSource(ModelSourceFile):
    def __init__(self, glossaryFileName):
        #type: (Text) -> None

        super(GlossaryModelSource, self).__init__(
            fileName=glossaryFileName)

        self.glossaryModel = None

        self.__descriptionLinesPerEntry={}
        #type: Optional[Dict[Entry, List[Text]]]
        #Just used to store during first step parsing the
        #lines that make the description of the entry.
        #This will be used later as the source of the
        #embedded parser for text. This filed will be set
        #to None just after.
        self.__descriptionFirstLinePerEntry={}
        #type: Optional[Dict[Entry, List[Text]]]

        self._parse()

    @property
    def model(self):
        return self.glossaryModel

    @property
    def usedModelByKind(self):
        _={}
        return _

    def _parse(self):
        self._parse_main_body()
        if self.glossaryModel and self.isValid:
            self._parse_and_resolve_descriptions()


    def _parse_main_body(self):
        """
        Parse everything in the glossary except the description
        of entries are parsed by the subparser for TextBlock
        In this first phase we just store the information as lines
        (and first line number). This info will be used in second
        phase to feed the embedded parser.
        """

        current_context=None
        #type: Optional[Union[GlossaryModel, Domain, Entry]]

        for (line_index, line) in enumerate(self.sourceLines):
            original_line = line
            line = line.replace(u'\t',u' ')
            line_no = line_index+1

            r = '^ *--.*$'
            m=re.match(r, line)
            if m:
                continue

            r = '^ *$'
            m=re.match(r, line)
            if m:
                continue

            if current_context is None:
                r = '^glossary +model *$'
                m=re.match(r, line)
                if m:
                    self.glossaryModel=GlossaryModel(
                        lineNo=line_no,
                    )
                    current_context=self.glossaryModel
                    continue

            if (isinstance(current_context, (
                    GlossaryModel,
                    Domain,
                    Entry))):
                r=r'^domain +(?P<name>\w+) *$'
                m=re.match(r, line)
                if m:
                    domain=Domain(
                        glossaryModel=self.glossaryModel,
                        name=m.group('name'),
                        lineNo=line_no,
                    )
                    current_context=domain
                    continue

            if isinstance(current_context, (
                    Domain,
                    Entry)):
                r=r'^    (?P<word1>\w+)(?P<words> \w+[\w ]+)? *: *$'
                m = re.match(r, line, re.UNICODE)
                if m:
                    if m.group('words') is None:
                        words=[]
                    else:
                        words=[ w
                            for w in m.group('words').split(' ')
                            if w!='']
                    domain=(
                        current_context.domain
                        if isinstance(current_context, Entry)
                        else current_context)
                    entry=Entry(
                        domain=domain,
                        mainTerm=m.group('word1'),
                        alternativeTerms=words,
                        description=None,
                        lineNo=line_no,
                    )
                    self.__descriptionLinesPerEntry[entry]=[]
                    entry.description=TextBlock(
                        container=entry,
                        lineNo=line_no+1,
                        lines=[],
                    )
                    current_context=entry
                    continue

            if isinstance(current_context, Entry):
                r='^        (?P<line>.*)'
                m = re.match(r, line)
                if m:
                    entry=current_context

                    # store the line no if this the first line of descr
                    if entry not in self.__descriptionFirstLinePerEntry:
                        self.__descriptionFirstLinePerEntry[entry]=line_no

                    self.__descriptionLinesPerEntry[
                         entry].append(m.group('line'))
                    continue

            print('ERROR at line %i. Cannot parse this line:'%line_no)
            print('-> %s' % line)


    def _parse_and_resolve_descriptions(self):
        """
        For all entry in the glossary parse its description
        (with the proper line) and resolve the description with
        this glossary.
        """
        for domain in self.glossaryModel.domainNamed.values():
            for entry in domain.entryNamed.values():
                desctext='\n'.join(self.__descriptionLinesPerEntry[entry])
                print('=',len(desctext))
                lno=self.__descriptionFirstLinePerEntry[entry]
                textParser=TextSourceFragment(
                    string=desctext,
                    startLineNo=lno)
                if not textParser.isValid:
                    # TODO: check what should be done
                    raise ValueError('Error in parsing Text source')
                else:
                    entry.description=textParser.textBlock
                    self.glossaryModel.resolveTextBlock(entry.description)
        self.__descriptionFirstLinePerEntry={}





    def printStatus(self):
        """
        Print the status of the file:

        * the list of errors if the file is invalid,
        * a short summary of entities (classes, attributes, etc.) otherwise
        """

        if self.isValid:
            from  modelscripts.scripts.glossaries.printer import Printer
            p=Printer(
                glossaryModel=self.glossaryModel,
                displayLineNos=True)
            print(p.do())
        else:
            print('%s error(s) in the glossary model' % len(self.issues))
            for e in self.issues:
                print(e)