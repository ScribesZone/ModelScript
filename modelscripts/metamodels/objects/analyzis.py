# coding=utf-8

"""
Define a series of object violations with respect to a class
model and gather all this analysis in an ObjectModelAnalyzis
object.
There is one class for all kind of violations. The Analysis
class contains a register for each kind of violations.
"""

from __future__ import print_function
from collections import OrderedDict
from typing import List, Optional, Dict, Text, Union, Tuple
from abc import ABCMeta, abstractmethod, abstractproperty

from modelscripts.base.grammars import (
    ASTNodeSourceIssue
)
from modelscripts.base.issues import (
    Levels,
)
from modelscripts.metamodels.classes import (
    ClassModel,
    Class,
    Attribute,
    Association,
    Role,
    RolePosition,
)
from modelscripts.metamodels.textblocks import (
    TextBlock
)
from modelscripts.metamodels.objects import (
    ObjectModel,
    Object,
    Slot,
    Link,
    LinkRole
)


ISSUES={
    'BAD_LINK_TYPE':'ob.ana.Link.WrongType',
    'LINK_MANY':'ob.ana.Link.Many',
    'BAD_CARD':'ob.ana.Link.BadCardinality',
    'BAD_ATT_TYPE':'ob.ana.Slot.BadType',
    'OBJ_BAD_ID':'ob.ana.Object.BadId',
    'MISSING_SLOT':'ob.ana.Slot.Missing'
}

def icode(ilabel):
    return ISSUES[ilabel]


class ConformityViolation(object):

    __metaclass__ = ABCMeta

    def __init__(self, omAnalysis):
        self.omAnalysis=omAnalysis
        #type:ObjectModelAnalyzis

        # Register the violation in the general registry
        # Each kind of violation will additionaly register
        # itself to the specific violations registry.
        self.omAnalysis.allViolations.append(self)

    @abstractproperty
    def message(self):
        pass

    @abstractproperty
    def issueCode(self):
        pass


class LinkRoleTypeViolation(ConformityViolation):
    """
    The object o in the position p (source|target) of the link l
    is of type e instead of a.
    """

    def __init__(self,
                 omAnalysis,
                 linkRole):
        #type: (ObjectModelAnalyzis, LinkRole) -> None
        super(LinkRoleTypeViolation, self).__init__(omAnalysis)
        self.linkRole=linkRole

        # add the violation to the analysis
        link=self.linkRole.link
        v_per_link=self.omAnalysis.linkRoleTypeViolationsPerLink
        if link not in v_per_link:
            v_per_link[link]=[]
        v_per_link[link].append(self)

    @property
    def message(self):
        return(
            'The %s of the link %s is of type "%s"'
            + ' instead of "%s".') % (
                    self.linkRole.position,
                    str(self.linkRole.link),
                    self.linkRole.objectType.name,
                    self.linkRole.roleType.name)

    @property
    def issueCode(self):
        return 'BAD_LINK_TYPE'


class UniqueLinkViolation(ConformityViolation):
    def __init__(self,
                 omAnalysis,
                 duplicatedLinks):
        #type: (ObjectModelAnalyzis, List[Link]) -> None

        super(UniqueLinkViolation, self).__init__(omAnalysis)

        self.duplicatedLinks=duplicatedLinks
        #type: List[Link]

        # add the violation to the analysis
        self.omAnalysis.uniqueLinkViolations.append(self)

    #TODO: unique link
    @property
    def message(self):
        return 'TODO: UniqueLinkViolation'

    @property
    def issueCode(self):
        return 'LINK_MANY'


class CardinalityViolation(ConformityViolation):
    """
    Cardinality violation due to not enough or too much outgoing
    links for a given association.
    """

    def __init__(self,
                 omAnalysis,
                 object,
                 role):
        super(CardinalityViolation, self).__init__(omAnalysis)

        self.object=object
        #type: Object
        self.role=role
        #type: Role

        # add the violation to the analysis object
        v_per_object=omAnalysis.cardinalityViolationsPerObject
        if self.object not in v_per_object:
            v_per_object[self.object]=[]
        v_per_object[self.object].append(self)

    @property
    def linkRoles(self):
        #type: () -> List[LinkRole]
        return self.object._link_roles_per_role[self.role]

    @property
    def actualCardinality(self):
        return len(self.linkRoles)

    @property
    def message(self):
        return (
            '"%s" has %i "%s".'
            ' Cardinality is %s' % (
                self.object.name,
                self.object.cardinality(self.role),
                self.role.name,
                self.role.cardinalityLabel))

    @property
    def issueCode(self):
        return 'BAD_CARD'


