# coding=utf-8

"""
Metamodel for relation models. These models contains relations.
Each relation contains columns and contraints.
Constraints can be key constraits, dependency constraints,
domain constraints and foreign key constraints.
"""


from collections import OrderedDict
from typing import List, Optional, Dict, Text, Union
from abc import ABCMeta, abstractmethod

# TODO:- to be continued
from modelscript.megamodels.py import (
    MAttribute
)
from modelscript.megamodels.elements import SourceModelElement
from modelscript.base.metrics import Metrics
from modelscript.megamodels.metamodels import Metamodel
from modelscript.megamodels.models import (
    Model,
    Placeholder)
from modelscript.megamodels.dependencies.metamodels import (
    MetamodelDependency
)
from modelscript.metamodels.permissions.sar import Resource
# used for typing
from modelscript.metamodels.glossaries import (
    GlossaryModel,
    METAMODEL as GLOSSARY_METAMODEL
)
from modelscript.metamodels.classes import (
    ClassModel,
    METAMODEL as CLASS_METAMODEL
)

__all__=(
    'RelationModel',
    'Relation',
    'Column',
    'Constraint',
    'Key',

)


class RelationModel(Model):

    def __init__(self):
        super(RelationModel, self).__init__()

        self._relationNamed = OrderedDict()
        # type: Dict[Text, Relation]

        self._glossaryModel='**not yet**'
        #type: Union[Text, Optional[GlossaryModel]]
        # will be set to the glossary model if any or None

        self._classModel='**not yet**'
        #type: Union[Text, Optional[ClassModel]]
        # will be set to the class model if any or None

        self.storyEvaluation=None
        #type: Optional['StoryEvaluation']
        #type
        # filled only if this model is the result of a story evaluation.
        # Otherwise this is most probably a handmade model.

    @property
    def glossaryModel(self):
        #type: ()-> GlossaryModel
        if self._glossaryModel is '**not yet**':
            self._glossaryModel=self.theModel(GLOSSARY_METAMODEL)
        return self._glossaryModel

    @property
    def classModel(self):
        #type: ()-> ClassModel
        if self._classModel is '**not yet**':
            self._classModel=self.theModel(CLASS_METAMODEL)
        return self._classModel

    def relation(self, name):
        if name in self._relationNamed:
            return self._relationNamed[name]
        else:
            return None

    @property
    def relations(self):
        #type: () -> List[Relation]
        return list(self._relationNamed.values())

    @property
    def metrics(self):
        #type: () -> Metrics
        ms=super(RelationModel, self).metrics
        ms.addList((
            ('relation', len(self.relations)),
            ('column',sum(
                len(o.columns)
                for o in self.relations))
        ))
        return ms

    @property
    def metamodel(self):
        #type: () -> Metamodel
        return METAMODEL



class Entity(Resource, metaclass=ABCMeta):
    pass


class Member(Resource, metaclass=ABCMeta):
    pass


class Relation(SourceModelElement, Entity):

    META_COMPOSITIONS = [
        'columns',
    ]

    def __init__(self, name, model,
                 astNode=None, lineNo=None, description=None):
        super(Relation, self).__init__(
            name=name,
            model=model,
            astNode=astNode,
            lineNo=lineNo,
            description=description)
        self.model._relationNamed[name] = self
        self._columnNamed = OrderedDict()


    @property
    def columns(self):
        return list(self._columnNamed.values())

    def column(self, name):
        if name in self._columnNamed:
            return self._columnNamed[name]
        else:
            return None

    @property
    def columnNames(self):
        return list(self.columnNames.keys())


class Column(SourceModelElement, Member):
    """
    Attributes.
    """

    def __init__(self, name, relation, type=None,
                 description=None,
                 lineNo=None, astNode=None):
        SourceModelElement.__init__(
            self,
            model=relation.model,
            name=name,
            astNode=astNode,
            lineNo=lineNo, description=description)
        self.relation = relation
        self.relation.columnNamed[name] = self
        self.type = type # string later resolved as SimpleType

    @property
    def label(self):
        return '%s.%s' % (self.relation.label, self.name)

class Constraint(SourceModelElement):
    pass

class Key(SourceModelElement):
    pass

METAMODEL = Metamodel(
    id='re',
    label='relation',
    extension='.res',
    modelClass=RelationModel
)
MetamodelDependency(
    sourceId='re',
    targetId='gl',
    optional=True,
    multiple=True,
)
MetamodelDependency(
    sourceId='re',
    targetId='cl',
    optional=True,
    multiple=True,
)