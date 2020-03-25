# coding=utf-8
"""

"""



from typing import List, Optional
from modelscript.megamodels.dependencies.metamodels import (
    MetamodelDependency
)
from modelscript.megamodels.metamodels import Metamodel
from modelscript.base.metrics import Metrics

# ---------------------------------------------------------------
#  Abstract syntax
# ---------------------------------------------------------------
from modelscript.metamodels.permissions.gpermissions import (
    Permission,
    PermissionSet,
    PermissionModel,
    PermissionRule
)
from modelscript.metamodels.permissions.sar import (
    Action,
    SAR
)
from modelscript.metamodels.permissions.sar import (
    Subject,
    Resource,
    Action,
)
from modelscript.metamodels.usecases import (
    UsecaseModel
)

__all__=(
    # Concrete actions
    'CreateAction',
    'ReadAction',
    'UpdateAction',
    'DeleteAction',
    'ExecuteAction',

    # Concrete models and rule
    'UCPermissionModel',
    'FactorizedPermissionRule'
)

ClassModel='ClassModel'

#------------------------------------------------------------------------------
#    Usecases/Classes specific
#------------------------------------------------------------------------------

CreateAction = Action('create', None)
ReadAction = Action('read', None)
UpdateAction = Action('update', None)
DeleteAction = Action('delete', None)
ExecuteAction = Action('execute', None)


class FactorizedPermissionRule(PermissionRule):
    def __init__(self, model, subjects, actions, resources, astNode=None, lineNo=None):
        #type: (UCPermissionModel, List[Subject], List[Action], List[Resource], Optional['ASTNode'], Optional[int])->None
        """
        A concrete rule representing at the same time various
        permissions thanks to the factorisation of
        subjects, actors and resources.
        For instance the rule
            ((S1,S2), (A1,A2,A3), (R1))
        represents 6 permissions.
        """
        super(FactorizedPermissionRule, self).__init__(
            model=model,
            lineNo=lineNo,
            astNode=astNode)

        self.subjects=subjects
        #type: List[Subject]

        self.actions=actions
        #type: List[Action]

        self.resources=resources
        #type: List[Resource]

    def __str__(self):
        return '%s %s %s' % (
            ','.join([s.subjectLabel for s in self.subjects]),
            ','.join([s.actionLabel for s in self.actions]),
            ','.join([s.resourceLabel for s in self.resources]),
        )


class UCPermissionModel(PermissionModel):
    """
    A usecase-class permission model
    """
    def __init__(self):
        super(UCPermissionModel, self).__init__()

        self.usecaseModel=None
        #type: Optional[UsecaseModel]
        #set later

        self.classModel=None
        #type: Optional[ClassModel]

        self.rules=[]
        #type: List[FactorizedPermissionRule]
        # The list of rules in the model. Actually the order
        # in this list is not important.
        # Note that "rules" is already defined in the superclass
        # but defining it again here allow to have better typing

        self._permissionSet=None
        #type: Optional[PermissionSet]
        # The permission set, computed on demand.
        # see permissionSet property.
        # The permission set is just the expansion of the rule
        # component in many different permissions.

    @property
    def metamodel(self):
        #type: () -> Metamodel
        return METAMODEL

    @property
    def permissionSet(self):
        #type: ()->PermissionSet

        if self._permissionSet is None:
            self._interpret()
        # noinspection PyTypeChecker
        return self._permissionSet

    @property
    def metrics(self):
        #type: () -> Metrics
        ms=super(UCPermissionModel, self).metrics
        ms.addList((
            ('rule', len(self.rules)),
            ('permission', len(self.permissionSet.permissions) ),
        ))
        return ms

    def _interpret(self):
        #type: ()->None
        self._permissionSet= PermissionSet()
        for rule in self.rules:
            for s in rule.subjects:
                for r in rule.resources:
                    for a in rule.actions:
                        p= Permission(s, a, r, rule)
                        self._permissionSet.permissions.add(p)
                        rule.permissions.append(p)

    def __str__(self):
        return '\n'.join([str(r) for r in self.rules])


METAMODEL=Metamodel(
    id='pe',    # other model could be registered
    label='permission',
    extension='.pes',
    modelClass=UCPermissionModel
)
MetamodelDependency(
    sourceId='pe',
    targetId='gl',
    optional=True,
    multiple=True,
)
MetamodelDependency(
    sourceId='pe',
    targetId='us',
    optional=False,
    multiple=False,
)
MetamodelDependency(
    sourceId='pe',
    targetId='cl',
    optional=False,
    multiple=False,
)