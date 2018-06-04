# coding=utf-8

"""
Class metamodel.

The structure of this package is::

    ClassModel
    <>--* Package
        <>--* Enumeration
        <>--* Class
              <>--* Attribute
              <>--* Operation
                    <>--* OperationCondition
              <>--* Invariant
        <>--* Association
              <>--2 Role
        <>--* AssociationClass
              <>--2 Role
              <>--* Attribute
              <>--* Operation
                    <>--* OperationCondition
        <>--* DataType

    Association, Class
    <|--  AssociationClass

    PackagableElement
    <|-- Enumeration

    SimpleType
    <|--  DataType
    <|--  Enumeration

"""
from __future__ import print_function

import abc
import collections
import logging

from typing import Text, Optional, Union, List, Dict

# TODO: to be continued
from modelscripts.megamodels.py import (
    MComposition,
    MReference,
    MAttribute
)
from modelscripts.megamodels.elements import SourceModelElement
from modelscripts.base.metrics import Metrics
from modelscripts.megamodels.metamodels import Metamodel
from modelscripts.megamodels.dependencies.metamodels import (
    MetamodelDependency
)
from modelscripts.megamodels.models import Model
from modelscripts.metamodels.permissions.sar import Resource

META_CLASSES=( # could be in __all__ (not used by PyParse)
    'ClassModel',
    'PackagableElement',
    'Entity',
    'Member',
    'SimpleType',
    'DataType',
    'Enumeration',
    'EnumerationLiteral',
    'Class',
    'Attribute',
    'Operation',
    'Association',
    'Role',
    'AssociationClass',
)

__all__= META_CLASSES



#TODO: make associationclass class and assoc + property
# currently the implem is based on separated list for assocclass
# not sure if this should be changed. We start to introduce
# the method 'regularClasses and regularAssociations' but
# we have to check if the storage should be changed or not


#TODO: check if cardinality handling is ok
# It seems that there is a bug with * ou 1..*

# logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('test.' + __name__)

