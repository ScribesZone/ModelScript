# coding=utf-8

from typing import Any, Optional, Dict, List
import collections


class SourceElement:

    def __init__(self, name, code=None):
        # name : invariants, preconidtions and postconditions can be anonymous
        # in this case name is empty
        self.name : Optional[str]
        self.source : Optional[Any]
        self.lineNo : int
        self.docComment = Optional[List[str]]
        self.eolComment = Optional[str]


class ClassModel(SourceElement):

    def __init__(self, name, code=None, lineNo=None, docComment=None, eolComment=None):
        self.enumerations : List[Enumeration]  # @property
        self.enumerationNamed : Dict[str, Enumeration]      # OrderedDict
        self.classes      : List[Class]  # @property  Do not contains associationclasses
        self.classNamed   : Dict[str, Class]            # OrderedDict
        self.associations : List[Association] # # @property  Do not contains associationclasses
        self.associationNamed : Dict[str, Association]      # OrderedDict Do not contains associationclasses
        self.associationsClasses : List[AssociationClass] # # @property
        self.associationClassNamed : Dict[str, AssociationClass]  # OrderedDict
        self.operations   : List[str] # # @property
        self.operationWithFullSignature   : Dict[str, Operation] # OrderedDict
        self.operationConditions : List[OperationCondition]
        self.basicTypes   : List[BasicType] # @property
        self.basicTypeNamed   : Dict[str, BasicType]        # OrderedDict

    def findAssociationOrAssociationClass(self, name:str) -> Association: ...
    def findRole(self, associationOrAssociationClassName, roleName:str) -> Role : ...
    def findClassOrAssociationClass(self, name:str) -> Class: ...
    def findInvariant(self, classOrAssociationClassName, invariantName): Invariant: ...




class TopLevelElement(SourceElement):

    def __init__(self, name, model, code=None, lineNo=None, docComment=None, eolComment=None):
        self.model : ClassModel


class SimpleType(object):

    def __init__(self, name, lineNo=None, docComment=None, eolComment=None):
        self.name = name


class BasicType(SimpleType):
    type = 'BasicType'


class Enumeration(TopLevelElement,SimpleType):
    type = 'Enumeration'

    def __init__(
            self, name:str, model:ClassModel, code:Optional[Any], literals:List[str],
            lineNo=None, docComment=None, eolComment=None):
        self.literals : List[str]


class Class(TopLevelElement):

    def __init__(
            self, name, model, isAbstract=False, superclasses=(),
            lineNo=None, docComment=None, eolComment=None):
        self.model : ClassModel
        self.isAbstract : bool
        self.superclasses : List[Class]
        self.attributes : List[Attribute] # @property
        self.attributeNamed : Dict[str,Attribute] # OrderedDict()
        self.operations : List[Operation] # @property
        self.operationWithSignature : Dict[str,Operation] # OrderedDict()
        self.invariants : List[Invariant] # @property
        self.invariantNamed : Dict[str,Invariant] # collections.OrderedDict()
        self.outgoingRoles : List[Role] # @computed
        self.incomingRoles : List[Role] # @computed

class Attribute(SourceElement):
    def __init__(
            self, name, class_, code=None, type=None,
            isDerived=False, isInit=False, expression=None,
            lineNo=None, docComment=None, eolComment=None):
        self.class_ : Class
        self.type : SimpleType # Set(String) is allowed. Currently not managed
        self.isDerived : bool # if "derived =" is used
        self.isInit : bool # if "init :" is used
        self.expression : Optional[str] # either for derived or init expression

class Operation(SourceElement):
    def __init__(
            self, name, model, class_, signature, code=None,expression=None,
            lineNo=None, docComment=None, eolComment=None):
        self.class_ : Class
        self.signature : str
        self.full_signature : str
        self.hasImplementation : bool
        self.expression : Optional[str] # only if hasImplementation
        self.conditions : List[OperationCondition] # @derived
        self.conditionNamed : Dict[str,OperationCondition] # OrderedDict()


class Condition(TopLevelElement):
    def __init__(
            self, name, model, class_, expression, code=None,
            lineNo=None, docComment=None, eolComment=None):
        # name : invariants, preconidtions and postconditions can be anonymous
        # in this case name is empty
        self.class_ : Optional[Class] # could be null as some invariants are toplevel
        self.expression : str


class OperationCondition(Condition):
    def __init__(
            self, name, model, class_, operation, expression, code=None,
            lineNo=None, docComment=None, eolComment=None):
        self.operation : Operation

class PreCondition(OperationCondition):
    def __init__(
            self, name, model, class_, operation, expression, code=None,
            lineNo=None, docComment=None, eolComment=None): ...


class PostCondition(OperationCondition):
    def __init__(
            self, name, model, class_, operation, expression, code=None,
            lineNo=None, docComment=None, eolComment=None): ...


class Invariant(Condition):
    def __init__(self, name, model, class_=None, code=None,
                 variable='self', expression=None,
                 additionalVariables = (), toplevelDefined=True,
                 isExistential=False,
                 lineNo=None, docComment=None, eolComment=None):
        self.toplevelDefined : bool     # only for invariant defined globally. False for thos in classes
        self.variable : str
        self.additionalVariables : List[str]
        self.isExistential : bool
        self.isModelInvariant : bool  # @property


class Association(TopLevelElement):
    def __init__(
            self, name, model, kind=None,
            lineNo=None, docComment=None, eolComment=None):
        self.kind : str # association|composition|aggregation|associationclass  # TODO:should associationclass be there?
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
    def __init__(
            self, name, association, code=None,
            cardMin=None, cardMax=None, type=None, isOrdered=False,
            qualifiers=None, subsets=None, isUnion=False,
            expression=None,
            lineNo=None, docComment=None, eolComment=None):
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

