# coding=utf-8

"""
Glossary metamodel.

    GlossaryModel
        <>--* Entry
"""
from __future__ import print_function

import collections

from typing import Dict, Text, Optional, List

from modelscripts.base.metrics import (
    Metrics,
    Metric
)
from modelscripts.megamodels.dependencies.metamodels import (
    MetamodelDependency
)
from modelscripts.megamodels.elements import SourceModelElement
from modelscripts.megamodels.metamodels import Metamodel
from modelscripts.megamodels.models import Model
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
    """
    Collection of named packages.
    """

    def __init__(self):
        super(GlossaryModel, self).__init__()

        self.packageNamed=collections.OrderedDict()
        # type: Dict[Text, Package]


    @property
    def glossaryList(self):
        #TODO: should be momoized. It is call for each occurrence.
        _=[self]+super(GlossaryModel, self).glossaryList
        return _

    @property
    def textBlocks(self):
        _=super(GlossaryModel, self).textBlocks
        if self.description is not None:
            _.append(self.description)
        for p in self.packages:
            _.extend(p.textBlocks)
        return _

    @property
    def packages(self):
        return list(self.packageNamed.values())

    @property
    def metamodel(self):
        #type: () -> Metamodel
        return METAMODEL


    def findEntry(self, term):
        #type: (Text) -> Optional[Entry]

        # search first as the main term
        for packages in self.packageNamed.values():
            if term in packages.entryNamed:
                return packages.entryNamed[term]

        # search then in inflections
        for packages in self.packageNamed.values():
            for entry in packages.entryNamed.values():
                if term in entry.inflections:
                    return entry

        # search then in synonyms
        for packages in self.packageNamed.values():
            for entry in packages.entryNamed.values():
                if term in entry.synonyms:
                    return entry

        return None

    # def resolve(self):
    #     self.resolveTextBlocks()

    @property
    def metrics(self):
        #type: () -> Metrics
        ms=super(GlossaryModel, self).metrics
        ms.add(Metric('package', len(self.packages)))
        ms.add(Metric(
            label='entry',
            plural='entries',
            n=sum(len(d.entries) for d in self.packages)))
        return ms


class Package(SourceModelElement):
    """
    A collection of entry indexed by the main term.
    """

    def __init__(self, glossaryModel, name, astNode=None):
        super(Package, self).__init__(
            model=glossaryModel,
            name=name,
            astNode=astNode
        )
        self.isResolved=False
        self.glossaryModel=glossaryModel
        self.glossaryModel.packageNamed[name]=self
        self.impliciteDeclaration = True
        self.entryNamed=collections.OrderedDict()
        # type: Dict[Text, Entry]
        # Entries indexed by main term name

    @property
    def entries(self):
        return self.entryNamed.values()

    @property
    def textBlocks(self):
        _=[]
        if self.description is not None:
            _.append(self.description)
        for p in self.entries:
            _.extend(p.textBlocks)
        return _



class Entry(SourceModelElement):
    """
    A main term with alternative terms, description
    and references
    """

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
        # TODO: check, unique main/alternative(?) term
        self.package=package
        #type: Package

        self.package.entryNamed[term]=self

        self.term=term
        #type: Text

        self.synonyms=list(synonyms)
        #type: List[Text]

        self.inflections=list(inflections)
        #type: List[Text]

        self.label=label
        #type: Optional[Text]

        self.translations=(
            {} if translations is None
            else translations )
        #type: Dict[Text, Text]

        self.occurrences=[]
        #type: List['TextReference']
        """ Occurrences that refer to this entry """

        self.isResolved=False

    @property
    def textBlocks(self):
        _=[]
        if self.description is not None:
            _.append(self.description)
        return _

METAMODEL = Metamodel(
    id='gl',
    label='glossary',
    extension='.gls',
    modelClass=GlossaryModel
)
MetamodelDependency(
    sourceId='gl',
    targetId='gl',
    optional=True,
    multiple=True,
)