class ClassModel(Model):
    """
    Class model.
    """
    # metaMembers = [
    #       MComposition('enumerations : Enumeration[*] inv model'),
    #       MComposition('regularClasses : Class [*] inv model'),
    #       MComposition(
    #           'associationsClasses : Association[*] inv model'),
    #       MComposition('dataTypes : DataType[*] inv model'),
    # ]


    #TODO: convert this to MComposition when ready
    META_COMPOSITIONS=[
        'enumerations',
        'regularClasses',
        'regularAssociations',
        'associationClasses',
        'dataTypes',
        'packages',
    ]
    def __init__(self):
        #type: () -> None
        super(ClassModel, self).__init__()

        self._isResolved=False

        self.enumerationNamed=collections.OrderedDict() #type: Dict[Text, Enumeration]
        #: Map of enumerations, indexed by name.

        #: Map of data types. Indexed by type names/
        #: populated during the resolution phase
        self.dataTypeNamed=collections.OrderedDict()  #type: Dict[Text, DataType]

        self.classNamed = collections.OrderedDict()  #type: Dict[Text, Class]
        #: Map of classes (including association classes), indexed by name.
        #: Use regularClassNamed to get only classes

        self.associationNamed = collections.OrderedDict() #type: Dict[Text, Association]
        #: Map of associations (including association classes), indexed by name.
        #: Use regularClassNamed to get only classes

        #: Map of association classes, indexed by name.
        self.associationClassNamed = collections.OrderedDict()  #type: Dict[Text, AssociationClass]

        # #: Map of operations, indexed by operation full signatures.
        # #: e.g. 'Person::raiseSalary(rate : Real) : Real
        self.operationWithFullSignature = collections.OrderedDict()  #type: Dict[Text, Operation]

        # ALL packages, not only the top level ones
        self.packageNamed=collections.OrderedDict() #type: Dict[Text, Package]

        #: List of all conditions (inv/pre/post).
        #  Both those that are declared within a class
        #  or those declared with a context at top level.
        #  Used for resolution.
        self._conditions = [] #type: List['Condition']


    @property
    def metamodel(self):
        return METAMODEL

    @MComposition('Package[*] inv model')
    def packages(self):
        return self.packageNamed.values()

    @property
    def packageNames(self):
        return self.packageNamed.keys()

    @MComposition('Enumeration[*] inv model')
    def enumerations(self):
        return self.enumerationNamed.values()

    @property
    def enumerationNames(self):
        return self.enumerationNamed.keys()

    @MReference('Class[*] inv model')
    def classes(self):
        """
        All classes or association classes.
        Use 'regularClasses' to remove association classes.
        """
        #TODO: check if this should be changed
        # with classNamed semantics changed
        return self.classNamed.values()

    @property
    def classNames(self):
        return self.classNamed.keys()

    @MComposition('Class[*] inv model')
    def regularClasses(self):
        return [
            class_ for class_ in self.classes
            if type(class_) == Class
            ]

    @property
    def regularClassNames(self):
        return [class_.name for class_ in self.regularClasses]

    @MReference('Association[*] inv model')
    def associations(self):
        return self.associationNamed.values()

    @property
    def associationNames(self):
        return self.associationNamed.keys()

    @MComposition('Association[*] inv model')
    def regularAssociations(self):
        return [
            association for association in self.associations
            if type(association) == Association
            ]

    @property
    def regularAssociationNames(self):
        return [a.name for a in self.regularAssociations]

    @MComposition('AssociationClass[*] inv model')
    def associationClasses(self):
        return self.associationClassNamed.values()

    @property
    def associationClassNames(self):
        return self.associationClassNamed.keys()

    @property
    def simpleTypeNamed(self):
        _ = self.dataTypeNamed.copy()
        _.update(self.enumerationNamed)
        return _

    @property
    def simpleTypes(self):
        return self.simpleTypeNamed.values()

    @property
    def simpleTypeNames(self):
        return self.simpleTypeNamed.keys()

    @MComposition('DataType[*] inv model')
    def dataTypes(self):
        return self.dataTypeNamed.values()

    @property
    def dataTypeNames(self):
        return self.dataTypeNamed.keys()

    @property
    def metrics(self):
        #type: () -> Metrics
        ms=super(ClassModel, self).metrics
        ms.addList((
            ('package', len(self.packages)),
            ('data type', len(self.dataTypes)),
            ('enumeration', len(self.enumerations)),
            ('enumeration literal', len(
                [el
                    for e in self.enumerations
                        for el in e.literals])),
            ('regular class', len(self.regularClasses) ),
            ('regular association',
                len(self.regularAssociations)),
            ('association class', len(self.associationClasses)),
        ))
        return ms

    def __str__(self):
        # TODO: move this to printer
        def category_line(label,elems):
            print(label)
            print(elems)
            n = len(list(elems))
            return '% 3d %s: %s' % (
                n,
                label.ljust(22),
                ','.join(elems)
            )
        categories = [
            ('packages', self.packageNames),
            ('data types', self.dataTypeNames),
            ('enumerations', self.enumerationNames),
            ('regular classes', self.regularClassNames),
            ('regular associations', self.associationNames),
            ('association classes', self.associationClassNames),
            ('operations', self.operationWithFullSignature.keys()),
            # ('invariants'           ,[i.name for i in self.invariants]),  FIXME: should be replaced
        ]
        total = 0
        lines = [ 'class model '+self.name ]
        for (label, items) in categories:
            lines.append(category_line(label, items))
            total += len(list(items))
        print(lines)
        lines.append('% 3d' % total)
        return  '\n'.join(lines)


    def _findAssociationOrAssociationClass(self, name):
        # TODO: check this implementation
        # should be most probably changed into
        # associationNamed property
        log.debug('_findAssociationOrAssociationClass:%s', name)
        if name in self.associationNamed:
            return self.associationNamed[name]
        elif name in self.associationClassNamed:
            return self.associationClassNamed[name]
        else:
            raise Exception('ERROR - %s : No association or association class'
                            % name )

    def _findClassOrAssociationClass(self, name):
        #type: (Text) -> Union[Class, AssociationClass]
        # TODO: see _findAssociationOrAssociationClass
        if name in self.classNamed:
            return self.classNamed[name]
        elif name in self.associationClassNamed:
            return self.associationClassNamed[name]
        else:
            raise Exception('ERROR - %s : No class or association class'
                            % name)

    def _findRole(self, associationOrAssociationClassName, roleName):
        # TODO: see _findAssociationOrAssociationClass
        # though there are two parmeters here
        log.debug('_findRole: %s::%s',
                  associationOrAssociationClassName, roleName)
        a = self._findAssociationOrAssociationClass(
                    associationOrAssociationClassName)

        log.debug('_findRole:  %s ',a)
        log.debug('_findRole:  %s ',a.roles)
        if roleName in a.roleNamed:
            return a.roleNamed[roleName]
        else:
            raise Exception('ERROR - No "%s" role on association(class) %s' %
                            (roleName, associationOrAssociationClassName)  )




    def _findInvariant(self, classOrAssociationClassName, invariantName):
        #type: (Text, Text) -> 'Invariant'
        c = self._findClassOrAssociationClass(
                    classOrAssociationClassName)
        if invariantName in c.invariantNamed:
            return c.invariantNamed[invariantName]
        else:
            raise Exception('ERROR - No "%s" invariant on class %s' %
                            (invariantName, classOrAssociationClassName))


