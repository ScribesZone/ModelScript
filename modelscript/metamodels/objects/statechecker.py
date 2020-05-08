# coding=utf-8

"""
Define a series of object violations with respect to a class
model and gather all this analysis in an StateCheck
object.
There is one class for each kind of violation. The Analysis
class contains a register for each kind of violations.
The violation objects are first created, and then at the end the
violations are converted to issues.
"""


from collections import OrderedDict, Counter
from typing import List, Optional, Dict, Text, Union, Tuple
from abc import ABCMeta, abstractmethod

from modelscript.base.grammars import (
    ASTNodeSourceIssue
)
from modelscript.base.issues import (
    Levels)
from modelscript.metamodels.classes.classes import (
    Class)
from modelscript.metamodels.classes.associations import (
    Role)
from modelscript.metamodels.classes.invariants import (
    OCLInvariant)
from modelscript.metamodels.objects.objects import (
    Object,
    ObjectModel)
from modelscript.metamodels.objects.links import (
    LinkRole,
    Link)

__all__={
    'ConformityViolation',
    'LinkRoleTypeViolation',
    'UniqueLinkViolation',
    'CardinalityViolation',
    'SlotValueTypeViolation',
    'IdViolation',
    'UndefinedIdViolation',
    'MissingSlotViolation',
    'CompositionCycleViolation',
    'OCLInvariantViolation',
    'StateCheck'
}

ISSUES={
    'BAD_LINK_TYPE':'ob.ana.Link.WrongType',
    'LINK_MANY':'ob.ana.Link.Many',
    'BAD_CARD':'ob.ana.Link.BadCardinality',
    'BAD_ATT_TYPE':'ob.ana.Slot.BadType',
    'OBJ_BAD_ID':'ob.ana.Object.BadId',
    'OBJ_UNKNOWED_BAD_ID':'ob.ana.Object.UnknownedId',
    'MISSING_SLOT':'ob.ana.Slot.Missing',
    'CYCLE':'ob.ana.Composition.Cycle',
    'FAILED_INV':'ob.ana.Invariant.Failed'
}

def icode(ilabel):
    return ISSUES[ilabel]


class ConformityViolation(object, metaclass=ABCMeta):
    """
    Abstract class for all sort of violations that can occur
    when checking a state. This ranges from Cardinalityviolations to
    UndefinedIdViolation.
    All violations are associated to a StateCheck and provide information
    related to the issue to generate: a message, a code and a
    issue level.
    """

    def __init__(self, stateCheck):
        self.stateCheck=stateCheck
        #type: StateCheck
        """
        The state this violation applies on.
        """

        # Register the violation in the general registry.
        # Each kind of violation will additionally register
        # itself to the specific violations registry.
        self.stateCheck.allViolations.append(self)

    @property
    @abstractmethod
    def message(self):
        pass

    @property
    @abstractmethod
    def issueCode(self):
        pass

    @property
    def level(self):
        # default to Error
        return Levels.Error


class LinkRoleTypeViolation(ConformityViolation):
    """
    Conformity violation corresponding to the following case:
    the object o in the position p (source|target)
    of the link l is of type e instead of a.
    """

    def __init__(self,
                 stateCheck,
                 linkRole):
        #type: (StateCheck, LinkRole) -> None
        super(LinkRoleTypeViolation, self).__init__(stateCheck)
        self.linkRole=linkRole

        # add the violation to the analysis
        link=self.linkRole.link
        v_per_link=self.stateCheck.linkRoleTypeViolationsPerLink
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
    """
    Conformity violation corresponding to the following case:
    two links between the same pair of objects.
    """
    def __init__(self,
                 stateCheck,
                 duplicatedLinks):
        #type: (StateCheck, List[Link]) -> None

        super(UniqueLinkViolation, self).__init__(stateCheck)

        self.duplicatedLinks=duplicatedLinks
        #type: List[Link]

        # add the violation to the analysis
        self.stateCheck.uniqueLinkViolations.append(self)

    @property
    def source(self):
        return self.duplicatedLinks[0].sourceObject

    @property
    def target(self):
        return self.duplicatedLinks[0].targetObject

    @property
    def association(self):
        return self.duplicatedLinks[0].association

    @property
    def message(self):
        return '%i duplicated links (%s, %s, %s)' % (
            len(self.duplicatedLinks),
            self.source.name,
            self.association.name,
            self.target.name)

    @property
    def issueCode(self):
        return 'LINK_MANY'


