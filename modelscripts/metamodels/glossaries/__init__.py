# coding=utf-8

"""
Glossary metamodel.

    GlossaryModel
        <>--* Entry
"""
from __future__ import print_function

import collections

from typing import Dict, Text, Optional, List

from modelscripts.megamodels.metamodels import Metamodel
from modelscripts.megamodels.models import Model
from modelscripts.megamodels.elements import SourceModelElement
from modelscripts.base.metrics import Metrics

class GlossaryModel(Model):
    """
    Collection of named packages.
    """

    def __init__(self):
        super(GlossaryModel, self).__init__()

        self.packageNamed=collections.OrderedDict()
        # type: Dict[Text, Package]

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
            ('packages', len(self.packages)),
            ('entry', sum(
                len(d.entries)
                for d in self.packages
            ))
        ))
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
        self.glossaryModel=glossaryModel
        self.glossaryModel.packageNamed[name]=self
        self.impliciteDeclaration = True
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

