# coding=utf-8
"""Definition of associations.
Defines the following metaclasses:
* Association,
* PlainAssociation,
* Role.
"""

import abc
import collections
from typing import Optional, Text, Dict, Union, List
from typing_extensions import Literal

from modelscript.megamodels.elements import (
    SourceModelElement)
from modelscript.megamodels.py import (
    MAttribute,
    MReference)
from modelscript.metamodels.classes import (
    PackagableElement,
    Entity,
    Member)
from modelscript.base.exceptions import (
    UnexpectedCase,
    NoSuchFeature,
    MethodToBeDefined)

RolePosition = Literal['source', 'target']

__all__ = (
    'opposite',
    'Association',
    'PlainAssociation',
    'Role'
)


def opposite(rolePosition):
    if rolePosition == 'source':
        return 'target'
    elif rolePosition == 'target':
        return 'source'
    else:
        raise UnexpectedCase(  # raise:OK
            "Role position '%s' doesn't exists." % rolePosition)

AssociationKind = Literal[
    'association',
    'composition',
    'aggregation',
    'associationclass']

class Association(PackagableElement, Entity, metaclass=abc.ABCMeta):
    """ Associations.
    """

    META_COMPOSITIONS = [
        'roles',
    ]

    kind: AssociationKind
    """Association kind.
    association, composition, aggregation or associationclass
    """

    roleNamed: Dict[str, 'Role']
    """Roles of the association indexed by names. An association
    can't have twice the same name. Moreover the roles are ordered,
    which is the basis to make the difference between the source
    and the target for binary association."""

    def __init__(self,
                 name: str,
                 model: 'ClassModel',
                 kind: AssociationKind = 'association',
                 package: Optional['Package'] = None,
                 lineNo: Optional[int] = None,
                 description: Optional[str] = None,
                 astNode: Optional['extXNode'] = None)\
            -> None:
        super(Association, self).__init__(
            name=name,
            model=model,
            package=package,
            astNode=astNode,
            lineNo=lineNo, description=description)
        self.kind = kind
        self.roleNamed = collections.OrderedDict()  # indexed by name

    @property
    def roles(self):
        """The list of roles in their definition order. """
        return list(self.roleNamed.values())

    @property
    def roleNames(self):
        return list(self.roleNamed.keys())

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
        """For binary association only, the first role that was defined."""
        if not self.isBinary:
            raise NoSuchFeature(  # raise:OK
                '"sourceRole" is not defined on "%s" n-ary association' % (
                    self.name
                ))
        return self.roles[0]

    @MReference('Role')
    def targetRole(self):
        """For binary association only, the second role that was
        defined."""
        if not self.isBinary:
            raise NoSuchFeature(  # raise:OK
                '"targetRole" is not defined on "%s" n-ary association' % (
                    self.name
                ))
        return self.roles[1]

    def role(self, position: RolePosition) -> 'Role':
        if position == 'source':
            return self.roles[0]
        elif position == 'target':
            return self.roles[1]
        else:
            raise UnexpectedCase(  # raise:OK
                'role position "%s" is not implemented' % position)

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

    @property
    def navigability(self):
        return {
            (True, True): 'both',
            (True, False): 'backward',
            (False, True): 'forward',
            (False, False): 'none'
        }[(self.roles[0].isNavigable, self.roles[1].isNavigable)]

    @property
    def isComposition(self):
        return self.kind == 'composition'

    @property
    def isAggregation(self):
        return self.kind == 'aggregation'


class PlainAssociation(Association):

    def __init__(self,
                 name: str, model, kind=None, package=None,
                 lineNo=None, description=None, astNode=None):
        # type: (Text,ClassModel,Optional[Text], Optional[Package] ,Optional[int],Optional[Text],Optional[Text]) -> None
        super(PlainAssociation, self).__init__(
            name=name,
            model=model,
            kind=kind,
            package=package,
            lineNo=lineNo,
            description=description,
            astNode=astNode
        )
        self.model._plainAssociationNamed[name] = self

    def isPlainAssociation(self):
        return True


class Role(SourceModelElement, Member):
    """Roles.
    """

    association: Association
    """Association containing the role."""

    cardinalityMin: Optional[int]
    """Cardinality minimal or None if the cardinality is not defined."""

    cardinalityMax: Optional[int]
    """Cardinality max as an integer or None for '*' or if neither 
    cardinalities are defined. """

    type: Union[str, 'Class']
    """Class to which the role is attached."""
    # checktype: str would be the expected type but it is not. Why ?

    navigability: bool
    """Navigability of the role."""

    tags: List[str]
    """Tags associated with the role"""

    stereotypes: List[str]
    """Stereotypes associated with the role"""

    def __init__(self,
                 name: str,
                 association: Association,
                 type,  # checktype
                 cardMin: Optional[int] = None,
                 cardMax: Optional[int] = None,
                 navigability: bool = False,
                 tags: List[str] = (),
                 stereotypes: List[str] = (),
                 astNode=None,
                 lineNo=None, description=None):

        assert isinstance(name, str)
        assert isinstance(association, Association)
        # assert navigability is not None

        # Unamed role get the name of the class with lowercase
        # for the first letter
        assert name is not None
        if name == '':
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
        self.type = type  # string to be resolved in Class
        self.navigability = navigability
        self.tags = tags
        self.stereotypes = stereotypes

    @property
    def isOrdered(self) -> bool:
        return 'ordered' in self.tags

    @property
    def isNavigable(self) -> bool:
        return self.navigability != 'x'

    @property
    def isNavigabilitySpecified(self) -> bool:
        return self.navigability is not None

    @property
    def label(self) -> str:
        return '%s.%s' % (self.association.label, self.name)

    @property
    def cardinalityLabel(self) -> Optional[str]:
        if self.cardinalityMin is None and self.cardinalityMax is None:
            return None
        if self.cardinalityMin == self.cardinalityMax:
            return str(self.cardinalityMin)
        if self.cardinalityMin == 0 and self.cardinalityMax is None:
            return '*'
        return ('%s..%s' % (
            str(self.cardinalityMin),
            '*' if self.cardinalityMax is None
            else str(self.cardinalityMax)
        ))

    @property
    def opposite(self) -> 'Role':
        if self.association.isNAry:
            raise NoSuchFeature(  #r aise:OK
                '%s "opposite" is not available for %s n-ary association. '
                'Try "opposites"' % (
                    self.name,
                    self.association.name
                ))
        rs = self.association.roles
        return rs[1] if self is rs[0] else rs[0]

    @property
    def opposites(self) -> List['Role']:
        rs = list(self.association.roles)
        rs.remove(self)
        return rs

    @property
    def isOne(self) -> bool:
        return self.cardinalityMax == 1

    @property
    def isMany(self) -> bool:
        return self.cardinalityMax is None or self.cardinalityMax >= 2

    @property
    def isSource(self) -> bool:
        return (
            self.association.isBinary
            and self.association.roles[0] == self
        )

    @property
    def isTarget(self) -> bool:
        return (
            self.association.isBinary
            and self.association.roles[1] == self
        )

    @property
    def position(self) -> RolePosition:
        if self.association.isBinary:
            if self.association.roles[0] == self:
                return 'source'
            else:
                return 'target'
        else:
            raise NoSuchFeature(  # raise:OK
                'role.position() not implemented'
                ' for n-ary association')

    def __str__(self):
        return '%s::%s' % (self.association.name, self.name)

    def acceptCardinality(self, actualCardinality):
        if actualCardinality < self.cardinalityMin:
            return False
        elif (self.cardinalityMax is not None
              and actualCardinality > self.cardinalityMax):
            return False
        else:
            return True
