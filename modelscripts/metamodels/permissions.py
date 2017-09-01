# coding=utf-8
"""

"""


from __future__ import absolute_import, division, print_function, unicode_literals

import abc
from abc import ABCMeta

from typing import List, Dict, Text, Optional

from modelscripts.sources.models import Model
from modelscripts.sources.sources import (
    SourceElement
)


# from modelscripts.metamodels.classes import (
#     ClassModel,
#     # Class,
#     # Association,
#     # AssociationClass,
#     # Attribute,
#     # Role,
# )
# from modelscripts.metamodels.usecases import (
#     UsecaseModel,
#     Actor,
#     Usecase,
# )

# from modelscripts.metamodels.classes import (
#     Resource,
#     Member,
# )


#---------------------------------------------------------------
#  Abstract syntax
#---------------------------------------------------------------

class Subject(object):
    __metaclass__ = ABCMeta

    @property
    def superSubjects(self):
        """ Direct parents """
        # type: () -> List[Subject]
        return []

    @property
    def allSuperSubjects(self):
        # type: () -> List[Subject]
        """ All supersubject recursively + this one"""
        parents = self.superSubjects
        _=[self]
        for p in parents:
            _.extend(p.allSuperSubjects)
        return _

    @property
    def subjectLabel(self):
        return _getNaming(self)


class Action(object):
    _actionNamed = {}  # type: Dict[Text, Action]

    @classmethod
    def named(cls, name):
        return Action._actionNamed[name]

    def __init__(self, name, value):
        self.value = value
        self.name = name
        Action._actionNamed[self.name] = self

    @property
    def actionLabel(self):
        return self.name

    def __str__(self):
        return self.actionLabel

    @property
    def superActions(self):
        """ Direct parents """
        # type: () -> List[Action]
        return []

    @property
    def allSuperActions(self):
        """ All superactions recursively + this one"""
        # type: () -> List[Action]
        acs = self.superActions
        return [self]+acs+ [a.superActions for a in acs]


class Resource(object):
    __metaclass__ = abc.ABCMeta

    @property
    def resourceLabel(self):
        return _getNaming(self)

    @property
    def superResources(self):
        """ Direct parents """
        # type: () -> List[Resource]
        return []

    @property
    def allSuperResources(self):
        # type: () -> List[Resource]
        """ All superresources recursively + this one"""
        rs = self.superResources
        return [self] + rs + [r.allSuperResources for r in rs]

class SAR(object):
    """
    Subject-Action-Resource triplet.
    """

    __metaclass__ = ABCMeta

    def __init__(self, subject, action, resource):
        #type: (Subject, Action, Resource) -> None
        self.subject=subject #type: Subject
        self.action=action #type: Action
        self.resource=resource #type: Resource

    def __str__(self):
        return '%s %s %s' % (
            self.subject.subjectLabel,
            self.action.actionLabel,
            self.resource.resourceLabel
        )



#-------------------------------------------------------------
# Access
#-------------------------------------------------------------

class Access(SAR):

    def __init__(self,
                 subject, action, resource,
                 accessSet):
        #type: (Subject, Action, Resource, AccessSet) -> None
        super(Access, self).__init__(
            subject=subject,
            action=action,
            resource=resource,
        )
        self.accessSet=accessSet #type: AccessSet
        self.accessSet.accesses.append(self)
        self.control = None  #type: Optional[Control]
        # None means that the access has not been controlled

        ps=self.accessSet.permissionSet
        if ps is not None:
            self.control=ps.control(self)

    def __str__(self):
        if self.control is None:
            _='Uncontrolled access'
        elif isinstance(self.control, Authorisation):
            _='Authorized access'
        elif isinstance(self.control, Denial):
            _='Access denied'
        else:
            raise NotImplementedError()
        return '%s: %s' % (
            _,
            SAR.__str__(self))


class AccessModel(Model):

    def __init__(self, permissionSet=None, source=None):
        super(AccessModel, self).__init__(
            source=source
        )
        self.accessSet=AccessSet(permissionSet=permissionSet) #type:AccessSet


