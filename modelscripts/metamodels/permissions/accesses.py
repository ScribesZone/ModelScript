# coding=utf-8
from typing import List, Optional

from modelscripts.megamodels.metamodels import Metamodel
from modelscripts.megamodels.dependencies.metamodels import (
    MetamodelDependency
)
from modelscripts.megamodels.models import Model
from modelscripts.metamodels.permissions import (
    PermissionSet
)
from modelscripts.metamodels.permissions.gpermissions import Control, Authorisation, Denial
from modelscripts.metamodels.permissions.sar import Subject, Action, Resource, SAR
"""
Classes to model access from subject to resources through actions.

AccessModel
--> AccessSet
    -o> PermissionSet
    <>- Access
        -o> Control
    
"""

__all__=(
    # semantics
    'AccessSet',
    'Access',

    # abstract syntax
    'AcessModel',
    ''

)
class AccessSet(object):
    """
    A set of access optionally controlled by a permission set.
    """

    def __init__(self, permissionSet=None):

        self.accesses=[]
        #type: List[Access]

        self.permissionSet=permissionSet
        #type: Optional[PermissionSet]



class Access(SAR):
    """
    Triplet (subject, action, resource) meaning that the subject
    do perform the action on the resource.
    If a control is indicated it means that the access has already
    been controlled by a permission set. Otherwise the access has not
    been controlled yet.
    """

    def __init__(self,
                 subject, action, resource,
                 accessSet):
        #type: (Subject, Action, Resource, AccessSet) -> None
        super(Access, self).__init__(
            subject=subject,
            action=action,
            resource=resource,
        )
        self.accessSet=accessSet
        #type: AccessSet
        # The access set the access pertains to.

        self.accessSet.accesses.append(self)

        self.control = None
        #type: Optional[Control]
        # None means that the access has not been controlled.

        ps=self.accessSet.permissionSet
        if ps is not None:
            self.control=ps.control(self)
        # If a permission set is given for the

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
    """
    A model of access, syntactically representing a access Set
    """

    def __init__(self, permissionSet=None):
        super(AccessModel, self).__init__()

        self.accessSet=AccessSet(
            permissionSet=permissionSet)
        #type:AccessSet


METAMODEL = Metamodel(
    id='ac',
    label='access',
    extension='.acs',
    modelClass=AccessModel
)
MetamodelDependency(
    sourceId='ac',
    targetId='gl',
    optional=True,
    multiple=True,
)
MetamodelDependency(
    sourceId='ac',
    targetId='us',
    optional=False,
    multiple=False,
)
MetamodelDependency(
    sourceId='ac',
    targetId='cl',
    optional=False,
    multiple=False,
)