class PackagableElement(SourceModelElement):
    """
    Top level element.
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self,
                 name,
                 model,
                 astNode=None,
                 package=None,
                 lineNo=None, description=None):
        super(PackagableElement, self).__init__(
            model=model,
            name=name,
            astNode=astNode,
            lineNo=lineNo, description=description)
        self.package=package
        if self.package is not None:
            self.package.addElement(self)

    @MAttribute('String')
    def label(self):
        if self.package is not None:
            return '%s.%s' % (
                self.package.label,
                self.name)
        else:
            return self.name

class Entity(Resource):
    __metaclass__ = abc.ABCMeta


class Member(Resource):
    __metaclass__ = abc.ABCMeta


class SimpleType(PackagableElement):
    """
    Simple types.
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self,
                 name,
                 model,
                 astNode=None,
                 package=None,
                 lineNo=None, description=None):
        super(SimpleType, self).__init__(
            model=model,
            name=name,
            package=package,
            astNode=astNode, lineNo=lineNo, description=description)


    @MAttribute('String')
    def label(self):
        return self.name



class DataType(SimpleType):
    """
    Data types such as integer.
    Data types are not explicitly defined in the source
    file, but they are used after after symbol resolution.
    """
    # not in sources, but used created during symbol resolution
    type = 'DataType'

    def __init__(self, model, name, astNode=None, package=None):
        super(DataType, self).__init__(
            model=model,
            name=name,
            astNode=astNode,
            package=package
        )
        self.model.dataTypeNamed[name]=self

    def __repr__(self):
        return self.name


class Package(PackagableElement, Entity):
    """
    Packages.
    """
    def __init__(self,
                 name,
                 model,
                 astNode=None,
                 package=None,
                 lineNo=None, description=None):
        super(Package, self).__init__(
            name=name,
            model=model,
            astNode=astNode,
            package=package,
            lineNo=lineNo, description=description,)
        self._elememts=[]
        self.model.packageNamed[name]=self


    @property
    def elements(self):
        return self._elememts

    def addElement(self, element):
        assert element is not None
        if element not in self._elememts:
            self._elememts.append(element)
            element.package=self


class Enumeration(SimpleType):
    """
    Enumerations.
    """
    META_COMPOSITIONS = [
        'literals',
    ]
    type = 'Enumeration'

    # metaMembers = [
    #       Reference('model : Model inv enumerations'),
    # ]

    def __init__(self,
                 name,
                 model,
                 package=None,
                 astNode=None,
                 lineNo=None, description=None):
        super(Enumeration, self).__init__(
            name,
            model,
            package=package,
            astNode=astNode,
            lineNo=lineNo,
            description=description)
        self.model.enumerationNamed[name] = self
        self._literals=[]

    @MComposition('EnumerationLiteral[*] inv enumeration')
    def literals(self):
        return self._literals

    # def addLiteral(self, name):
    #     self.literals.append(name)


    def __repr__(self):
        return '%s(%s)' % (self.name, repr(self.literals))

class EnumerationLiteral(SourceModelElement):

    def __init__(self, name, enumeration, astNode=None, lineNo=None,
                 description=None):
        SourceModelElement.__init__(
            self,
            model=enumeration.model,
            astNode=astNode,
            name=name,
            lineNo=lineNo, description=description)
        self.enumeration=enumeration
        self.enumeration._literals.append(self)


class Class(PackagableElement, Entity):
    """
    Classes.
    """

    META_COMPOSITIONS = [
        'attributes',
        'operations',
        'invariants',
    ]

    def __init__(self, name, model, isAbstract=False, superclasses=(),
                 package=None, lineNo=None, description=None, astNode=None):
        super(Class, self).__init__(
            name=name,
            model=model,
            package=None,
            astNode=astNode,
            lineNo=lineNo,
            description=description)
        self.model.classNamed[name] = self
        self.isAbstract = isAbstract
        self.superclasses = superclasses  # strings resolved as classes
        #FIXME: add support for inheritance
        self.attributeNamed = collections.OrderedDict()
        # Signature looks like op(p1:X):Z
        self.operationWithSignature = collections.OrderedDict()
        # Anonymous invariants are indexed with id like _inv2
        # but their name (in Invariant) is always ''
        # This id is just used internaly
        self.invariantNamed = collections.OrderedDict()   # after resolution
        self.outgoingRoles = [] # after resolution
        self.incomingRoles = [] # after resolution

    @property
    def attributes(self):
        return self.attributeNamed.values()

    @property
    def attributeNames(self):
        return self.attributeNamed.keys()

    @property
    def operations(self):
        return self.operationWithSignature.values()

    @property
    def invariants(self):
        return self.invariantNamed.values()

    @property
    def invariantNames(self):
        return self.invariantNamed.keys()


