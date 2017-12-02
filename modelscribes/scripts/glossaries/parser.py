# coding=utf-8
from __future__ import unicode_literals, print_function, absolute_import, division
from typing import Text, Union, Optional, Dict, List
import re

from modelscribes.megamodels.sources import ModelSourceFile
from modelscribes.scripts.megamodels.parser import (
    isMegamodelStatement
)
from modelscribes.metamodels.glossaries import (
    GlossaryModel,
    Domain,
    Entry,
    METAMODEL,
)
from modelscribes.base.issues import (
    Issue,
    LocalizedSourceIssue,
    Levels,
    FatalError,
)
from modelscribes.metamodels.texts import (
    TextBlock,
)
from modelscribes.scripts.texts.parser import TextSourceFragment
from modelscribes.megamodels.metamodels import Metamodel

DEBUG=0

class GlossaryModelSource(ModelSourceFile):
    def __init__(self, glossaryFileName):
        #type: (Text) -> None

        self.__descriptionLinesPerEntry={}
        #type: Optional[Dict[Entry, List[Text]]]
        """
        Just used to store during the first step parsing the
        lines that make the description of the entry.
        This will be used later as the source of the
        embedded parser for text. This field will be set
        to None just after.
        """

        self.__descriptionFirstLinePerEntry={}
        #type: Optional[Dict[Entry, List[Text]]]

        super(GlossaryModelSource, self).__init__(
            fileName=glossaryFileName)

        #
        #
        # self.parseToFillModel()

    @property
    def metamodel(self):
        #type: () -> Metamodel
        return METAMODEL

    @property
    def glossaryModel(self):
        #type: () -> GlossaryModel
        m=self.model #type: GlossaryModel
        return m


    def parseToFillModel(self):
        self._parse_main_body()
        if self.glossaryModel and self.isValid:
            self._parse_and_resolve_descriptions()

    def _parse_main_body(self):
        """
        Parse everything in the glossary except the description
        of entries. These descriptions are parsed by the
        subparser for TextBlock.
        In this first phase we just store the information
        as lines (and first line number). This info will
        be used in second phase to feed the embedded parser.
        """

        current_context=self.glossaryModel
        #type: Optional[Union[GlossaryModel, Domain, Entry]]

        for (line_index, line) in enumerate(self.sourceLines):
            original_line = line
            line = line.replace(u'\t',u' ')
            line_no = line_index+1

            #-----------------------------------------------
            #  comments
            #-----------------------------------------------

            r = '^ *--.*$'
            m=re.match(r, line)
            if m:
                continue

            #-----------------------------------------------
            #  blank lines
            #-----------------------------------------------
            r = '^ *$'
            m=re.match(r, line)
            if m:
                continue


            #-----------------------------------------------
            #  megamodel statements
            #-----------------------------------------------
            is_mms = isMegamodelStatement(
                lineNo=line_no,
                modelSourceFile=self)
            if is_mms:
                # megamodel statements have already been
                # parse so silently ignore them
                continue


            #-----------------------------------------------
            #  domain
            #-----------------------------------------------
            if (isinstance(current_context, (
                    GlossaryModel,
                    Domain,
                    Entry))):
                r=r'^domain +(?P<name>\w+) *$'
                m=re.match(r, line)
                if m:
                    #FIXME: don't create a domain if defined before
                    domain=Domain(
                        glossaryModel=self.glossaryModel,
                        name=m.group('name'),
                        lineNo=line_no,
                    )
                    current_context=domain
                    continue


            #-----------------------------------------------
            #  domain
            #-----------------------------------------------
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
                    #FIXME: error if term already in domain
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

            #-----------------------------------------------
            #  description
            #-----------------------------------------------

            if isinstance(current_context, Entry):
                r='^        (?P<line>.*)'
                m = re.match(r, line)
                if m:
                    entry=current_context

                    # store the line number if this the first
                    # line of description
                    if entry not in self.__descriptionFirstLinePerEntry:
                        self.__descriptionFirstLinePerEntry[entry]=line_no

                    self.__descriptionLinesPerEntry[
                         entry].append(m.group('line'))
                    continue

            #-----------------------------------------------
            #  error
            #-----------------------------------------------

            LocalizedSourceIssue(
                sourceFile=self,
                level=Levels.Error,
                message='Syntax error',
                line=line_no
            )



    def _parse_and_resolve_descriptions(self):
        """
        For all entry in the glossary parse its description
        (with the proper line) and resolve the description with
        this glossary.
        """
        for domain in self.glossaryModel.domainNamed.values():
            for entry in domain.entryNamed.values():
                desctext='\n'.join(self.__descriptionLinesPerEntry[entry])
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


METAMODEL.registerSource(GlossaryModelSource)
