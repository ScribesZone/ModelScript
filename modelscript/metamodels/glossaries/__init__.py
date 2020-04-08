# coding=utf-8
"""Glossary metamodel.

    GlossaryModel
        <>--* Package
            <>--* Entry (indexed by name)
"""

import collections
from typing import Dict, Text, Optional, List

from modelscript.base.metrics import (
    Metrics,
    Metric)
from modelscript.megamodels.dependencies.metamodels import (
    MetamodelDependency
)
from modelscript.megamodels.elements import SourceModelElement
from modelscript.megamodels.metamodels import Metamodel
from modelscript.megamodels.models import Model

__all__ = (
    'GlossaryModel',
    'Package',
    'Entry',
    'METAMODEL'
)

# class WithTextBlockModel(object):
#
#     def __init__(self):
#         self.glossaryList=[]
#         #type: List[GlossaryModel]
#         # Filled later. The list of glossary used to solve text block
#
#         self.textBlocks=[]


# GlossaryDependent must be first !


class GlossaryModel(Model):
    """Collection of named packages.
    Glossaries allows to search entry by name.
    Package are namespaces, that is terms with the same name may exists
    in different packages.
    """

    packageNamed: Dict[Text, 'Package']

    def __init__(self):
        super(GlossaryModel, self).__init__()
        self.packageNamed = collections.OrderedDict()

    @property
    def glossaryList(self):
        #TODO:4 should be memoized. It is call for each occurrence.
        _ = [self]+super(GlossaryModel, self).glossaryList
        return _

    @property
    def packages(self):
        return list(self.packageNamed.values())

    @property
    def metamodel(self) -> Metamodel:
        return METAMODEL

    def findEntry(self, term: str)-> Optional['Entry']:
        """Find an entry given a string (the term to be found)/
        """
        # search first as the main term
        for packages in list(self.packageNamed.values()):
            if term in packages.entryNamed:
                return packages.entryNamed[term]

        # search then in inflections
        for packages in list(self.packageNamed.values()):
            for entry in list(packages.entryNamed.values()):
                if term in entry.inflections:
                    return entry

        # search then in synonyms
        for packages in list(self.packageNamed.values()):
            for entry in list(packages.entryNamed.values()):
                if term in entry.synonyms:
                    return entry

        return None

    @property
    def metrics(self) -> Metrics:
        ms = super(GlossaryModel, self).metrics
        ms.add(Metric('package', len(self.packages)))
        ms.add(Metric(
            label='entry',
            plural='entries',
            n=sum(len(d.entries) for d in self.packages)))
        return ms


class Package(SourceModelElement):
    """A collection of entry indexed by the (main) term.
    A package is named and is a part of a glossary.
    """

    isResolved: bool
    glossaryModel: GlossaryModel
    description: Optional[str]
    entryNamed: Dict[Text, 'Entry']
    """Entries indexed by main term name"""

    def __init__(self,
                 glossaryModel,
                 name,
                 description=None,
                 astNode=None):
        super(Package, self).__init__(
            model=glossaryModel,
            name=name,
            astNode=astNode
        )
        self.isResolved = False
        self.glossaryModel = glossaryModel
        self.glossaryModel.packageNamed[name] = self
        self.description = description
        self.entryNamed = collections.OrderedDict()

    @property
    def entries(self):
        return list(self.entryNamed.values())


class Entry(SourceModelElement):
    """A main term with alternative terms, description
    and references
    """

    package: Package
    term: str
    synonyms: List[str]
    inflections: List[str]
    label: Optional[str]
    translations: Dict[str, str]
    occurrences: List['TextReference']
    isResolved: bool

    def __init__(self,
                 package,
                 term,
                 label=None,
                 synonyms=(),
                 inflections=(),
                 translations=None,
                 astNode=None):
        super(Entry, self).__init__(
            model=package.glossaryModel,
            name=None,
            astNode=astNode
        )
        # TODO:3 check, unique main/alternative(?) term
        self.package = package
        self.package.entryNamed[term] = self
        self.term = term
        self.synonyms = list(synonyms)
        self.inflections = list(inflections)
        self.label = label
        self.translations = (
            {} if translations is None
            else translations )
        self.occurrences = []
        self.isResolved = False


METAMODEL = Metamodel(
    id='gl',
    label='glossary',
    extension='.gls',
    modelClass=GlossaryModel
)