class CardinalityViolation(ConformityViolation):
    """
    Cardinality violation due to not enough or too much outgoing
    links for a given association.
    """

    def __init__(self,
                 stateCheck,
                 object,
                 role):
        super(CardinalityViolation, self).__init__(stateCheck)

        self.object=object
        #type: Object
        self.role=role
        #type: Role

        # add the violation to the analysis object
        v_per_object=stateCheck.cardinalityViolationsPerObject
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
            '"%s" has %i "%s" but'
            ' cardinality is %s.' % (
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
                 stateCheck,
                 slot,
                 expectedType,
                 actualType):
        super(SlotValueTypeViolation, self).__init__(stateCheck)

        self.slot=slot
        self.expectedType=expectedType
        self.actualType=actualType

        # add the violation to the analysis
        v_per_object=stateCheck.slotValueTypeViolationPerObject
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
    Violation of {id} property due to various objects having
    the same id.
    """
    def __init__(self, stateCheck, class_, objects):
        super(IdViolation, self).__init__(stateCheck)

        self.class_=class_
        self.idPrint=objects[0].idPrint
        self.objects=objects

        v_per_class=self.stateCheck.idViolationsPerClass
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
            'Duplicated ids for %s' % objects)

    @property
    def issueCode(self):
        return 'OBJ_BAD_ID'


class UndefinedIdViolation(ConformityViolation):
    """
    Violation of {id} cannot be computed due to unspecified
    values.
    """
    def __init__(self, stateCheck, class_):
        super(UndefinedIdViolation, self).__init__(stateCheck)
        self.class_=class_
        self.stateCheck.undefinedIdViolation.append(class_)

    @property
    def message(self):
        return 'Some unspecified values makes it impossible ' \
               'to check {id}s for class %s' % self.class_.name

    @property
    def issueCode(self):
        return 'OBJ_UNKNOWED_BAD_ID'

    @property
    def level(self):
        return Levels.Info


class MissingSlotViolation(ConformityViolation):
    """
    Unspecified value for an attribute.
    According to the class of an object the object should have
    a slot, but there is none.
    """
    def __init__(self, stateCheck, object, attribute):
        super(MissingSlotViolation, self).__init__(stateCheck)

        self.object=object
        self.attribute=attribute

        # add the violation to the analysis
        v_per_object=stateCheck.missingSlotsPerObject
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


class CompositionCycleViolation(ConformityViolation):
    #TODO:3 add violation for composition cycle
    pass


class OCLInvariantViolation(ConformityViolation):
    """
    OCL invariant which failed for the given state.
    """

    def __init__(self, stateCheck, oclInvariant):
        #type: (StateCheck, OCLInvariant) -> None
        # TODO:- add param

        super(OCLInvariantViolation, self).__init__(stateCheck)

        self.oclInvariant = oclInvariant
        #type: OCLInvariant

        #TODO:- add info

        # add the violation to the analysis
        stateCheck.oclInvariantViolations.append(self)

    @property
    def message(self):
        return (
                'OCL invariant failed for objects') # TODO:- improve

    @property
    def issueCode(self):
        return 'FAILED_INV'


class StateCheck(object):
    """
    Check of an ObjectModel. Executing the check() method
    creates a list of ConformityViolation. There is one list
    for each kind of violation, and one global that
    contains all kind of violations.
    An Issue is raised for each violation.
    """

    def __init__(self, objectModel):
        #type: (ObjectModel) -> None

        self.objectModel=objectModel
        #type: ObjectModel
        # The object model being checked.

        self.allViolations=[]
        #type: List[ConformityViolation]
        # Filled by all check methods through the abstract class
        # ConformityViolation

        self.linkRoleTypeViolationsPerLink=OrderedDict()
        #type: Dict[Link, List[LinkRoleTypeViolation]]
        # Filled by _check_roles_types

        self.uniqueLinkViolations=[]
        #type: List[UniqueLinkViolation]
        # Filled by _check_unique_links

        self.undefinedIdViolation=[]
        #type: List[Class]
        # filled by _check_object_ids

        self.idViolationsPerClass=OrderedDict()
        #type: Dict[Class, List[IdViolation]]
        # filled by _check_object_ids

        self.slotValueTypeViolationPerObject=OrderedDict()
        #type: Dict[Object, List[SlotValueTypeViolation]]
        # filled by _check_slot_types

        self.missingSlotsPerObject=OrderedDict()
        #type: Dict[Object, List[MissingSlotViolation]]
        # filled by _check_missing_slots

        self.cardinalityViolationsPerObject=OrderedDict()
        #type: Dict[Object, List[CardinalityViolation]]
        # filled by _check_cardinalities

        self.oclInvariantViolations=[]
        #type: List[OCLInvariantViolation]


    @property
    def checkStepEvaluation(self):
        return self.objectModel.checkStepEvaluation

    def _check_slot_types(self, object):
        """
        Visit what slot that exist for the given object
        and then compare them with the schema for the object.
        Check that all slots values have a correct type.
        """
        for slot in object.slots:
            if not slot.attribute.type.accept(slot.simpleValue):
                SlotValueTypeViolation(
                    stateCheck=self,
                    slot=slot,
                    expectedType=slot.attribute.type,
                    actualType=type(slot.simpleValue))

    def _check_missing_slots(self, object):
        """
        Visit the schema and then compare it with existing slot
        to check that all expected attributes are defined
        """
        class_=object.class_
        for attr in class_.attributes: #TODO:2  check inheritance
            for slot in object.slots:
                if slot.attribute==attr:
                    break
            else:
                self.missingSlot=MissingSlotViolation(
                    stateCheck=self,
                    object=object,
                    attribute=attr
                )

    def _check_object_slots(self):
        for object in self.objectModel.objects:
            self._check_slot_types(object)
            self._check_missing_slots(object)

    def _check_object_ids(self):
        om=self.objectModel
        if om.classModel is not None:
            # check ids for all classes
            for class_ in om.classModel.classes:
                has_unspecified = False
                if len(class_.idPrint)>=1:
                    # more that one object, check ids
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
                                has_unspecified=True
                        if len(like_o1)>=2:
                            IdViolation(
                                stateCheck=self,
                                class_=class_,
                                objects=like_o1)
                if has_unspecified:
                    UndefinedIdViolation(
                        stateCheck=self,
                        class_=class_)

    def _check_link_role_types(self):
        """
        Check, for all links, that the type of the origin/target
        objects are compatible with the type of the corresponding
        roles in the schema.
        Fill _link_roles_per_role if everything is ok,
        otherwise create LinkRoleTypeViolation.
        Note that this method start with the actual links in
        the object model, so some association may not be covered.
        The method _add_all_roles_from_schema do the opposite:
        start from everything from the schema and add an empty
        list if necessary.
        """

        def process(linkRole):
            #TODO:2 check inheritance
            #   A conformity function should be called instead of
            #   equality.
            if linkRole.objectType!=linkRole.roleType:
                # A type violation is created and the
                # do not register the linkRole to the object
                # registery.
                print('UU'*10, 'Link role violation')
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
            print('YY'*10, 'processing link', link)
            for position in ['source', 'target']:
                link_role=link.linkRole(position)
                process(link_role)

    def _add_all_roles_from_schema(self):
        """
        For all objects, add all the roles (linkRole indeed) that are
        defined in the schema. If the role has not be defined by
        _check_link_role_types it will be initialized here. It will
        be initialized to [], at lest if there is not set before..
        """
        for object in self.objectModel.objects:
            for role in object.class_.ownedOppositeRoles:  #TODO:2 check inheritance
                if role not in object._link_roles_per_role:
                    object._link_roles_per_role[role]=[]

    def _check_cardinalities(self):
        for object in self.objectModel.objects:
            print('HH'*10, 'check card for %s' % object)
            for role in list(object._link_roles_per_role.keys()):
                actual=object.cardinality(role)
                ok=role.acceptCardinality(actual)
                print('HH'*10, '    %s[%s]=%s -> %s' % (role, role.cardinalityLabel, actual, ok))

                if not ok:
                    CardinalityViolation(
                        stateCheck=self,
                        object=object,
                        role=role
                    )
                    # print('XX'*30, '%s.%s=#%s/%s' % (
                    #     object.name,
                    #     role.name,
                    #     actual,
                    #     role.cardinalityLabel))

    def _check_unique_links(self):
        # reuse the _link_roles_per_role to simplify comparaison
        # A link is duplicate if the same object play more than
        # one the same role.
        # To avoid detecting duplicate in both end like in
        #     (a, R, b)
        #     (a, R, b)
        # only one side is considered.
        for object in self.objectModel.objects:
            for role in list(object._link_roles_per_role.keys()):
                if role.isTarget:
                    links_per_object = dict()
                    if ( len(object._link_roles_per_role[role]) >= 2):
                        for link_role in \
                                object._link_roles_per_role[role]:
                            o = link_role.object
                            if o not in links_per_object:
                                links_per_object[o] = []
                            links_per_object[o].append(link_role.link)
                        for o in list(links_per_object.keys()):
                            if len(links_per_object[o]) >= 2:
                                UniqueLinkViolation(
                                    stateCheck=self,
                                    duplicatedLinks=\
                                        links_per_object[o])

    def _check_invariants(self):
        # Check all ocl invariants.
        # This check is performed by USE tool
        # It creates OCLInvariantViolation
        # print(('@@'*40+'\n')*5)
        if False:
            print('@@'*10, 'ocl invariant to be checked with use ocl')
        # print(('@@'*40+'\n')*5)

    def XXX(self):
        debug = False
        for object in self.objectModel.objects:
            for role in list(object._link_roles_per_role.keys()):
                if debug:
                    print('GG'*20, '%s.%s=%s' % (
                        object.name,
                        role.name,
                        object.cardinality(role)))
                for link_role in object._link_roles_per_role[role]:
                    if debug:
                        print('GG'*20,' '*10, str(link_role), link_role.object)


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
            level=v.level,
            message='%s:%s' % (check.label, v.message))

    def _raise_all_issues_located_at_check_point(self):
        for v in self.allViolations:
            self._raise_issue(v)

    def check(self):
        # perform all checks
        self._check_object_ids()
        self._check_object_slots()
        self._check_link_role_types()    # must be here
        self._add_all_roles_from_schema()  # must be here
        self._check_cardinalities()
        self._check_unique_links()
        self._check_invariants()

        # tranform failed check to issues
        if self.objectModel.checkStepEvaluation is not None:
            self._raise_all_issues_located_at_check_point()

        self.XXX()





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

    #     def _check_object_roles(self, object):
    #         for role in object.class_.outgoingRoles:
    #             links=self._objects_per_role(object, role)
    #             if role.acceptCardinality(len(links), role.card
    #                 cv=CardinalityViolation(
    #                     object=object,
    #                     role=role,
    #                     links=links)
    #                 self.cardinalityViolation.append(cv)
    # XXX
