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
    def __init__(self, name, code=None, lineNo=None, docComment=None, eolComment=None):
        self.name = name
        self.source = code
        self.lineNo = lineNo
        self.docComment = docComment
        self.eolComment = eolComment



class Model(SourceElement):
    """
    Class model.
    """
    def __init__(self, name, code=None, lineNo=None, docComment=None, eolComment=None):
        super(Model, self).__init__(name, code, lineNo, docComment, eolComment)
        self.isResolved = False

        #: Map of enumerations, indexed by name.
        self.enumerationNamed = collections.OrderedDict()

        #: Map of classes, indexed by name.
        self.classNamed = collections.OrderedDict()  #indexed by name

        #: Map of associations, indexed by name.
        self.associationNamed = collections.OrderedDict()  #indexed by name

        #: Map of association classes, indexed by name.
        self.associationClassNamed = collections.OrderedDict()  #indexed by name

        # #: Map of operations, indexed by operation full signatures.
        # #: e.g. 'Person::raiseSalary(rate : Real) : Real
        self.operationWithFullSignature = collections.OrderedDict()  #indexed by full signature

        #: List of all conditions (inv/pre/post).
        #  Both those that are declared within a class
        #  or those declared with a context at top level.
        #  Used for resolution.
        self._conditions = []

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

    @property
    def basicTypes(self):
        return self.basicTypeNamed.values()

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
            ('operations'           ,self.operationWithFullSignature.keys()),
            # ('invariants'           ,[i.name for i in self.invariants]),  FIXME: should be replaced
            ('basic types'          ,self.basicTypeNamed.keys()),
        ]
        total = 0
        lines = [ 'model '+self.name ]
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

    def __init__(self, name, model, code=None, literals=(), lineNo=None, docComment=None, eolComment=None):
        super(Enumeration, self).__init__(name, model, code, lineNo=lineNo, docComment=docComment, eolComment=eolComment)
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
    def __init__(self, name, model, isAbstract=False, superclasses=(),
                 lineNo=None, docComment=None, eolComment=None):
        super(Class, self).__init__(
            name, model,
            lineNo=lineNo, docComment=docComment, eolComment=eolComment)
        self.model.classNamed[name] = self
        self.isAbstract = isAbstract
        self.superclasses = superclasses  # strings resolved as classes
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
    def operations(self):
        return self.operationWithSignature.values()\

    @property
    def invariants(self):
        return self.invariantNamed.values()


class Attribute(SourceElement):
    """
    Attributes.
    """
    def __init__(self, name, class_, code=None, type=None,
                 isDerived=False, isInit=False, expression=None,
                 lineNo=None, docComment=None, eolComment=None):
        super(Attribute, self).__init__(
            name, code=code,
            lineNo=lineNo, docComment=docComment, eolComment=eolComment)
        self.class_ = class_
        self.class_.attributeNamed[name] = self
        self.type = type # string resolved as SimpleType
        self.isDerived = isDerived
        self.isInit = isInit
        self.expression = expression



# class Parameter

class Operation(TopLevelElement):
    """
    Operations.
    """
    def __init__(self, name, model, class_, signature, code=None,
                 expression=None,
                 lineNo=None, docComment=None, eolComment=None):
        super(Operation, self).__init__(
            name, model, code,
            lineNo=lineNo, docComment=docComment, eolComment=eolComment)
        self.class_ = class_
        self.signature = signature
        self.class_.operationWithSignature[signature] = self
        self.full_signature = '%s::%s' % (class_.name, self.signature)
        self.model.operationWithFullSignature[self.full_signature] = self
        # self.parameters = parameters
        # self.return_type = return_type
        self.expression = expression
        # Anonymous pre/post are indexed with id like _pre2/_post6
        # but their name (in PreCondition/PostCondition) is always ''
        # This id is just used internaly
        self.conditionNamed = collections.OrderedDict()

    @property
    def conditions(self):
        return self.conditionNamed.values()


    @property
    def hasImplementation(self):
        return self.expression is not None


class Condition(TopLevelElement):
    """
    Invariant, precondition or postcondition
    """
    __metaclass__ = abc.ABCMeta
    def __init__(
            self, name, model, class_, expression, code=None,
            lineNo=None, docComment=None, eolComment=None):
        super(Condition, self).__init__(
            name, model, code=code,
            lineNo=lineNo, docComment=docComment, eolComment=eolComment)
        self.class_ = class_  # str resolved in Class  # could be null as some invariants are toplevel
        self.expression = expression
        # add it so that it can be resolved later
        self.model._conditions.append(self)


class OperationCondition(Condition):
    """
    Operation conditions (precondition or postcondition).
    """
    __metaclass__ = abc.ABCMeta
    def __init__(
            self, name, model, class_, operation, expression,
            code=None,   # FIXME: operation vould be unknowed
            lineNo=None, docComment=None, eolComment=None ):
        super(OperationCondition, self).__init__(
            name, model, class_=class_, expression=expression, code=code,
            lineNo=lineNo, docComment=docComment, eolComment=eolComment)
        self.operation=operation # the signature of the operation, then resolved as Operation
        # # store the condition in the operation
        # operation.conditionNamed[name] = self



class PreCondition(OperationCondition):
    """
    Preconditions.
    """
    def __init__(self,
                 name, model, class_, operation, expression, code=None,
                 lineNo=None, docComment=None, eolComment=None):
        super(PreCondition, self).__init__(
            name, model, class_=class_, operation=operation, expression=expression,
            code=code,
            lineNo=lineNo, docComment=docComment, eolComment=eolComment
        )



class PostCondition(OperationCondition):
    """
    Postconditions.
    """
    def __init__(self,
                 name, model, class_, operation, expression, code=None,
                 lineNo=None, docComment=None, eolComment=None):
        super(PostCondition, self).__init__(
            name, model, class_=class_, operation=operation, expression=expression,
            code=code,
            lineNo=lineNo, docComment=docComment, eolComment=eolComment)


class Invariant(Condition):
    """
    Invariants.
    """
    def __init__(self, name, model, expression, class_=None, code=None,
                 variable='self',
                 additionalVariables = (),
                 toplevelDefined=True,
                 isExistential=False,
                 lineNo=None, docComment=None, eolComment=None):
        super(Invariant, self).__init__(
            name, model, class_=class_, expression=expression, code=code,
            lineNo=lineNo, docComment=docComment, eolComment=eolComment)
        self.variable = variable
        self.additionalVariables = additionalVariables
        self.toplevelDefined=toplevelDefined,
        self.isExistential = isExistential

    @property
    def isModelInvariant(self):
        """
        Is the invariant defined on model, that is without any context
        """
        return self.class_ is None


    def __str__(self):
        return '%s::%s' % (self.class_.name, self.name)

    def __repr__(self):
        return 'INV(%s::%s)' % (self.class_.name, self.name)



class Association(TopLevelElement):
    """
    Associations.
    """
    def __init__(self,
                 name, model, kind=None,
                 lineNo=None, docComment=None, eolComment=None):
        # type: (str) -> None
        super(Association, self).__init__(
            name, model,
            lineNo=lineNo, docComment=docComment, eolComment=eolComment)
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



class Role(SourceElement):
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
        super(Role, self).__init__(
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




class AssociationClass(Class,Association):
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


