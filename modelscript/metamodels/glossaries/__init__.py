# coding=utf-8

"""
Glossary metamodel.

    GlossaryModel
        <>--* Package
            <>--* Entry (indexed by name)
"""


import collections

from typing import Dict, Text, Optional, List

from modelscript.base.metrics import (
    Metrics,
    Metric
)
from modelscript.megamodels.dependencies.metamodels import (
    MetamodelDependency
)
from modelscript.megamodels.elements import SourceModelElement
from modelscript.megamodels.metamodels import Metamodel
from modelscript.megamodels.models import Model
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
    Glossaries allows to seach entry by name.
    Package are namespace, that is terms with the same name may exists
    in different packages.
    """

    def __init__(self):
        super(GlossaryModel, self).__init__()

        self.packageNamed=collections.OrderedDict()
        # type: Dict[Text, Package]


    @property
    def glossaryList(self):
        #TODO:4 should be momoized. It is call for each occurrence.
        _=[self]+super(GlossaryModel, self).glossaryList
        return _

    @property
    def packages(self):
        return list(self.packageNamed.values())

    @property
    def metamodel(self):
        #type: () -> Metamodel
        return METAMODEL


    def findEntry(self, term):
        """
        Find an entry given a string (the term to be found)/
        """
        #type: (Text) -> Optional[Entry]

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
    A collection of entry indexed by the (main) term.
    A package is named and is a part of a glossary.
    """

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
        self.isResolved=False

        self.glossaryModel=glossaryModel

        self.glossaryModel.packageNamed[name]=self

        self.description=description

        self.entryNamed=collections.OrderedDict()
        # type: Dict[Text, Entry]
        # Entries indexed by main term name

    @property
    def entries(self):
        return list(self.entryNamed.values())


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
        # TODO:3 check, unique main/alternative(?) term
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


METAMODEL = Metamodel(
    id='gl',
    label='glossary',
    extension='.gls',
    modelClass=GlossaryModel
)
