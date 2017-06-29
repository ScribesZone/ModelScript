# coding=utf-8

"""
Partial AST for USE OCL Model. The elements in this module are generated
by the "parser" module.
"""

import logging

# logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('test.' + __name__)

import collections
import abc

class SourceElement(object):
    """
    Element of a source file.
    """
    __metaclass__ = abc.ABCMeta
    def __init__(self, name, code=None):
        self.name = name
        self.source = code



class Model(SourceElement):
    """
    Class model.
    """
    def __init__(self, name, code=None):
        super(Model,self).__init__(name,code)
        self.isResolved = False

        #: Map of enumerations, indexed by name.
        self.enumerationNamed = collections.OrderedDict()

        #: Map of classes, indexed by name.
        self.classNamed = collections.OrderedDict()  #indexed by name

        #: Map of associations, indexed by name.
        self.associationNamed = collections.OrderedDict()  #indexed by name

        #: Map of association classes, indexed by name.
        self.associationClassNamed = collections.OrderedDict()  #indexed by name

        #: Map of operations, indexed by operation full signatures.
        #: e.g. 'Person::raiseSalary(rate : Real) : Real
        #: This is useful for pre/post condition lookup
        self.operationWithSignature = collections.OrderedDict()  #indexed by full signature

        #: List of invariants.
        #: Invariants are not indexed due to construction order.
        #: The invariant are properties of classes and this is the normal
        #: way to access them (just like attributes for instance)
        self.invariants = []

        self.operationConditions = []

        #: Map of basic types. Indexed by type names/
        #: populated during the resolution phase
        self.basicTypeNamed = collections.OrderedDict()

    @property
    def enumerations(self):
        return self.enumerationNamed.values()

    @property
    def classes(self):
        return self.classNamed.values()

    @property
    def associations(self):
        return self.associationNamed.values()

    @property
    def associationClasses(self):
        return self.associationClassNamed.values()

    def findAssociationOrAssociationClass(self, name):
        log.debug('findAssociationOrAssociationClass:%s', name)
        if name in self.associationNamed:
            return self.associationNamed[name]
        elif name in self.associationClassNamed:
            return self.associationClassNamed[name]
        else:
            raise Exception('ERROR - %s : No association or association class'
                            % name )


    def findRole(self, associationOrAssociationClassName, roleName):
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


    def findClassOrAssociationClass(self, name):
        if name in self.classNamed:
            return self.classNamed[name]
        elif name in self.associationNamed:
            return self.associationNamed[name]
        else:
            raise Exception('ERROR - %s : No class or association class'
                            % name)

    def findInvariant(self, classOrAssociationClassName, invariantName):
        c = self.findClassOrAssociationClass(
                    classOrAssociationClassName)
        if invariantName in c.invariantNamed:
            return c.invariantNamed[invariantName]
        else:
            raise Exception('ERROR - No "%s" invariant on class %s' %
                            (invariantName, classOrAssociationClassName))

    def __str__(self):

        def category_line(label,elems):
            n = len(list(elems))
            return '% 3d %s: %s' % (
                n,
                label.ljust(22),
                ','.join(elems)
            )
        categories = [
            ('enumerations'         ,self.enumerationNamed.keys()),
            ('classes'              ,self.classNamed.keys()),
            ('associations'         ,self.associationNamed.keys()),
            ('association classes'  ,self.associationClassNamed.keys()),
            ('operations'           ,self.operationWithSignature.keys()),
            ('invariants'           ,[i.name for i in self.invariants]),
            ('operation conditions' ,[i.name for i in self.operationConditions]),
            ('basic types'          ,self.basicTypeNamed.keys()),
        ]
        total = 0
        lines = [ 'model '+self.name ]
        for (label, items) in categories:
            lines.append(category_line(label, items))
            total += len(list(items))
        lines.append('% 3d' % total)

        return  '\n'.join(lines)



            # + 'operation conditions:' \
            # + ','.join([i.name for i in self.operationConditions]) + '\n' \
            # + 'basic types         :' \
            # + ','.join(self.basicTypes.keys()) + '\n'



class TopLevelElement(SourceElement):
    """
    Top level element.
    """
    __metaclass__ = abc.ABCMeta
    def __init__(self, name, model, code=None):
        super(TopLevelElement,self).__init__(name,code=code)
        self.model = model



class SimpleType(object):
    """
    Simple types.
    """
    __metaclass__ = abc.ABCMeta



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


class Enumeration(TopLevelElement,SimpleType):
    """
    Enumerations.
    """
    type = 'Enumeration'

    def __init__(self, name, model, code=None, literals=()):
        super(Enumeration, self).__init__(name, model, code)
        self.model.enumerationNamed[name] = self
        self.literals = list(literals)


    def addLiteral(self, name):
        self.literals.append(name)

    def __repr__(self):
        return '%s(%s)' % (self.name,repr(self.literals))



