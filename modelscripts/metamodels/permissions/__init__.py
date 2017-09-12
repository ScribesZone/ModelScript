# coding=utf-8
"""

"""


from __future__ import absolute_import, division, print_function, unicode_literals

from typing import List, Optional

from modelscripts.megamodels import Metamodel
# ---------------------------------------------------------------
#  Abstract syntax
# ---------------------------------------------------------------
from modelscripts.metamodels.permissions.gpermission import Permission, PermissionSet, PermissionModel, PermissionRule
from modelscripts.metamodels.permissions.sar import Action, SAR
from modelscripts.metamodels.permissions.sar import (
    Subject,
    Resource,
    Action,

)

#------------------------------------------------------------------------------
#    Usecases/Classes specific
#------------------------------------------------------------------------------

CreateAction = Action('C', None)
ReadAction = Action('R', None)
UpdateAction = Action('U', None)
DeleteAction = Action('D', None)
ExecuteAction = Action('X', None)


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
    def metamodel(self):
        return metamodel

    @property
    def permissionSet(self):
        #type: ()->PermissionSet
        if self._permissionSet is None:
            self._interpret()
        # noinspection PyTypeChecker
        return self._permissionSet

    def _interpret(self):
        #type: ()->None
        self._permissionSet= PermissionSet()
        for rule in self.rules:
            for s in rule.subjects:
                for r in rule.resources:
                    for a in rule.actions:
                        p= Permission(s, a, r, rule)
                        self._permissionSet.permissions.append(p)
                        rule.permissions.append(p)

    def __str__(self):
        return '\n'.join([str(r) for r in self.rules])


metamodel=Metamodel(
    id='pm',    # other model could be registered
    label='permission',
    extension='.pmm',
    modelClass=UCPermissionModel
)