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

from modelscribes.megamodels.metamodels import Metamodel
from modelscribes.megamodels.models import Model
from modelscribes.megamodels.elements import SourceModelElement
from modelscribes.base.metrics import Metrics


class GlossaryModel(Model):
    """
    Collection of named domains.
    """

    def __init__(self):
        super(GlossaryModel, self).__init__()

        self.domainNamed=collections.OrderedDict()
        # type: Dict[Text, Domain]

    @property
    def domains(self):
        return list(self.domainNamed.values())

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


    # def resolveTextBlock(self, textBlock):
    #     for line in textBlock.lines:
    #         for token in line.tokens:
    #             if isinstance(token, Reference):
    #                 reference=token
    #                 reference.resolve(self)

    @property
    def metrics(self):
        #type: () -> Metrics
        ms=super(GlossaryModel, self).metrics
        ms.addList((
            ('domain', len(self.domains)),
            ('entry', sum(
                len(d.entries)
                for d in self.domains
            ))
        ))
        return ms


class Domain(SourceModelElement):
    """
    A collection of entry indexed by the main term.
    """


    def __init__(self, glossaryModel, name, lineNo=None):
        super(Domain, self).__init__(
            model=glossaryModel,
            name=name,
            lineNo=lineNo
        )
        self.glossaryModel=glossaryModel
        self.glossaryModel.domainNamed[name]=self
        self.entryNamed=collections.OrderedDict()
        # type: Dict[Text, Entry]
        # Entries indexed by main term name

    @property
    def entries(self):
        return self.entryNamed.values()


class Entry(SourceModelElement):
    """
    A main term with alternative terms, description
    and references
    """

    def __init__(self,
                 domain,
                 mainTerm,
                 alternativeTerms=(),
                 lineNo=None):
        super(Entry, self).__init__(
            model=domain.glossaryModel,
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

        self.occurrences=[]
        #type: List['Occurrence']


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

