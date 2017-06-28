# coding=utf-8

from typing import Any, Optional, Dict, List
import collections


class SourceElement:

    def __init__(self, name, code=None):
        self.name : str
        self.source : Optional[Any]


class Model(SourceElement):

    def __init__(self, name, code=None):
        self.enumerations : Dict[str, Enumeration]      # collections.OrderedDict
        self.classes      : Dict[str, Class]            # collections.OrderedDict
        self.associations : Dict[str, Association]      # collections.OrderedDict
        self.associationsClasses : Dict[str, AssociationClass]  # collections.OrderedDict
        self.operations   : Dict[str, Operation]        # collections.OrderedDict
        self.invariants   : List[Invariant]
        self.operationConditions : List[OperationCondition]
        self.basicTypes   : Dict[str, BasicType]        # collections.OrderedDict
    def findAssociationOrAssociationClass(self, name:str) -> Association: ...
    def findRole(self, associationOrAssociationClassName, roleName:str) -> Role : ...
    def findClassOrAssociationClass(self, name:str) -> Class: ...
    def findInvariant(self, classOrAssociationClassName, invariantName): Invariant: ...




class TopLevelElement(SourceElement):

    def __init__(self, name, model, code=None):
        self.model : Model


class SimpleType(object):

    def __init__(self, name):
        self.name = name


class BasicType(SimpleType):
    type = 'BasicType'


class Enumeration(TopLevelElement,SimpleType):
    type = 'Enumeration'

    def __init__(self, name:str, model:Model, code:Optional[Any], literals:List[str]):
        self.literals : List[str]


class Class(TopLevelElement):

    def __init__(self, name, model, isAbstract=False, superclasses=()):
        self.isAbstract : bool
        self.superclasses : List[Class]
        self.attributes : Dict[str,Attribute] # collections.OrderedDict()
        self.operations : Dict[str,Operation] # collections.OrderedDict()
        self.invariants : Dict[str,Invariant] # collections.OrderedDict()


class Attribute(SourceElement):
    def __init__(self, name, class_, code=None, type=None):
        self.class_ : Class
        self.type : SimpleType


class Operation(SourceElement):
    def __init__(self, name, model, class_, signature, code=None,expression=None):
        self.class_ : Class
        self.signature : str
        self.full_signature : str
        self.expression : str


class OperationCondition(TopLevelElement):
    def __init__(self, name, model, operation, expression, code=None ):
        self.expression : str


class PreCondition(OperationCondition):
    def __init__(self, name, model, operation, expression, code=None ): ...


class PostCondition(OperationCondition):
    def __init__(self, name, model, operation, expression, code=None ): ...


class Invariant(TopLevelElement):
    def __init__(self, name, model, class_=None, code=None,
                 variable='self', expression=None,
                 additionalVariables = (),
                 isExistential=False):
        self.class_ : Class
        self.expression : str
        self.variable : str
        self.additionalVariables : List[str]
        self.isExistential : bool


class Association(TopLevelElement):
    def __init__(self, name, model, kind=None):
        self.kind : str # type: List[str]
        self.roles : Dict[str,Role]
        self.arity : int
        self.isBinary : bool


class Role(SourceElement):
    def __init__(self, name, association, code=None,
                 cardMin=None, cardMax=None, type=None, isOrdered=False,
                 qualifiers=None, subsets=None, isUnion=False,
                 expression=None):
        self.association : Association
        self.cardinalityMin : int
        self.cardinalityMax : Optional[int]
        self.type : Class
        self.isOrdered : bool
        self.qualifiers : Dict[str,SimpleType]
        self.subsets : List[str]
        self.isUnion : List[str]
        self.expression : bool
        self.opposite : Optional[Role] # set for binary association only

class AssociationClass(Class,Association): ...


class ExpressionPath(object):
    def __init__(self, startClass, pathString):
        self.pathString : str
        self.startClass : Class
        self.elements : Any # ??N self._evaluate(startClass, pathString.split('.'))

