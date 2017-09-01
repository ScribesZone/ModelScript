# coding=utf-8

"""
Class metamodel.

The structure of this package is::

    ClassModel
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
    <>--* BasicType

    Association, Class
    <|--  AssociationClass

    TopLevelElement
    <|-- Enumeration

    SimpleType
    <|--  BasicType
    <|--  Enumeration

"""
from __future__ import print_function

import abc
import collections
import logging

from typing import Text, Optional, Union, Any, List, Dict

from modelscripts.metamodels.permissions import Resource
from modelscripts.sources.models import Model
from modelscripts.sources.sources import (
    SourceElement,
    SourceFile
)

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
    def __init__(self,
                 name=None,
                 source=None,
                 code=None,
                 lineNo=None,
                 docComment=None,
                 eolComment=None):
        #type: (Optional[Text], Optional[SourceFile], Any, int, Text, Text) -> None
        super(ClassModel, self).__init__(
            source=source, name=name, code=code,
            lineNo=lineNo, docComment=docComment, eolComment=eolComment)

        self._isResolved = False

        self.enumerationNamed = collections.OrderedDict() #type: Dict[Text, Enumeration]
        #: Map of enumerations, indexed by name.

        #: Map of basic types. Indexed by type names/
        #: populated during the resolution phase
        self.basicTypeNamed = collections.OrderedDict()  #type: Dict[Text, BasicType]

        self.classNamed = collections.OrderedDict()  #type: Dict[Text, Class]
        #: Map of classes (including association classes), indexed by name.
        #: Use regularClassNamed to get only classes

        self.associationNamed = collections.OrderedDict() #type: Dict[Text, Association]
        #: Map of associations (including association classes), indexed by name.
        #: Use regularClassNamed to get only classes

        #: Map of association classes, indexed by name.
        self.associationClassNamed = collections.OrderedDict()  #type: Dict[Text, Association]

        # #: Map of operations, indexed by operation full signatures.
        # #: e.g. 'Person::raiseSalary(rate : Real) : Real
        self.operationWithFullSignature = collections.OrderedDict()  #type: Dict[Text, Operation]

        #: List of all conditions (inv/pre/post).
        #  Both those that are declared within a class
        #  or those declared with a context at top level.
        #  Used for resolution.
        self._conditions = [] #type: List['Condition']



    @property
    def label(self):
        return self.name

    @property
    def enumerations(self):
        return self.enumerationNamed.values()

    @property
    def enumerationNames(self):
        return self.enumerationNamed.keys()

    @property
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

    @property
    def regularClasses(self):
        return [
            class_ for class_ in self.classes
            if type(class_) == Class
            ]

    @property
    def regularClassNames(self):
        return [class_.name for class_ in self.regularClasses]

    @property
    def associations(self):
        return self.associationNamed.values()

    @property
    def associationNames(self):
        return self.associationNamed.keys()

    @property
    def regularAssociations(self):
        return [
            association for association in self.associations
            if type(association) == Association
            ]

    @property
    def regularAssociationNames(self):
        return [a.name for a in self.regularAssociations]

    @property
    def associationClasses(self):
        return self.associationClassNamed.values()

    @property
    def associationClassNames(self):
        return self.associationClassNamed.keys()

    @property
    def simpleTypeNamed(self):
        _ = self.basicTypeNamed.copy()
        _.update(self.enumerationNamed)
        return _

    @property
    def simpleTypes(self):
        return self.simpleTypeNamed.values()

    @property
    def simpleTypeNames(self):
        return self.simpleTypeNamed.keys()



    @property
    def basicTypes(self):
        return self.basicTypeNamed.values()

    @property
    def basicTypeNames(self):
        return self.basicTypeNamed.keys()




    def findAssociationOrAssociationClass(self, name):
        # TODO: check this implementation
        # should be most probably changed into
        # associationNamed property
        log.debug('findAssociationOrAssociationClass:%s', name)
        if name in self.associationNamed:
            return self.associationNamed[name]
        elif name in self.associationClassNamed:
            return self.associationClassNamed[name]
        else:
            raise Exception('ERROR - %s : No association or association class'
                            % name )

    def findClassOrAssociationClass(self, name):
        #type: (Text) -> Union[Class, AssociationClass]
        # TODO: see findAssociationOrAssociationClass
        if name in self.classNamed:
            return self.classNamed[name]
        elif name in self.associationNamed:
            return self.associationNamed[name]
        else:
            raise Exception('ERROR - %s : No class or association class'
                            % name)

    def findRole(self, associationOrAssociationClassName, roleName):
        # TODO: see findAssociationOrAssociationClass
        # though there are two parmeters here
        log.debug('findRole: %s::%s',
                  associationOrAssociationClassName, roleName)
        a = self.findAssociationOrAssociationClass(
                    associationOrAssociationClassName)

        log.debug('findRole:  %s ',a)
        log.debug('findRole:  %s ',a.roles)
        if roleName in a.roleNamed:
            return a.roleNamed[roleName]
        else:
            raise Exception('ERROR - No "%s" role on association(class) %s' %
                            (roleName, associationOrAssociationClassName)  )




    def findInvariant(self, classOrAssociationClassName, invariantName):
        #type: (Text, Text) -> 'Invariant'
        c = self.findClassOrAssociationClass(
                    classOrAssociationClassName)
        if invariantName in c.invariantNamed:
            return c.invariantNamed[invariantName]
        else:
            raise Exception('ERROR - No "%s" invariant on class %s' %
                            (invariantName, classOrAssociationClassName))

    def __str__(self):
        # TODO: move this to printer
        def category_line(label,elems):
            n = len(list(elems))
            return '% 3d %s: %s' % (
                n,
                label.ljust(22),
                ','.join(elems)
            )
        categories = [
            ('enumerations', self.enumerationNames),
            ('regular classes', self.regularClassNames),
            ('regular associations', self.associationNames),
            ('association classes', self.associationClassNames),
            ('operations', self.operationWithFullSignature.keys()),
            # ('invariants'           ,[i.name for i in self.invariants]),  FIXME: should be replaced
            ('basic types', self.basicTypeNames),
        ]
        total = 0
        lines = [ 'class model '+self.name ]
        for (label, items) in categories:
            lines.append(category_line(label, items))
            total += len(list(items))
        lines.append('% 3d' % total)
        return  '\n'.join(lines)




