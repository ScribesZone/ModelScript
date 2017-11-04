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
from modelscribes.megamodels.metamodels import Metamodel
from modelscribes.megamodels.models import Model
from modelscribes.base.sources import SourceElement
from modelscribes.megamodels.dependencies.metamodels import (
    MetamodelDependency
)

class GlossaryModel(Model):
    """
    Collection of named domains.
    """

    def __init__(self):
        super(GlossaryModel, self).__init__()

        self.domainNamed=collections.OrderedDict()
        # type: Dict[Text, Domain]

    @property
    def metamodel(self):
        #type: () -> Metamodel
        return METAMODEL


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
    """
    A collection of entry indexed by the main term.
    """


    def __init__(self, glossaryModel, name, lineNo=None):
        super(Domain, self).__init__(
            name=name,
            lineNo=lineNo
        )
        self.glossaryModel=glossaryModel
        self.glossaryModel.domainNamed[name]=self
        self.entryNamed=collections.OrderedDict()
        # type: Dict[Text, Entry]
        # Entries indexed by main term name


class Entry(SourceElement):
    """
    A main term with alternative terms, description
    and references
    """

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

METAMODEL = Metamodel(
    id='gl',
    label='glossary',
    extension='.gls',
    modelClass=GlossaryModel
)
# MetamodelDependency(
#     sourceId='gl',
#     targetId='gl',
#     optional=True,
#     multiple=True,
# )