class Class(TopLevelElement):
    """
    Classes.
    """
    def __init__(self, name, model, isAbstract=False, superclasses=()):
        super(Class, self).__init__(name, model)
        self.model.classNamed[name] = self
        self.isAbstract = isAbstract
        self.superclasses = superclasses  # strings resolved as classes
        self.attributeNamed = collections.OrderedDict()
        self.operationNamed = collections.OrderedDict()
        self.invariantNamed = collections.OrderedDict()   # after resolution
        self.outgoingRoles = [] # after resolution
        self.incomingRoles = [] # after resolution

    @property
    def attributes(self):
        return self.attributeNamed.values()

    @property
    def operations(self):
        return self.operationNamed.values()\

    @property
    def invariants(self):
        return self.invariantNamed.values()



class Attribute(SourceElement):
    """
    Attributes.
    """
    def __init__(self, name, class_, code=None, type=None):
        super(Attribute, self).__init__(name, code=code)
        self.class_ = class_
        self.class_.attributeNamed[name] = self
        self.type = type # string resolved as SimpleType



# class Parameter


class Operation(TopLevelElement):
    """
    Operations.
    """
    def __init__(self, name, model, class_, signature, code=None,
                 expression=None):
        super(Operation, self).__init__(name, model, code)
        self.class_ = class_
        self.class_.operationNamed[name] = self
        self.signature = signature
        self.full_signature = '%s::%s' % (class_.name, self.signature)
        self.model.operationWithSignature[self.full_signature] = self
        # self.parameters = parameters
        # self.return_type = return_type
        self.expression = expression
        self.conditionNamed = collections.OrderedDict()

    @property
    def conditions(self):
        return self.conditionNamed.values()



class OperationCondition(TopLevelElement):
    """
    Operation conditions (precondition or postcondition).
    """
    __metaclass__ = abc.ABCMeta
    def __init__(self, name, model, operation, expression, code=None ):
        super(OperationCondition, self).__init__(name, model, code=code)
        self.model.operationConditions.append(self)
        operation.conditionNamed[name] = self
        self.expression = expression



class PreCondition(OperationCondition):
    """
    Preconditions.
    """
    def __init__(self, name, model, operation, expression, code=None ):
        super(PreCondition, self).__init__(
            name, model, operation, expression, code=code)



class PostCondition(OperationCondition):
    """
    Postconditions.
    """
    def __init__(self, name, model, operation, expression, code=None):
        super(PostCondition, self).__init__(
            name, model, operation, expression, code=code)



class Invariant(TopLevelElement):
    """
    Invariants.
    """
    def __init__(self, name, model, class_=None, code=None,
                 variable='self', expression=None,
                 additionalVariables = (),
                 isExistential=False):
        super(Invariant, self).__init__(name, model, code=code)
        self.model.invariants.append(self)
        self.class_ = class_  # str resolved in Class
        self.expression = expression
        self.variable = variable
        self.additionalVariables = additionalVariables
        self.isExistential = isExistential


    def __str__(self):
        return '%s::%s' % (self.class_.name, self.name)

    def __repr__(self):
        return 'INV(%s::%s)' % (self.class_.name, self.name)



class Association(TopLevelElement):
    """
    Associations.
    """
    def __init__(self, name, model, kind=None):
        # type: (str) -> None
        super(Association, self).__init__(name,model)
        self.model.associationNamed[name] = self
        self.kind = kind
        self.roleNamed = collections.OrderedDict() # indexed by name

    @property
    def roles(self):
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

class Role(SourceElement):
    """
    Roles.
    """
    def __init__(self, name, association, code=None,
                 cardMin=None, cardMax=None, type=None, isOrdered=False,
                 qualifiers=None, subsets=None, isUnion=False,
                 expression=None):

        # unamed role get the name of the class with lowercase for the first letter
        if name=='' or name is None:
            if type is not None:
                name = type[:1].lower() + type[1:]
        super(Role, self).__init__(name, code=code)
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

    def __str__(self):
        return '%s::%s' % (self.association.name, self.name)

class AssociationClass(Class,Association):
    """
    Association classes.
    """
    def __init__(self, name, model, isAbstract=False, superclasses=()):
        # Use multi-inheritance to initialize the association class
        Class.__init__(self, name, model, isAbstract, superclasses)
        Association.__init__(self, name, model, 'associationclass' )
        # But register the association class apart and only once, to avoid
        # confusion and the duplicate in the associations and classes lists
        del self.model.classNamed[name]
        del self.model.associationNamed[name]
        self.model.associationClassNamed[name] = self


# http://pythex.org
# TODO
#   (self\.[\w.]+ |\w +::\w + |\$\w +\.\w + [\w.] * | \$\w +: \w +)
# model

class ExpressionPath(object):
    """
    Expression paths.
    """
    def __init__(self, startClass, pathString):
        self.pathString = pathString
        self.startClass = startClass
        self.elements = self._evaluate(startClass, pathString.split('.'))


    def _evaluate(self, current, names):
        return NotImplementedError() # TODO