class TopLevelElement(SourceElement):
    """
    Top level element.
    """
    __metaclass__ = abc.ABCMeta
    def __init__(self, name, model, code=None, lineNo=None, docComment=None, eolComment=None):
        super(TopLevelElement,self).__init__(name, code=code, lineNo=lineNo, docComment=docComment, eolComment=eolComment)
        self.model = model

    @property
    def label(self):
        return self.name


class Entity(Resource):
    __metaclass__ = abc.ABCMeta

class Member(Resource):
    __metaclass__ = abc.ABCMeta

class SimpleType(object):
    """
    Simple types.
    """
    __metaclass__ = abc.ABCMeta

    @property
    def label(self):
        return self.name



class BasicType(SimpleType):
    """
    Basic types such as integer.
    Basic types are not explicitly defined in the source
    file, but they are used after after symbol resolution.
    """
    # not in sources, but used created during symbol resolution
    type = 'BasicType'

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name



class Enumeration(TopLevelElement, SimpleType):
    """
    Enumerations.
    """
    type = 'Enumeration'

    def __init__(self, name, model, code=None, literals=(), lineNo=None, docComment=None, eolComment=None):
        super(Enumeration, self).__init__(name, model, code, lineNo=lineNo, docComment=docComment, eolComment=eolComment)
        self.model.enumerationNamed[name] = self
        self.literals = list(literals)

    #TODO check if the literals should be a object as well
    #it seems that this could help for model transformation

    def addLiteral(self, name):
        self.literals.append(name)

    def __repr__(self):
        return '%s(%s)' % (self.name, repr(self.literals))


class Class(TopLevelElement, Entity):
    """
    Classes.
    """
    def __init__(self, name, model, isAbstract=False, superclasses=(),
                 lineNo=None, docComment=None, eolComment=None):
        super(Class, self).__init__(
            name, model,
            lineNo=lineNo, docComment=docComment, eolComment=eolComment)
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


class Attribute(SourceElement, Member):
    """
    Attributes.
    """
    def __init__(self, name, class_, code=None, type=None,
                 isDerived=False, isInit=False, expression=None,
                 lineNo=None, docComment=None, eolComment=None):
        SourceElement.__init__(
            self,
            name, code=code,
            lineNo=lineNo, docComment=docComment, eolComment=eolComment)
        self.class_ = class_
        self.class_.attributeNamed[name] = self
        self.type = type # string resolved as SimpleType
        self.isDerived = isDerived
        self.isInit = isInit
        self.expression = expression

    @property
    def label(self):
        return '%s.%s' % (self.class_.label, self.name)

