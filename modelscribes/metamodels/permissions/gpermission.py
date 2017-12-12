# coding=utf-8
from abc import ABCMeta
from typing import List

from modelscribes.base.sources import SourceElement
from modelscribes.megamodels.models import Model
from modelscribes.metamodels.permissions.sar import SAR
from modelscribes.megamodels.elements import SourceModelElement

class Permission(SAR):

    def __init__(self, subject, action, resource, rule=None):
        super(Permission, self).__init__(
            subject=subject,
            action=action,
            resource=resource
        )
        self.rule=rule

    def accept(self, access):
        #type: ('Access') -> bool
        _=(
            self.action in access.action.allSuperActions
            and self.resource in access.resource.allSuperResources
            and self.subject in access.subject.allSuperSubjects
        )
        return _

    def __str__(self):
        return '%s can %s %s' % (
            self.subject.subjectLabel,
            self.action.actionLabel,
            self.resource.resourceLabel
        )



class Control(object):
    __metaclass__ = ABCMeta

    def __init__(self, access):
        #type: ('Access') -> None
        self.access=access


class Authorisation(Control):

    def __init__(self, access, permission):
        super(Authorisation, self).__init__(access)
        self.permission=permission


class Denial(Control):

    def __init__(self, access):
        super(Denial, self).__init__(access)


class PermissionSet(object):

    def __init__(self, permissions=None):
        #type: ()->None
        if permissions is None:
            permissions=set()
        self.permissions = permissions
        self.controls=[]

    def control(self, access):
        #type: ('Access') -> Control
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


class PermissionModel(Model):
    __metaclass__ = ABCMeta

    pass


class PermissionRule(SourceModelElement):
    __metaclass__ = ABCMeta

    def __init__(self, lineNo, model):
        #type: (int, PermissionModel) -> None
        super(PermissionRule, self).__init__(lineNo=lineNo)
        self.model=model
        self.permissions=[] #type: List[Permission]