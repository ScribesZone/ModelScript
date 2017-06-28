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
        self.enumerations = collections.OrderedDict()

        #: Map of classes, indexed by name.
        self.classes = collections.OrderedDict()  #indexed by name

        #: Map of associations, indexed by name.
        self.associations = collections.OrderedDict()  #indexed by name

        #: Map of association classes, indexed by name.
        self.associationClasses = collections.OrderedDict()  #indexed by name

        #: Map of operations, indexed by operation full signatures.
        #: e.g. 'Person::raiseSalary(rate : Real) : Real
        #: This is useful for pre/post condition lookup
        self.operations = collections.OrderedDict()  #indexed by full signature

        #: List of invariants.
        #: Invariants are not indexed due to construction order.
        #: The invariant are properties of classes and this is the normal
        #: way to access them (just like attributes for instance)
        self.invariants = []

        self.operationConditions = []

        #: Map of basic types. Indexed by type names/
        #: populated during the resolution phase
        self.basicTypes = collections.OrderedDict()


    def findAssociationOrAssociationClass(self, name):
        log.debug('findAssociationOrAssociationClass:%s', name)
        if name in self.associations:
            return self.associations[name]
        elif name in self.associationClasses:
            return self.associationClasses[name]
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
        if roleName in a.roles:
            return a.roles[roleName]
        else:
            raise Exception('ERROR - No "%s" role on association(class) %s' %
                            (roleName, associationOrAssociationClassName)  )


    def findClassOrAssociationClass(self, name):
        if name in self.classes:
            return self.classes[name]
        elif name in self.associationClasses:
            return self.associationClasses[name]
        else:
            raise Exception('ERROR - %s : No class or association class'
                            % name)

    def findInvariant(self, classOrAssociationClassName, invariantName):
        c = self.findClassOrAssociationClass(
                    classOrAssociationClassName)
        if invariantName in c.invariants:
            return c.invariants[invariantName]
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
            ('enumerations'         ,self.enumerations.keys()),
            ('classes'              ,self.classes.keys()),
            ('associations'         ,self.associations.keys()),
            ('association classes'  ,self.associationClasses.keys()),
            ('operations'           ,self.operations.keys()),
            ('invariants'           ,[i.name for i in self.invariants]),
            ('operation conditions' ,[i.name for i in self.operationConditions]),
            ('basic types'          ,self.basicTypes.keys()),
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
        self.model.enumerations[name] = self
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
        self.model.classes[name] = self
        self.isAbstract = isAbstract
        self.superclasses = superclasses  # strings resolved as classes
        self.attributes = collections.OrderedDict()
        self.operations = collections.OrderedDict()
        self.invariants = collections.OrderedDict()   # after resolution



class Attribute(SourceElement):
    """
    Attributes.
    """
    def __init__(self, name, class_, code=None, type=None):
        super(Attribute, self).__init__(name, code=code)
        self.class_ = class_
        self.class_.attributes[name] = self
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
        self.class_.operations[name] = self
        self.signature = signature
        self.full_signature = '%s::%s' % (class_.name, self.signature)
        self.model.operations[self.full_signature] = self
        # self.parameters = parameters
        # self.return_type = return_type
        self.expression = expression

        self.conditions = collections.OrderedDict()




class OperationCondition(TopLevelElement):
    """
    Operation conditions (precondition or postcondition).
    """
    __metaclass__ = abc.ABCMeta
    def __init__(self, name, model, operation, expression, code=None ):
        super(OperationCondition, self).__init__(name, model, code=code)
        self.model.operationConditions.append(self)
        operation.conditions[name] = self
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
        self.model.associations[name] = self
        self.kind = kind
        self.roles = collections.OrderedDict() # indexed by name
        self.arity = 0   # to be set
        self.isBinary = None # to be set



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
        self.association.roles[name] = self
        self.cardinalityMin = cardMin
        self.cardinalityMax = cardMax
        self.type = type        # string to be resolved in Class
        self.isOrdered = isOrdered

        # (str,str) to be resolved in (str,SimpleType)
        self.qualifiers = qualifiers
        self.subsets = subsets
        self.isUnion = isUnion
        self.expression = expression
        self.opposite = None   # set for binary association only

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
        del self.model.classes[name]
        del self.model.associations[name]
        self.model.associationClasses[name] = self


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


