from __future__ import print_function
import abc
import collections

from typing import Union, Optional, Text

from modelscripts.megamodels.elements import (
    SourceModelElement)
from modelscripts.megamodels.py import (
    MAttribute,
    MReference)
from modelscripts.metamodels.classes import (
    PackagableElement,
    Entity,
    Member)
from modelscripts.base.exceptions import (
    UnexpectedCase,
    UnexpectedValue,
    NoSuchFeature,
    MethodToBeDefined)

RolePosition=Union['source','target']

def opposite(rolePosition):
    if rolePosition=='source':
        return 'target'
    elif rolePosition=='target':
        return 'source'
    else:
        raise UnexpectedCase( #raise:OK
            "Role position '%s' doesn't exists." % rolePosition)


class Association(PackagableElement, Entity):
    """
    Associations.
    """

    __metaclass__ = abc.ABCMeta

    META_COMPOSITIONS = [
        'roles',
    ]

    def __init__(self,
                 name, model, kind=None, package=None,
                 lineNo=None, description=None, astNode=None):
        # type: (Text, 'ClassModel',Optional[Text], Optional['Package'] ,Optional[int],Optional[Text],Optional[Text]) -> None
        super(Association, self).__init__(
            name=name,
            model=model,
            package=package,
            astNode=astNode,
            lineNo=lineNo, description=description)
        self.kind = kind
        #type: Text
        # association|composition|aggregation|associationclass
        # TODO:3 check if 'associationclass' is ok there
        self.roleNamed = collections.OrderedDict() # indexed by name

    @property
    def roles(self):
        return self.roleNamed.values()

    @property
    def roleNames(self):
        return self.roleNamed.keys()

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
            raise NoSuchFeature( #raise:OK
                '"sourceRole" is not defined on "%s" n-ary association' % (
                    self.name
                ))
        return self.roles[0]

    @MReference('Role')
    def targetRole(self):
        if not self.isBinary:
            raise NoSuchFeature( #raise:OK
                '"targetRole" is not defined on "%s" n-ary association' % (
                    self.name
                ))
        return self.roles[1]

    def role(self, position):
        #type: (RolePosition) -> Role
        if position=='source':
            return self.roles[0]
        elif position=='target':
            return self.roles[1]
        else:
            raise UnexpectedCase( #raise:OK
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
            (True, True) : 'both',
            (True, False) : 'backward',
            (False, True) : 'forward',
            (False, False) : 'none'
        }[(self.roles[0].isNavigable, self.roles[1].isNavigable)]

    @property
    def isComposition(self):
        return self.kind=='composition'

    @property
    def isAggregation(self):
        return self.kind=='aggregation'

    @abc.abstractmethod
    def isPlainAssociation(self):
        # This method is not really useful as isinstance can be used.
        # It is just used to prevent creating object of this class
        # (using ABCMeta is not enough to prevent this).
        raise MethodToBeDefined( #raise:OK
            'isPlainAssociation() must be defined.')


class PlainAssociation(Association):

    def __init__(self,
                 name, model, kind=None, package=None,
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
    """
    Roles.
    """

    def __init__(self, name, association, astNode=None,
                 cardMin=None, cardMax=None, type=None,
                 navigability=None,
                 qualifiers=None, subsets=None, isUnion=False,
                 expression=None,
                 tags=(),
                 stereotypes=(),
                 lineNo=None, description=None):

        # unamed role get the name of the class with lowercase for the first letter
        if name == '' or name is None:
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
        self.type = type  # string to be resolved in Class

        # (str,str) to be resolved in (str,SimpleType)
        self.qualifiers = qualifiers
        self.subsets = subsets
        self.isUnion = isUnion
        self.expression = expression
        self.tags=tags
        self.navigability=navigability
        self.stereotypes=stereotypes

    @property
    def isOrdered(self):
        return 'ordered' in self.tags

    @property
    def isNavigable(self):
        return self.navigability != 'x'

    @property
    def isNavigabilitySpecified(self):
        return self.navigability is not None

    @property
    def label(self):
        return '%s.%s' % (self.association.label, self.name)

    @property
    def cardinalityLabel(self):
        if self.cardinalityMin is None and self.cardinalityMax is None:
            return None
        if self.cardinalityMin == self.cardinalityMax:
            return str(self.cardinalityMin)
        if self.cardinalityMin == 0 and self.cardinalityMax is None:
            return '*'
        return ('%s..%s' % (
            str(self.cardinalityMin),
            '*' if self.cardinalityMax is None else str(
                self.cardinalityMax)

        ))

    @property
    def opposite(self):
        if self.association.isNAry:
            raise NoSuchFeature( #raise:OK
                '%s "opposite" is not available for %s n-ary association. '
                'Try "opposites"' % (
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

    @property
    def position(self):
        # type: () -> RolePosition
        if self.association.isBinary:
            if self.association.roles[0] == self:
                return 'source'
            else:
                return 'target'
        else:
            raise NoSuchFeature( #raise:OK
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