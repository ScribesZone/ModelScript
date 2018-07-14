import abc
import collections

from modelscripts.megamodels.elements import SourceModelElement
from modelscripts.megamodels.py import MAttribute, MComposition
from modelscripts.metamodels.classes import PackagableElement, Entity, \
    Member


class Class(PackagableElement, Entity):
    """
    Classes.
    """

    __metaclass__ = abc.ABCMeta

    META_COMPOSITIONS = [
    #    'attributes', TODO: restore, raise an exception
        'operations',
        'invariants',
    ]

    def __init__(self, name, model,
                 isAbstract=False, superclasses=(),
                 package=None,
                 lineNo=None, description=None, astNode=None):
        super(Class, self).__init__(
            name=name,
            model=model,
            package=package,
            astNode=astNode,
            lineNo=lineNo,
            description=description)
        self.isAbstract = isAbstract
        self.superclasses = superclasses
        # strings resolved as classes

        self._ownedAttributeNamed = collections.OrderedDict()
        #type: List[Attribute]
        # List of attributes directly declared by the class.
        # No inherited attributes.
        # Will be filled by the parser fillModel

        self._inheritedAttributeNamed = None
        #type: Optional[List[Attribute]]
        # List of inherited attributes from all super class.
        # Computed by finalize.add_inherited_attributes
        # Before it is set to None

        # TODO: deal with operation and operation names
        # Signature looks like op(p1:X):Z
        self.operationNamed = collections.OrderedDict()

        # Anonymous invariants are indexed with id like _inv2
        # but their name (in Invariant) is always ''
        # This id is just used internaly
        self.invariantNamed = collections.OrderedDict()   # after resolution

        self._ownedOppositeRoles = []
        #type: List[Role]
        # defined by finalize.add_attached_roles_to_classes

        self._ownedPlayedRoles = []
        #type: List[Role]
        # defined by finalize.add_attached_roles_to_classes

        self.inheritanceCycles=None
        #type Optional[List[Class]]
        # The list of cycle starting and going to the current class.
        # This attribute is set during finalize

    @property
    def ownedAttributes(self):
        return self._ownedAttributeNamed.values()

    def ownedAttribute(self, name):
        if name in self._ownedAttributeNamed:
            return self._ownedAttributeNamed[name]
        else:
            return None

    @property
    def ownedAttributeNames(self):
        return self._ownedAttributeNamed.keys()

    @property
    def inheritedAttributes(self):
        if self._inheritedAttributeNamed is None:
            # This should happend just when there is a cycle
            # The [] value is to ensure that the model is still
            # usable. Instead of raising an exception it is best
            # to ignore attribute. This prevent exception when
            # using the model. Just like the printer. It is not
            # nice to require client to check which attributes
            # are defined or note.
            return []
        return self._inheritedAttributeNamed.values()

    def inheritedAttribute(self, name):
        if self._inheritedAttributeNamed is None:
            # see inheritedAttributes
            return []
        if name in self._inheritedAttributeNamed:
            return self._inheritedAttributeNamed[name]
        else:
            return None

    @property
    def inheritedAttributeNames(self):
        if self._inheritedAttributeNamed is None:
            # see inheritedAttributes
            return []
        return self._inheritedAttributeNamed.keys()

    @property
    def attributes(self):
        return self.ownedAttributes+self.inheritedAttributes

    def attribute(self, name):
        oa=self.ownedAttribute(name)
        if oa is not None:
            return oa
        else:
            return self.inheritedAttribute(name)

    @property
    def attributeNames(self):
        return self.ownedAttributeNames+self.inheritedAttributeNames

    @property
    def operations(self):
        return self.operationNamed.values()

    @property
    def operationNames(self):
        return self.invariantNamed.keys()

    @property
    def invariants(self):
        return self.invariantNamed.values()

    @property
    def invariantNames(self):
        return self.invariantNamed.keys()

    @property
    def ownedOppositeRoles(self):
        return self._ownedOppositeRoles

    @property
    def ownedPlayedRoles(self):
        return self._ownedPlayedRoles

    @property
    def names(self):
        return (
            self.attributeNames
            +self.operationNames
            +self.invariantNames)

    @property
    def idPrint(self):
        #type: () -> List[Attribute]
        return [
            a for a in self.attributes
                if a.isId ]

    @abc.abstractmethod
    def isPlainClass(self):
        # This method is not really useful as isinstance can be used.
        # It is just used to prevent creating object of this class
        # (using ABCMeta is not enough to prevent this).
        raise NotImplementedError()

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<class %s>' % self.name


class PlainClass(Class):
    """
    PlainClasses, that is, classes that are not association class.
    """
    def __init__(self, name, model,
                 isAbstract=False, superclasses=(),
                 package=None,
                 lineNo=None, description=None, astNode=None):
        super(PlainClass, self).__init__(
            name=name,
            model=model,
            isAbstract=isAbstract,
            superclasses=superclasses,
            package=package,
            astNode=astNode,
            lineNo=lineNo,
            description=description)

        self.model._plainClassNamed[name] = self

    def isPlainClass(self):
        return True


class Attribute(SourceModelElement, Member):
    """
    Attributes.
    """

    def __init__(self, name, class_, type=None,
                 description=None,
                 visibility='public',
                 isDerived=False,
                 isOptional=False,
                 tags=(),
                 stereotypes=(),
                 isInit=False, expression=None,
                 lineNo=None, astNode=None):
        SourceModelElement.__init__(
            self,
            model=class_.model,
            name=name,
            astNode=astNode,
            lineNo=lineNo, description=description)
        self.class_ = class_
        self.class_._ownedAttributeNamed[name] = self
        self.type = type # string later resolved as SimpleType
        self._isDerived = isDerived
        self.visibility=visibility
        self.isOptional = isOptional
        self.isInit = isInit  # ?
        self.expression = expression
        self.tags=tags
        self.stereotypes=stereotypes

    @MAttribute('Boolean')
    def isDerived(self):
        return self._isDerived

    @isDerived.setter
    def isDerived(self,isDerived):
        self._isDerived=isDerived

    @property
    def label(self):
        return '%s.%s' % (self.class_.label, self.name)

    @property
    def isId(self):
        return 'id' in self.tags

    @property
    def isReadOnly(self):
        return 'readOnly' in self.tags

    @property
    def isClass(self):
        return 'isClass' in self.tags


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