import abc

from modelscript.megamodels.elements import SourceModelElement
from modelscript.megamodels.py import MAttribute, MComposition
from modelscript.metamodels.classes import (
    PackagableElement,
    Item)
from modelscript.base.exceptions import (
    MethodToBeDefined)

class SimpleType(PackagableElement, Item):
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
        PackagableElement.__init__(self,
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
    Built-in data types are not explicitly defined in the source
    file, but they are used after after symbol resolution.
    See "core" module.
    """
    # not in sources, but used created during symbol resolution
    type = 'DataType'

    def __init__(self,
                 model,
                 name,
                 superDataType=None,  # Not used yet
                 astNode=None,
                 package=None,
                 implementationClass=None,
                 isCore=False):
        super(DataType, self).__init__(
            model=model,
            name=name,
            astNode=astNode,
            package=package
        )
        self.superDataType=superDataType
        self.implementationClass=implementationClass
        self.model._dataTypeNamed[name]=self
        self.isCore=isCore

    def __repr__(self):
        return self.name


class AttributeType(object):

    def __init__(self,
                 simpleType,
                 isOptional=False,
                 isMultiple=False):
        self.simpleType=simpleType
        self.isOptional=isOptional
        self.isMultiple=isMultiple

    def accept(self, simpleValue):
        null_type=self.simpleType.model.dataType('NullType')
        valueType=simpleValue.type
        # print('KK'*10,
        #       str(simpleValue)+':'+ str(valueType),
        #       'with var',
        #       id(self.simpleType),
        #       self.simpleType.name,
        #       self.isOptional)
        return (
            (valueType==null_type and self.isOptional)
            or valueType==self.simpleType
        )

    @property
    def name(self):
        return self.simpleType.name


    def __str__(self):
        return (
              unicode(self.simpleType)
            + ('[0..1]' if self.isOptional else '')
        )


class UnspecifiedValue(object):
    """
    This value just represents that a slot has not specified.
    There is only one value.
    """
    def __str__(self):
        return '?'


UNSPECIFIED=UnspecifiedValue()


class SimpleValue(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractproperty
    def type(self):
        raise MethodToBeDefined( #raise:OK
            'property .type not implemented')

    @abc.abstractmethod
    def equals(self, simpleValue):
        raise MethodToBeDefined( #raise:OK
            'equals() not implemented')


class EnumerationValue(object):

    def __init__(self, literal):
        self.value=literal
        #type: EnumerationLiteral

    def __str__(self):
        return "%s.%s" % (
            self.value.enumeration.name,
            self.value.name)

    @property
    def type(self):
        return self.value.enumeration

    def equals(self, enumValue):
        return self.value==enumValue.value


class DataValue(SimpleValue):

    __metaclass__ = abc.ABCMeta

    def __init__(self, stringRepr, value, type):
        self.stringRepr=stringRepr
        self.value=value
        self._type=type

    @property
    def type(self):
        return self._type

    def __str__(self):
        return self.stringRepr

    def equals(self, enumValue):
        return self.value==enumValue.value

    @property
    def isCore(self):
        return False    # will be refined for core


class UserDefinedDataValue(DataValue):
    """
    Not used in practice so far.
    """

    def __init__(self, stringRepr, value, type):
        super(UserDefinedDataValue, self).__init__(
            stringRepr=stringRepr,
            value=value,
            type=type
        )


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
        self.model._enumerationNamed[name] = self
        self._literals=[]
        # Not sure to understand why this is not a Dict

    @MComposition('EnumerationLiteral[*] inv enumeration')
    def literals(self):
        return self._literals

    @property
    def literalNames(self):
        return [l.name for l in self.literals]

    def literal(self, name):
        # Not sure to understand why this is not a Dict
        for literal in self.literals:
            if literal.name==name:
                return literal
        else:
            return None

    def __str__(self):
        return self.name

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