class Attribute(SourceModelElement, Member):
    """
    Attributes.
    """

    def __init__(self, name, class_, type=None,
                 description=None,
                 visibility='public',
                 isDerived=False,
                 isOptional=False,
                 isId=False,
                 isReadOnly=False,
                 isInit=False, expression=None,
                 lineNo=None, astNode=None):
        SourceModelElement.__init__(
            self,
            model=class_.model,
            name=name,
            astNode=astNode,
            lineNo=lineNo, description=description)
        self.class_ = class_
        self.class_.attributeNamed[name] = self
        self.type = type # string later resolved as SimpleType
        self._isDerived = isDerived
        self.visibility=visibility
        self.isOptional = isOptional
        self.isInit = isInit
        self.expression = expression
        self.isId=isId
        self.isReadOnly=isReadOnly

    @MAttribute('Boolean')
    def isDerived(self):
        return self._isDerived

    @isDerived.setter
    def isDerived(self,isDerived):
        self._isDerived=isDerived

    @property
    def label(self):
        return '%s.%s' % (self.class_.label, self.name)

# class Parameter

class Operation(SourceModelElement, Member):
    """
    Operations.
    """
    META_COMPOSITIONS = [
        'conditions',
    ]

    def __init__(self, name,  class_, signature, code=None,
                 expression=None, astNode=None,
                 lineNo=None, description=None):
        SourceModelElement.__init__(
            self,
            model=class_.model,
            name=name,
            astNode=astNode,
            lineNo=lineNo, description=description)
        self.class_ = class_
        self.signature = signature
        self.class_.operationWithSignature[signature] = self
        self.full_signature = '%s::%s' % (class_.name, self.signature)
        self.class_.model.operationWithFullSignature[self.full_signature] = self
        # self.parameters = parameters
        # self.return_type = return_type
        self.expression = expression
        # Anonymous pre/post are indexed with id like _pre2/_post6
        # but their name (in PreCondition/PostCondition) is always ''
        # This id is just used internaly
        self.conditionNamed = collections.OrderedDict() #type: Dict[Text, 'Condition']

    @property
    def label(self):
        return '%s.%s' % (self.class_.label, self.name)

    @MComposition('Condition[*]')
    def conditions(self):
        return self.conditionNamed.values()

    def conditionNames(self):
        return self.conditionNamed.keys()


    @MAttribute('Boolean')
    def hasImplementation(self):
        return self.expression is not None


class Association(PackagableElement, Entity):
    """
    Associations.
    """
    META_COMPOSITIONS = [
        'roles',
    ]

    def __init__(self,
                 name, model, kind=None, package=None,
                 lineNo=None, description=None, astNode=None):
        # type: (Text,ClassModel,Optional[Text],Optional[int],Optional[Text],Optional[Text]) -> None
        super(Association, self).__init__(
            name=name,
            model=model,
            package=package,
            astNode=astNode,
            lineNo=lineNo, description=description)
        self.model.associationNamed[name] = self
        self.kind = kind   # association|composition|aggregation|associationclass  # TODO:should associationclass be
        # there?
        self.roleNamed = collections.OrderedDict() # indexed by name

    @MComposition('Role[*]')
    def roles(self):
        return self.roleNamed.values()

    @property
    def roleNames(self):
        return self.roleNamed.values()

    @MAttribute('Integer')
    def arity(self):
        return len(self.roles)

    @MAttribute('Boolean')
    def isBinary(self):
        return self.arity == 2

    @MAttribute('Boolean')
    def isNAry(self):
        return self.arity >= 3

    @MReference('Role')
    def sourceRole(self):
        if not self.isBinary:
            raise ValueError(
                '"sourceRole" is not defined on "%s" n-ary association' % (
                    self.name
                ))
        return self.roles[0]

    @MReference('Role')
    def targetRole(self):
        if not self.isBinary:
            raise ValueError(
                '"targetRole" is not defined on "%s" n-ary association' % (
                    self.name
                ))
        return self.roles[1]

    @MAttribute('Boolean')
    def isManyToMany(self):
        return (
            self.isBinary
            and self.roles[0].isMany
            and self.roles[1].isMany
        )

    @MAttribute('Boolean')
    def isOneToOne(self):
        return (
            self.isBinary
            and self.roles[0].isOne
            and self.roles[1].isOne
        )

    @MAttribute('Boolean')
    def isForwardOneToMany(self):
        return (
            self.isBinary
            and self.roles[0].isOne
            and self.roles[1].isMany
        )

    @MAttribute('Boolean')
    def isBackwardOneToMany(self):
        return (
            self.isBinary
            and self.roles[0].isMany
            and self.roles[1].isOne
        )

    @MAttribute('Boolean')
    def isOneToMany(self):
        return self.isForwardOneToMany or self.isBackwardOneToMany


