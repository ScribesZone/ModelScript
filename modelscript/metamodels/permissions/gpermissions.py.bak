# coding=utf-8

"""
---------------------------------------------------------------------
                  Semantics of permissions
---------------------------------------------------------------------

PermissionSet
<>- Permission
<>- Control
--- control(access) : Control

SAR
<|- Permission
    --- accept(access) : bool

Control
<|- Denial
<|- Authorisation


--------------------------------------------------------------------
                    Generic permission model
--------------------------------------------------------------------

PermissionModel
<>- PermissionRule

"""

from abc import ABCMeta
from typing import List, Optional, Set

from modelscript.megamodels.models import Model
from modelscript.metamodels.permissions.sar import SAR
from modelscript.megamodels.elements import SourceModelElement

__all__=(
    # Semantics
    'PermissionSet',
    'Permission',
    'Control',
    'Denial',
    'Authorisation',

    # Generic abstract syntax
    'PermissionModel',
    'PermissionRule'
)



class Permission(SAR):
    """
    A permission is a triplet (subject, action, resource).
    It can accept() or not an access.
    """

    def __init__(self, subject, action, resource, rule=None):
        super(Permission, self).__init__(
            subject=subject,
            action=action,
            resource=resource
        )
        self.rule=rule

    def accept(self, access):
        #type: ('Access') -> bool

        _=(  # order might help for performance (or not)
                self.action in access.action.allSuperActions
            and self.resource in access.resource.allSuperResources
            and self.subject in access.subject.allSuperSubjects)
        return _

    def __str__(self):
        return '%s can %s %s' % (
            self.subject.subjectLabel,
            self.action.actionLabel,
            self.resource.resourceLabel
        )



class Control(object):
    """
    A control is the result of checking that a permission
    accept or not a access. A control is either an Authorisation
    or a Denial.
    """
    __metaclass__ = ABCMeta

    def __init__(self, access):
        #type: ('Access') -> None
        self.access=access


class Authorisation(Control):
    """
    A successful control. In this case the permission that
    allowed success is given.
    """

    def __init__(self, access, permission):
        super(Authorisation, self).__init__(access)
        self.permission=permission


class Denial(Control):
    """
    A denial of access. The same information as control as
    no permission was found to allow the access.
    """
    def __init__(self, access):
        super(Denial, self).__init__(access)


class PermissionSet(object):
    """
    A set of permission (in no particular order).
    This collection of permission can be used to
    control an access and create an Control object
    accordingly (either a Authorisation or Denial).
    The permission set also accumulate the control
    made so using it (either authorisation or denial).
    """
    def __init__(self, permissions=None):
        #type: (Optional[Set[Permission]])->None

        self.permissions = (
            set(permissions) if permissions is not None
            else set())
        #type: Set[Permission]
        """ The collection of permissions"""

        self.controls=[]
        #type: List[Control]
        """ The list of controls already made """

    def control(self, access):
        #type: ('Access') -> Control
        """
        Control an access according to the permission set.
        Returns the control, (either authorisation or denial)
        """
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



#--------------------------------------------------------------------
#                    Generic permission model
#--------------------------------------------------------------------

class PermissionModel(Model):
    """
    Abstract permission model.
    """
    __metaclass__ = ABCMeta

    def __init__(self):
        super(PermissionModel, self).__init__()

        self.rules=[]
        #type: List[PermissionRule]


class PermissionRule(SourceModelElement):
    __metaclass__ = ABCMeta

    def __init__(self,
                 model,
                 lineNo=None,
                 astNode=None):
        #type: (PermissionModel, Optional[int], Optional['ASTNode']) -> None
        super(PermissionRule, self).__init__(
            model=model,
            name=None,
            lineNo=lineNo,
            astNode=astNode)

        self.permissions=[]   # TODO:- check if this is useful
        #type: List[Permission]