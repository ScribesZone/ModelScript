# coding=utf-8

"""
Glossary metamodel.

    GlossaryModel
    <>--* Domain
          <>--* Entry
"""
from __future__ import print_function

import collections

from typing import Dict, Text, Optional, List

from modelscribes.metamodels.texts import (
    TextBlock,
    Reference,

)
from modelscribes.megamodels import Model, Metamodel
from modelscribes.base.sources import SourceElement


class GlossaryModel(Model):

    def __init__(self, source=None, lineNo=None):
        super(GlossaryModel, self).__init__(
            source=source,
            name=None,
            lineNo=lineNo
        )
        self.domainNamed=collections.OrderedDict()
        # type: Dict[Text, Domain]

    @property
    def metamodel(self):
        return metamodel

    def findEntry(self, term):
        #type: (Text) -> Optional[Entry]

        # search first in the main terms
        for domain in self.domainNamed.values():
            if term in domain.entryNamed:
                return domain.entryNamed[term]

        # search then in alternatives terms
        for domain in self.domainNamed.values():
            for entry in domain.entryNamed.values():
                if term in entry.alternativeTerms:
                    return entry

        return None


    def resolveTextBlock(self, textBlock):
        for line in textBlock.lines:
            for token in line.tokens:
                if isinstance(token, Reference):
                    reference=token
                    reference.resolve(self)




class Domain(SourceElement):

    def __init__(self, glossaryModel, name, lineNo=None):
        super(Domain, self).__init__(
            name=name,
            lineNo=lineNo
        )
        self.glossaryModel=glossaryModel
        self.glossaryModel.domainNamed[name]=self
        self.entryNamed=collections.OrderedDict()
        # type: Dict[Text, Entry]
        # Entries indexed y main term name


class Entry(SourceElement):

    def __init__(self,
                 domain,
                 mainTerm,
                 alternativeTerms=(),
                 description=None,
                 lineNo=None):
        super(Entry, self).__init__(
            name=None,
            lineNo=lineNo
        )
        # TODO: check, unique main/alternative(?) term
        self.domain=domain
        #type: Domain

        self.domain.entryNamed[mainTerm]=self

        self.mainTerm=mainTerm
        #type: Text

        self.alternativeTerms=list(alternativeTerms)
        #type: List[Text]

        self.description=description
        #type: Optional[TextBlock]

        self.references=[]
        #type: List[Reference]

metamodel = Metamodel(
    id='gl',
    label='glossary',
    extension='.glm',
    modelClass=GlossaryModel
)