class Role(SourceModelElement, Member):
    """
    Roles.
    """

    def __init__(self, name, association, astNode=None,
                 cardMin=None, cardMax=None, type=None, isOrdered=False,
                 qualifiers=None, subsets=None, isUnion=False,
                 expression=None,
                 lineNo=None, description=None):

        # unamed role get the name of the class with lowercase for the first letter
        if name=='' or name is None:
            if type is not None:
                name = type[:1].lower() + type[1:]
        SourceModelElement.__init__(
            self,
            model=association.model,
            name=name,
            astNode=astNode,
            lineNo=lineNo, description=description)
        self.association = association
        self.association.roleNamed[name] = self
        self.cardinalityMin = cardMin
        self.cardinalityMax = cardMax
        self.type = type        # string to be resolved in Class
        #type:
        self.isOrdered = isOrdered

        # (str,str) to be resolved in (str,SimpleType)
        self.qualifiers = qualifiers
        self.subsets = subsets
        self.isUnion = isUnion
        self.expression = expression

    @property
    def label(self):
        return '%s.%s' % (self.association.label, self.name)

    @property
    def cardinalityLabel(self):
        if self.cardinalityMin is None and self.cardinalityMax is None:
            return None
        if self.cardinalityMin == self.cardinalityMax:
            return str(self.cardinalityMin)
        if self.cardinalityMin==0 and self.cardinalityMax is None:
            return '*'
        return ('%s..%s' %(
            str(self.cardinalityMin),
            '*' if self.cardinalityMax is None else str(self.cardinalityMax)

        ))

    @property
    def opposite(self):
        if self.association.isNAry:
            raise ValueError(
                '%s "opposite" is not available for %s n-ary association. Try "opposites"' % (
                    self.name,
                    self.association.name
                ))
        rs = self.association.roles
        return rs[1] if self is rs[0] else rs[0]

    @property
    def opposites(self):
        rs = list(self.association.roles)
        rs.remove(self)
        return rs

    @property
    def isOne(self):
        return self.cardinalityMax == 1

    @property
    def isMany(self):
        return self.cardinalityMax is None or self.cardinalityMax >= 2

    @property
    def isTarget(self):
        return (
            self.association.isBinary
            and self.association.roles[1] == self
        )

    @property
    def isSource(self):
        return (
            self.association.isBinary
            and self.association.roles[0] == self
        )

    def __str__(self):
        return '%s::%s' % (self.association.name, self.name)


class AssociationClass(Class, Association):
    """
    Association classes.
    """
    def __init__(self,
                 name, model, isAbstract=False, superclasses=(),
                 package=None,
                 lineNo=None, description=None, astNode=None):
        # Use multi-inheritance to initialize the association class
        Class.__init__(self,
            name=name,
            model=model,
            isAbstract=isAbstract,
            superclasses=superclasses,
            package=package,
            lineNo=lineNo,
            description=description,
            astNode=astNode)
        Association.__init__(self,
            name=name,
            model=model,
            kind='associationclass',
            package=package,
            lineNo=lineNo,
            description=description, astNode=astNode)
        # But register the association class apart and only once, to avoid
        # confusion and the duplicate in the associations and classes lists
        del self.model.classNamed[name]
        del self.model.associationNamed[name]
        self.model.associationClassNamed[name] = self


METAMODEL = Metamodel(
    id='cl',
    label='class',
    extension='.cls',
    modelClass=ClassModel
)

MetamodelDependency(
    sourceId='cl',
    targetId='gl',
    optional=True,
    multiple=True,
)

# http://pythex.org
# TODO
#   (self\.[\w.]+ |\w +::\w + |\$\w +\.\w + [\w.] * | \$\w +: \w +)
# model

# class ExpressionPath(object):
#     """
#     Expression paths.
#     """
#     def __init__(self, startClass, pathString):
#         self.pathString = pathString
#         self.startClass = startClass
#         self.elements = self._evaluate(startClass, pathString.split('.'))
#
#
#     def _evaluate(self, current, names):
#         return NotImplementedError() # TODO


