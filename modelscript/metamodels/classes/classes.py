# coding=utf-8
"""Class related metaclasses.
This module defines:
* Class,
* PlainClass,
* Attribute,
"""

from typing_extensions import Literal
from typing import List, Optional, Dict, Union, Any
import abc
import collections

from modelscript.megamodels.elements import SourceModelElement
from modelscript.megamodels.models import Placeholder
from modelscript.megamodels.py import MAttribute, MComposition
from modelscript.metamodels.classes import (
    PackagableElement,
    Entity,
    Member)
from modelscript.metamodels.classes.associations import (
    Role)
from modelscript.base.exceptions import (
    MethodToBeDefined)

Later = Optional

__all__ = (
    'Class',
    'PlainClass',
    'Attribute')


class Class(PackagableElement, Entity, metaclass=abc.ABCMeta):
    """ Classes.
    """

    META_COMPOSITIONS = [
    #    'attributes', TODO:3 restore, raise an exception
    ]

    isAbstract: bool

    superclasses: List[Union[Placeholder, 'Class']]  # later: List['Class']
    """Names of superclasses later resolved as classes."""

    subclassed: List['Class']
    """Subclasses"""

    _ownedAttributeNamed: Dict[str, 'Attribute']
    """ Attributes directly declared by the class.
    No inherited attributes. Attributed indexed by name.
    """

    _ownedOppositeRoleNamed: Dict[str, Role]
    # defined by finalize.add_attached_roles_to_classes
    # The opposite role a index by their name.
    # This is possible because all opposite roles
    # have a different name, which is not the case for
    # played roles.

    _ownedPlayedRoles: List[Role]
    # Defined by finalize.add_attached_roles_to_classes.
    # A list because various played role can have the same name.

    # -------- inherited part ----------------------------------

    inheritanceCycles: Later[List[List['Class']]]
    """The list of cycles starting and going to the current class.
    For instance [[A,B,A], [A,A]]
    """

    _inheritedAttributeNamed: Later[Dict[str, 'Attribute']]
    """Dict of inherited attributes from all super classes.
    Inherited attributes are stored by names.
    """

    _inheritedOppositeRoleNamed: Optional[Dict[str, Role]]
    """Dict of inherited opposite roles from all super classes.
    Inherited role are stored by names.
    This is ok since all opposite roles must have a
    different name. This contrasts with played role
    that can have arbitrary (duplicated) names."""

    _inheritedPlayedRoles: Optional[List[Role]]
    """List of inherited played roles from all super classes.
    This is a list rather that a dict since various
    played role can have the same name."""

    def __init__(self,
                 name: str,
                 model,
                 isAbstract: bool = False,
                 superclasses: List[Placeholder] = (),
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

        self.subclasses = []
        # Subclasses are [] during fillModel then set during resolve()

        self._ownedAttributeNamed = collections.OrderedDict()
        # Will be filled by the parser fillModel"""

        self._ownedOppositeRoleNamed = collections.OrderedDict()
        self._ownedPlayedRoles = []

        # -------- inherited part ----------------------------------

        self.inheritanceCycles = None
        # This attribute is set during finalize

        self._inheritedAttributeNamed = None
        # Computed by finalize.add_inherited_attributes
        # Before this it is set to None. This serves as
        # a marker to indicates whether add_inherited_attributes
        # has been run or not on this class.

        self._inheritedOppositeRoleNamed = None
        # This attribute is Computed by finalize.add_inherited_roles
        # Before this it is set to None. This serves as
        # a marker to indicates whether add_inherited_roles
        # has been run or not on this class.

        self._inheritedPlayedRoles = None
        # Computed by finalize.add_inherited_roles
        # Before this it is set to None. This serves as
        # a marker to indicates whether add_inherited_roles
        # has been run or not on this class.

    # -----------------------------------------------------------------
    #   ownedAttributes
    # -----------------------------------------------------------------

    @property
    def ownedAttributes(self):
        return list(self._ownedAttributeNamed.values())

    def ownedAttribute(self, name):
        if name in self._ownedAttributeNamed:
            return self._ownedAttributeNamed[name]
        else:
            return None

    @property
    def ownedAttributeNames(self):
        return list(self._ownedAttributeNamed.keys())

    # -----------------------------------------------------------------
    #   inheritedAttributes
    # -----------------------------------------------------------------

    @property
    def inheritedAttributes(self):
        if self._inheritedAttributeNamed is None:
            # This should happened just when a cycle has been detected.
            # In this case a fatal issue has been raised, which is ok,
            # but the rest of finalize code didn't execute properly.
            # The [] value here is to ensure that the model is still
            # usable and that the cycle detection fail gracefully.
            # Instead of raising an exception in this method it is best
            # to ignore inherited attributes. This prevent a new
            # exception when using the model.
            # Just like the printer. It is not
            # nice to require client to check which attributes
            # are defined or not.
            return []
        return list(self._inheritedAttributeNamed.values())

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
        return list(self._inheritedAttributeNamed.keys())

    # -----------------------------------------------------------------
    #   attributes
    # -----------------------------------------------------------------

    @property
    def attributes(self):
        return self.ownedAttributes+self.inheritedAttributes

    def attribute(self, name):
        oa = self.ownedAttribute(name)
        if oa is not None:
            return oa
        else:
            return self.inheritedAttribute(name)

    @property
    def attributeNames(self):
        return self.ownedAttributeNames+self.inheritedAttributeNames

    # -----------------------------------------------------------------
    #   ownedOppositeRoles
    # -----------------------------------------------------------------

    @property
    def ownedOppositeRoles(self):
        return list(self._ownedOppositeRoleNamed.values())

    def ownedOppositeRole(self, name):
        if name in self._ownedOppositeRoleNamed:
            return self._ownedOppositeRoleNamed[name]
        else:
            return None

    @property
    def ownedOppositeRoleNames(self):
        return list(self._ownedOppositeRoleNamed.keys())

    # -----------------------------------------------------------------
    #   inheritedOppositeRoles
    # -----------------------------------------------------------------

    @property
    def inheritedOppositeRoles(self):
        if self._inheritedOppositeRoleNamed is None:
            # When there is no cycle, the content of the attribute
            # is a dict. Otherwise it will remain to None.
            # If a cycle is detected a fatal issue is raised, which is ok,
            # but the rest of finalize code didn't execute properly.
            # The [] value here is to ensure that the model is still
            # usable and that the cycle detection fail gracefully.
            # Instead of raising an exception in this method it is best
            # to ignore inherited attributes. This prevent a new
            # exception when using the model.
            # Just like the printer. It is not
            # nice to require client to check which attributes
            # are defined or not.
            return []
        return list(self._inheritedAttributeNamed.values())

    def inheritedOppositeRole(self, name):
        if self._inheritedOppositeRoleNamed is None:
            # see inheritedOppositeRoles
            return None
        if name in self._inheritedOppositeRoleNamed:
            return self._inheritedOppositeRoleNamed[name]
        else:
            return None

    @property
    def inheritedOppositeRoleNames(self):
        if self._inheritedOppositeRoleNamed is None:
            # see inheritedAttributes
            return []
        return list(self._inheritedOppositeRoleNamed.keys())

    # -----------------------------------------------------------------
    #   oppositeRoles
    # -----------------------------------------------------------------

    @property
    def oppositeRoles(self):
        return self.ownedOppositeRoles+self.inheritedOppositeRoles

    def oppositeRole(self, name):
        oor = self.ownedOppositeRole(name)
        if oor is not None:
            return oor
        else:
            return self.inheritedOppositeRole(name)

    @property
    def oppositeRoleNames(self):
        return self.ownedOppositeRoleNames\
               + self.inheritedOppositeRoleNames

    # -----------------------------------------------------------------
    #   ownedPlayedRoles
    # -----------------------------------------------------------------

    @property
    def ownedPlayedRoles(self):
        return list(self._ownedPlayedRoles)

    # There is no method ownedPlayedRole(self, name) because the
    # ownedPlayedRoles are not indexed by name since various roles
    # may have the same name.

    @property
    def ownedPlayedRoleNames(self):
        return [
            r.name for r in self._ownedPlayedRoles]

    # -----------------------------------------------------------------
    #   inheritedPlayedRoles
    # -----------------------------------------------------------------

    @property
    def inheritedPlayedRoles(self):
        if self._inheritedOppositeRoleNamed is None:
            # When there is no cycle, the content of the attribute
            # is a dict. Otherwise it will remain to None.
            # If a cycle is detected a fatal issue is raised, which is ok,
            # but the rest of finalize code didn't execute properly.
            # The [] value here is to ensure that the model is still
            # usable and that the cycle detection fail gracefully.
            # Instead of raising an exception in this method it is best
            # to ignore inherited attributes. This prevent a new
            # exception when using the model.
            # Just like the printer. It is not
            # nice to require client to check which attributes
            # are defined or not.
            return []
        return list(self._inheritedPlayedRoles)

    @property
    def inheritedPlayedRoleNames(self):
        if self._inheritedOppositeRoleNamed is None:
            # see inheritedAttributes
            return []
        return list(self._inheritedPlayedRoles)

    # -----------------------------------------------------------------
    #   playedRoles
    # -----------------------------------------------------------------

    @property
    def playedRoles(self):
        return self.ownedPlayedRoles+self.inheritedPlayedRoles

    @property
    def playedRoleNames(self):
        return self.ownedPlayedRoleNames\
               + self.inheritedPlayedRoles

    # ------- misc ------------------------------------------------------

    @property
    def cycles(self) -> str:
        """
        A string describing the inheritance cycles starting from this
        class if any or None if there is no cycle.
        """
        if self.inheritanceCycles:
            return (
                ', '.join(
                    ('<'.join(c.name for c in cycle))
                    for cycle in self.inheritanceCycles))
        else:
            return None

    @property
    def names(self):
        return (
            self.attributeNames
            + self.invariantNames)

    @property
    def idPrint(self) -> List['Attribute']:
        """List of all {id} attributes.
        """
        return [
            a for a in self.attributes
            if a.isId]

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
    """ Attributes.
    """

    class_: 'Class'
    """Class of the attribute."""

    type: Union[str, 'AttributeType']
    """Type of the attribute (AttributeType). An AttributeType is
    a simple type plus optionality and multiplicity. 
    Something that could be like String[0..1] or String[*]."""

    isDerived: bool
    """Whether the attribute is derived or not."""

    visibility: Optional[
        Literal['public', 'private', 'protected', 'package']]
    """The visibility of the attribute."""

    isOptional: bool
    """Whether the attribute is optional or not.
    For instance x : String[0..1] is optional."""

    tags: List[str]
    """The list of tags associated with the attribute."""

    stereotypes: List[str]
    """The list of stereotypes associated with the attribute."""

    def __init__(self, name, class_,
                 type=None,
                 description=None,
                 visibility=None,
                 isDerived=False,
                 isOptional=False,
                 tags=(),
                 stereotypes=(),
                 lineNo=None, astNode=None):
        SourceModelElement.__init__(
            self,
            model=class_.model,
            name=name,
            astNode=astNode,
            lineNo=lineNo, description=description)
        self.class_ = class_
        self.class_._ownedAttributeNamed[name] = self
        self.type = type  # string later resolved as SimpleType
        self.isDerived = isDerived
        self.visibility = visibility
        self.isOptional = isOptional
        self.tags = tags
        self.stereotypes = stereotypes

    # @MAttribute('Boolean')
    # def isDerived(self):
    #     return self._isDerived
    #
    # @isDerived.setter
    # def isDerived(self,isDerived):
    #     self._isDerived = isDerived

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