class AccessSet(object):

    def __init__(self, permissionSet=None):

        self.accesses=[] #type: List[Access]
        self.permissionSet=permissionSet #type: Optional[PermissionSet]



#-------------------------------------------------------------
# Permission
#-------------------------------------------------------------


class Permission(SAR):

    def __init__(self, subject, action, resource, rule=None):
        super(Permission, self).__init__(
            subject=subject,
            action=action,
            resource=resource
        )
        self.rule=rule

    def accept(self, access):
        #type: (Access) -> bool
        _=(
            self.action in access.action.allSuperActions
            and self.resource in access.resource.allSuperResources
            and self.subject in access.subject.allSuperSubjects
        )
        return _

    def __str__(self):
        return '%s is allowed to %s %s' % (
            self.subject.subjectLabel,
            self.action.actionLabel,
            self.resource.resourceLabel
        )

class Control(object):
    __metaclass__ = ABCMeta

    def __init__(self, access):
        self.access=access


class Authorisation(Control):

    def __init__(self, access, permission):
        super(Authorisation, self).__init__(access)
        self.permission=permission

class Denial(Control):

    def __init__(self, access):
        super(Denial, self).__init__(access)


class PermissionSet(object):

    def __init__(self, permissions=set()):
        #type: ()->None
        self.permissions = []
        self.controls=[]

    def control(self, access):
        #type: (Access) -> Control
        for p in self.permissions:
            if p.accept(access):
                c=Authorisation(
                    access=access,
                    permission=p)
                break
        else: #for
            c=Denial(access)
        self.controls.append(c)
        return c










def _getNaming(o):
    for att in ['label', 'name', 'id', '__str__', '__repr__']:
        if hasattr(o, att):
            return getattr(o, att)
    return id(o)


class PermissionModel(Model):
    __metaclass__ = ABCMeta

    pass

class PermissionRule(SourceElement):
    __metaclass__ = ABCMeta

    def __init__(self, lineNo, model):
        #type: (int, PermissionModel) -> None
        super(PermissionRule, self).__init__(lineNo=lineNo)
        self.model=model
        self.permissions=[] #type: List[Permission]







#------------------------------------------------------------------------------
#    Usecases/Classes specific
#------------------------------------------------------------------------------

CreateAction=Action('C',None)
ReadAction=Action('R', None)
UpdateAction=Action('U', None)
DeleteAction=Action('D', None)
ExecuteAction=Action('X', None)


class FactorizedPermissionRule(PermissionRule):
    def __init__(self, model, subjects, actions, resources, lineNo=None):
        #type: (UCPermissionModel, List[Subject], List[Action], List[Resource])->None
        super(FactorizedPermissionRule, self).__init__(
            lineNo=lineNo,
            model=model)
        self.subjects=subjects      #type: List[Subject]
        self.actions=actions        #type: List[Action]
        self.resources=resources    #type: List[Resource]

    def __str__(self):
        return '%s %s %s' % (
            ','.join([s.subjectLabel for s in self.subjects]),
            ','.join([s.actionLabel for s in self.actions]),
            ','.join([s.resourceLabel for s in self.resources]),
        )


class UCPermissionModel(PermissionModel):

    def __init__(self, usecaseModel, classModel, source=None):
        # #type: (UsecaseModel, ClassModel, SourceFile) -> None
        super(UCPermissionModel, self).__init__(source=source)
        self.usecaseModel=usecaseModel
        self.classModel=classModel
        self.rules=[]             #type: List[FactorizedPermissionRule]

        self._permissionSet=None   #type: Optional[PermissionSet]

    @property
    def permissionSet(self):
        #type: ()->PermissionSet
        if self._permissionSet is None:
            self._interpret()
        # noinspection PyTypeChecker
        return self._permissionSet

    def _interpret(self):
        #type: ()->None
        self._permissionSet=PermissionSet()
        for rule in self.rules:
            for s in rule.subjects:
                for r in rule.resources:
                    for a in rule.actions:
                        p=Permission(s, a, r, rule)
                        self._permissionSet.permissions.append(p)
                        rule.permissions.append(p)

    def __str__(self):
        return '\n'.join([str(r) for r in self.rules])
