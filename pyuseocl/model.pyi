# coding=utf-8

from typing import Any, Optional, Dict, List
import collections


class SourceElement:

    def __init__(self, name, code=None):
        self.name : str
        self.source : Optional[Any]


class Model(SourceElement):

    def __init__(self, name, code=None):
        self.enumerations : List[Enumeration]  # @property
        self.enumerationNamed : Dict[str, Enumeration]      # collections.OrderedDict
        self.classes      : List[Class]  # @property
        self.classNamed   : Dict[str, Class]            # collections.OrderedDict
        self.associations : List[Association] # # @property
        self.associationNamed : Dict[str, Association]      # collections.OrderedDict
        self.associationsClasses : List[AssociationClass] # # @property
        self.associationClassNamed : Dict[str, AssociationClass]  # collections.OrderedDict
        self.operations   : List[str] # # @property
        self.operationWithSignature   : Dict[str, Operation]        # collections.OrderedDict
        self.invariants   : List[Invariant]
        self.operationConditions : List[OperationCondition]
        self.basicTypes   : List[BasicType] # @property
        self.basicTypeNamed   : Dict[str, BasicType]        # collections.OrderedDict
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
        self.attributes : List[Attribute] # @property
        self.attributeNamed : Dict[str,Attribute] # collections.OrderedDict()
        self.operations : List[Operation] # @property
        self.operationNamed : Dict[str,Operation] # collections.OrderedDict()
        self.invariants : List[Invariant] # @property
        self.invariantNamed : Dict[str,Invariant] # collections.OrderedDict()
        self.outgoingRoles : List[Role] # @computed
        self.incomingRoles : List[Role] # @computed

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
        self.conditions : List[OperationCondition] # @derived
        self.conditionNamed : Dict[str,OperationCondition] # OrderedDict()


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
        self.roles : List[Role] # @property
        self.roleNamed : Dict[str,Role] # collections.OrderedDict()
        self.sourceRole : Role # @property  valid only for binary association
        self.targetRole : Role # @property  valid only for binary association
        self.arity : int      # @property
        self.isBinary : bool  # @property
        self.isNAry : bool    # @property
        self.isManyToMany : bool # @property binary and both roles are many
        self.isOneToOne : bool # @property binary and both roles are one
        self.isForwardOneToMany : bool # @property binary and both roles are one
        self.isBackwardOneToMany : bool # @property binary and both roles are one
        self.isOneToMany : bool # @property binary and both roles are one


class Role(SourceElement):
    def __init__(self, name, association, code=None,
                 cardMin=None, cardMax=None, type=None, isOrdered=False,
                 qualifiers=None, subsets=None, isUnion=False,
                 expression=None):
        self.association : Association
        self.cardinalityMin : int
        self.cardinalityMax : Optional[int]
        self.isOne : bool # @property   card ?..1
        self.isMany : bool # @property   card ?..*
        self.type : Class
        self.isOrdered : bool
        self.qualifiers : Dict[str,SimpleType]
        self.subsets : List[str]
        self.isUnion : List[str]
        self.expression : bool
        self.opposite : Role # @property valid only for binary associations
        self.opposites : List[Role] # @property always valid
        self.isTarget : bool # @property true only for target of binary association
        self.isSource : bool # @property true only for source of binary association

class AssociationClass(Class,Association): ...


class ExpressionPath(object):
    def __init__(self, startClass, pathString):
        self.pathString : str
        self.startClass : Class
        self.elements : Any # ??N self._evaluate(startClass, pathString.split('.'))

