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


class AccessSet(object):

    def __init__(self, permissionSet=None):

        self.accesses=[] #type: List[Access]
        self.permissionSet=permissionSet #type: Optional[PermissionSet]



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

    def __init__(self, permissionSet=None):
        super(AccessModel, self).__init__()
        self.accessSet=AccessSet(permissionSet=permissionSet) #type:AccessSet


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