class SlotValueTypeViolation(ConformityViolation):
    """
    Unauthorized value for a given attribute of a given object.
    The type of the attribute in the class model is
    not compatible with the type actual value of the slot.
    """

    def __init__(self,
                 omAnalysis,
                 slot,
                 expectedType,
                 actualType):
        super(SlotValueTypeViolation, self).__init__(omAnalysis)

        self.slot=slot
        self.expectedType=expectedType
        self.actualType=actualType

        # add the violation to the analysis
        v_per_object=omAnalysis.slotValueTypeViolationPerObject
        object=slot.object
        if object not in v_per_object:
            v_per_object[object]=[]
        v_per_object[object].append(self)

    @property
    def message(self):
        return (
            'Illegal value "%s" for attribute %s:%s' % (
                self.slot.simpleValue,
                self.slot.name,
                self.expectedType))

    @property
    def issueCode(self):
        return 'BAD_ATT_TYPE'


class IdViolation(ConformityViolation):
    """
    Violation of {id} property due to various object having
    the same id.
    """
    def __init__(self, omAnalysis, class_, objects):
        super(IdViolation, self).__init__(omAnalysis)

        self.class_=class_
        self.idPrint=objects[0].idPrint
        self.objects=objects

        v_per_class=self.omAnalysis.idViolationsPerClass
        if self.class_ not in v_per_class:
            v_per_class[class_]=[]
        v_per_class[class_].append(self)

    @property
    def message(self):
        onames=[o.name for o in self.objects]
        if len(self.objects)<=3:
            objects=','.join(onames)
        else:
            objects = (
                ','.join(onames[:2])
                +'... (%i more)' % (len(onames)-3))
        return (
            'Duplicate ids for class %s. See %s' %(
                self.class_,
                objects))

    @property
    def issueCode(self):
        return 'OBJ_BAD_ID'


class MissingSlotViolation(ConformityViolation):
    """
    Unspecified value for an attribute.
    According to the class of an object the object should have
    a slot, but there is none.
    """
    def __init__(self, omAnalysis, object, attribute):
        super(MissingSlotViolation, self).__init__(omAnalysis)

        self.object=object
        self.attribute=attribute

        # add the violation to the analysis
        v_per_object=omAnalysis.missingSlotsPerObject
        if self.object not in v_per_object:
            v_per_object[self.object]=[]
        v_per_object[self.object].append(self)

    @property
    def message(self):
        return (
            'The attribute "%s" is not specified'
            ' for object "%s".' % (
                self.attribute.name,
                self.object.name
            ))

    @property
    def issueCode(self):
        return 'MISSING_SLOT'


