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
    LocalizedSourceIssue,
    Levels,
)
from modelscribes.metamodels.textblocks import (
    TextBlockModel,
)
from modelscribes.scripts.textblocks.parser import TextBlockSource
from modelscribes.megamodels.metamodels import Metamodel

DEBUG=0

class GlossaryModelSource(ModelSourceFile):
    def __init__(self, glossaryFileName):
        #type: (Text) -> None

        self.descriptionBlockSourcePerEntry={}
        #type:Dict[Entry, TextBlockSource]]


        # self.__descriptionLinesPerEntry={}
        # #type: Optional[Dict[Entry, List[Text]]]
        # """
        # Just used to store during the first step parsing the
        # lines that make the description of the entry.
        # This will be used later as the source of the
        # embedded parser for text. This field will be set
        # to None just after.
        # """
        #
        # self.__descriptionFirstLineNoPerEntry={}
        # #type: Optional[Dict[Entry, List[Text]]]

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
            self._parseDescriptions()

    def _parse_main_body(self):
        """
        Parse everything in the glossary except the description
        of entries. These descriptions are parsed by the
        subparser for TextBlockModel.
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
                    name=m.group('name')
                    if name in self.glossaryModel.domainNamed:
                        # If the domain already exists, reuse it
                        current_content=(
                            self.glossaryModel.domainNamed[name])
                    else:
                        # Creates a new domain with this name
                        domain=Domain(
                            glossaryModel=self.glossaryModel,
                            name=name,
                            lineNo=line_no,
                        )
                        current_context=domain
                    continue


            #-----------------------------------------------
            #  entry
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
                    name=m.group('word1')
                    if name in domain.entryNamed:
                        # The simplest way deal with the
                        # multiple definition is to concatenate
                        # text after existing definition. This
                        # avoid skipping the next lines.
                        LocalizedSourceIssue(
                            sourceFile=self,
                            level=Levels.Error,
                            message=
                                '%s.%s already exist.'
                                ' Definitions will be appended.' %
                                (domain.name, name),
                            line=line_no
                        )
                        # do not create an new entry
                        # reuse instead the old entry
                        entry=domain.entryNamed[name]
                    else:
                        # Create a new entry
                        entry=Entry(
                            domain=domain,
                            mainTerm=name,
                            alternativeTerms=words,
                            description=None,
                            lineNo=line_no,
                        )
                        # Create an empty text block for description
                        descr=TextBlockModel()
                        entry.description=descr
                        self.descriptionBlockSourcePerEntry[entry]=(
                            TextBlockSource())
                    current_context=entry
                    continue

            #-----------------------------------------------
            #  description
            #-----------------------------------------------

            if isinstance(current_context, Entry):
                r='^ *\|(?P<line>.*)'
                m = re.match(r, line)
                if m:
                    entry=current_context
                    self.descriptionBlockSourcePerEntry[entry] \
                            .addTextLine(
                                textLine=m.group('line'),
                                lineNo=line_no)
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



    def _parseDescriptions(self):
        """
        For all entry description in the glossary
        resolve the description with this glossary.
        """
        for domain in self.glossaryModel.domainNamed.values():
            for entry in domain.entryNamed.values():
                description_parser= (
                    self.descriptionBlockSourcePerEntry[entry])
                # lno=self.__descriptionFirstLineNoPerEntry[entry]
                description_parser.parseToFillModel(
                    container=entry,
                    glossary=self.model
                )
                if not description_parser.isValid:
                    # TODO: check what should be done
                    raise ValueError('Error in parsing Text source')
                else:
                    entry.description=description_parser.model



        # self.__descriptionFirstLineNoPerEntry={}


METAMODEL.registerSource(GlossaryModelSource)