# class Parameter

class Operation(SourceElement, Member):
    """
    Operations.
    """
    def __init__(self, name,  class_, signature, code=None,
                 expression=None,
                 lineNo=None, docComment=None, eolComment=None):
        SourceElement.__init__(
            self,
            name, code,
            lineNo=lineNo, docComment=docComment, eolComment=eolComment)
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

    @property
    def conditions(self):
        return self.conditionNamed.values()

    def conditionNames(self):
        return self.conditionNamed.keys()


    @property
    def hasImplementation(self):
        return self.expression is not None




class Association(TopLevelElement, Entity):
    """
    Associations.
    """
    def __init__(self,
                 name, model, kind=None,
                 lineNo=None, docComment=None, eolComment=None):
        # type: (Text,ClassModel,Optional[Text],Optional[int],Optional[Text],Optional[Text]) -> None
        super(Association, self).__init__(
            name, model,
            lineNo=lineNo, docComment=docComment, eolComment=eolComment)
        self.model.associationNamed[name] = self
        self.kind = kind   # association|composition|aggregation|associationclass  # TODO:should associationclass be
        # there?
        self.roleNamed = collections.OrderedDict() # indexed by name

    @property
    def roles(self):
        return self.roleNamed.values()

    @property
    def roleNames(self):
        return self.roleNamed.values()

    @property
    def arity(self):
        return len(self.roles)

    @property
    def isBinary(self):
        return self.arity == 2

    @property
    def isNAry(self):
        return self.arity >= 3

    @property
    def sourceRole(self):
        if not self.isBinary:
            raise ValueError(
                '"sourceRole" is not defined on "%s" n-ary association' % (
                    self.name
                ))
        return self.roles[0]

    @property
    def targetRole(self):
        if not self.isBinary:
            raise ValueError(
                '"targetRole" is not defined on "%s" n-ary association' % (
                    self.name
                ))
        return self.roles[1]

    @property
    def isManyToMany(self):
        return (
            self.isBinary
            and self.roles[0].isMany
            and self.roles[1].isMany
        )

    @property
    def isOneToOne(self):
        return (
            self.isBinary
            and self.roles[0].isOne
            and self.roles[1].isOne
        )

    @property
    def isForwardOneToMany(self):
        return (
            self.isBinary
            and self.roles[0].isOne
            and self.roles[1].isMany
        )

    @property
    def isBackwardOneToMany(self):
        return (
            self.isBinary
            and self.roles[0].isMany
            and self.roles[1].isOne
        )

    @property
    def isOneToMany(self):
        return self.isForwardOneToMany or self.isBackwardOneToMany



class Role(SourceElement, Member):
    """
    Roles.
    """
    def __init__(self, name, association, code=None,
                 cardMin=None, cardMax=None, type=None, isOrdered=False,
                 qualifiers=None, subsets=None, isUnion=False,
                 expression=None,
                 lineNo=None, docComment=None, eolComment=None):

        # unamed role get the name of the class with lowercase for the first letter
        if name=='' or name is None:
            if type is not None:
                name = type[:1].lower() + type[1:]
        SourceElement.__init__(
            self,
            name, code=code,
            lineNo=lineNo, docComment=docComment, eolComment=eolComment)
        self.association = association
        self.association.roleNamed[name] = self
        self.cardinalityMin = cardMin
        self.cardinalityMax = cardMax
        self.type = type        # string to be resolved in Class
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
                 lineNo=None, docComment=None, eolComment=None):
        # Use multi-inheritance to initialize the association class
        Class.__init__(self,
                       name, model, isAbstract, superclasses,
                       lineNo=lineNo, docComment=docComment, eolComment=eolComment)
        Association.__init__(self,
                             name, model, 'associationclass',
                             lineNo=lineNo, docComment=docComment, eolComment=eolComment)
        # But register the association class apart and only once, to avoid
        # confusion and the duplicate in the associations and classes lists
        del self.model.classNamed[name]
        del self.model.associationNamed[name]
        self.model.associationClassNamed[name] = self









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