class ObjectModelAnalyzis(object):

    def __init__(self, objectModel):
        self.objectModel=objectModel

        self.allViolations=[]
        #type: List[ConformityViolation]
        # filled by all analyzis method through the class
        # ConformityViolation

        self.linkRoleTypeViolationsPerLink=OrderedDict()
        #type: Dict[Link, List[LinkRoleTypeViolation]]
        # filled by _analyze_roles_types

        self.uniqueLinkViolations=[]
        #type: List[UniqueLinkViolation]

        self.idViolationsPerClass=OrderedDict()
        #type: Dict[Class, List[IdViolation]]
        # filled by _analyze_object_ids

        self.slotValueTypeViolationPerObject=OrderedDict()
        #type: Dict[Object, List[SlotValueTypeViolation]]

        self.missingSlotsPerObject=OrderedDict()
        #type: Dict[Object, List[MissingSlotViolation]]
        # filled by _analyze_missing_slots

        self.cardinalityViolationsPerObject=OrderedDict()
        #type: Dict[Object, List[CardinalityViolation]]

    def _analyze_slot_types(self, object):
        """
        Visit what slot that exist for the given object
        and then compare them with the schema for the object.
        Check that all slots values have a correct type.
        """
        for slot in object.slots:
            if not slot.attribute.type.accept(slot.simpleValue):
                SlotValueTypeViolation(
                    omAnalysis=self,
                    slot=slot,
                    expectedType=slot.attribute.type,
                    actualType=type(slot.simpleValue))

    def _analyze_missing_slots(self, object):
        """
        Visit the schema and then compare it with existing slot
        to check that all expected attributes are defined
        """
        class_=object.class_
        for attr in class_.attributes: #TODO:  inheritance
            for slot in object.slots:
                if slot.attribute==attr:
                    break
            else:
                self.missingSlot=MissingSlotViolation(
                    omAnalysis=self,
                    object=object,
                    attribute=attr
                )

    def _analyze_object_slots(self):
        for object in self.objectModel.objects:
            self._analyze_slot_types(object)
            self._analyze_missing_slots(object)

    def _analyze_object_ids(self):
        om=self.objectModel
        if om.classModel is not None:
            has_none=False
            for class_ in om.classModel.classes:
                if len(class_.idPrint)>=1:
                    remaining_objects=om.classExtension(class_)[::-1]
                    while len(remaining_objects)>=2:
                        o1=remaining_objects.pop()
                        like_o1=[o1]
                        for o2 in remaining_objects:
                            eq=o1.idPrint.equals(o2.idPrint)
                            if eq==True:
                                like_o1.append(o2)
                                remaining_objects.remove(o2)
                            elif eq==False:
                                pass
                            else:
                                has_none=True
                        if len(like_o1)>=2:
                            IdViolation(
                                omAnalysis=self,
                                class_=class_,
                                objects=like_o1)

    def _analyze_link_role_types(self):
        """
        Check for all links that the type of the origin/target
        objects are compatible with the type of the corresponding roles.
        Fill _link_roles_per_role if everything is ok,
        otherwise create LinkRoleTypeViolation.
        """

        def process(linkRole):
            #TODO: inheritance
            if linkRole.objectType!=linkRole.roleType:
                # A type violation is created and the
                # do not register the linkRole to the object
                # registery.
                v = LinkRoleTypeViolation(self, linkRole)
            else:
                # The linkRole is well typed : store it in the
                # linkRole / role / opposite object registery
                oo=linkRole.opposite.object
                role=linkRole.role
                if role not in oo._link_roles_per_role:
                    oo._link_roles_per_role[role]=[]
                oo._link_roles_per_role[role].append(linkRole)

        for link in self.objectModel.links:
            for position in ['source', 'target']:
                link_role=link.linkRole(position)
                process(link_role)

    def _add_all_roles_from_schema(self):
        """
        For all objects, add all the roles (linkRole) that are in
        defined in the schema. If the role has not be defined by
        _analyze_link_role_types it will be initialized to [] here,
        otherwise it is left untouched with the existing link roles.
        """
        for object in self.objectModel.objects:
            for role in object.class_.ownedRoles:  #TODO: inheritance
                if role not in object._link_roles_per_role:
                    object._link_roles_per_role[role]=[]

    def _analyze_cardinalities(self):
        for object in self.objectModel.objects:
            for role in object._link_roles_per_role.keys():
                actual=object.cardinality(role)
                if not role.acceptCardinality(actual):
                    CardinalityViolation(
                        omAnalysis=self,
                        object=object,
                        role=role
                    )
                    # print('XX'*30, '%s.%s=#%s/%s' % (
                    #     object.name,
                    #     role.name,
                    #     actual,
                    #     role.cardinalityLabel))

    def _analyze_unique_links(self):
        pass # TODO: implement unique links if necessary

    # def XXX(self):
    #     for object in self.objectModel.objects:
    #         for role in object._link_roles_per_role.keys():
    #             print('GG'*20, '%s.%s=%s' % (
    #                 object.name,
    #                 role.name,
    #                 object.cardinality(role)))
    #             for link_role in object._link_roles_per_role[role]:
    #                 print('GG'*20,' '*10, str(link_role))


    @property
    def messages(self):
        return [ v.message for v in self.allViolations ]

    def _raise_issue(self, v):
        assert self.objectModel.checkStepEvaluation is not None
        check=self.objectModel.checkStepEvaluation.step
        ast_node=check.astNode
        position=check.position
        ASTNodeSourceIssue(
            code=icode(v.issueCode),
            astNode=ast_node,
            position=position,
            level=Levels.Error,
            message=v.message)

    def _raise_all_issues_located_at_check_point(self):
        for v in self.allViolations:
            self._raise_issue(v)

    def analyze(self):
        self._analyze_object_ids()
        self._analyze_object_slots()
        self._analyze_link_role_types()
        self._add_all_roles_from_schema()
        self._analyze_cardinalities()
        self._analyze_unique_links()
        if self.objectModel.checkStepEvaluation is not None:
            self._raise_all_issues_located_at_check_point()
        # self.XXX()





    # def _incomingsPerAssociation(self, object, association):
    #     #type: (Association) -> List[Link]
    #     return [ l
    #              for l in self._incomingLinks[object]
    # #              if l.association==association]
    # #
    # self.linksPerRole = OrderedDict()
    #
    # # type: Dict[Object, Dict[Role, List[Link]]

        # def _objects_per_role(self, object, role):
        #     # type: (Object, Role) -> List[Tuple[Object, Link]]
        #     forward = role.isTarget
        #     result = []
        #     for link in self.state.links:
        #         if forward:
        #             if link.source == object:
        #                 result.append((link.target, link))
        #         else:
        #             if link.target == object:
        #                 result.append((link.source, link))
        #     return result

    #     def _analyze_object_roles(self, object):
    #         for role in object.class_.outgoingRoles:
    #             links=self._objects_per_role(object, role)
    #             if role.acceptCardinality(len(links), role.card
    #                 cv=CardinalityViolation(
    #                     object=object,
    #                     role=role,
    #                     links=links)
    #                 self.cardinalityViolation.append(cv)
    # XXX
