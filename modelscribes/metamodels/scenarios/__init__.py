# coding=utf-8
"""
Code of the Scenario metamodel.

The structure of this module is::

    ScenarioModel
    <>--* ActorInstanceNamed
    <>--* ContextBlock
    <>--* MainBlock
    <>--* Operation
    --->0..1 ScenarioEvaluation
"""

# TODO: add support for  'include <x.obs>

import collections

from typing import Optional, Dict, List, Text

from modelscribes.base.metrics import Metrics
from modelscribes.megamodels.elements import SourceModelElement
from modelscribes.megamodels.metamodels import Metamodel
from modelscribes.megamodels.models import Model
from modelscribes.megamodels.dependencies.metamodels import (
    MetamodelDependency
)
from modelscribes.metamodels.classes import (
    ClassModel,
)
from modelscribes.metamodels.scenarios.evaluations import (
    ScenarioEvaluation
)
from modelscribes.metamodels.permissions import (
    UCPermissionModel)
from modelscribes.metamodels.permissions.sar import Subject
from modelscribes.metamodels.scenarios.blocks import (
    Block,
    MainBlock,
    ContextBlock
)
from modelscribes.metamodels.scenarios.operations import (
    Operation
)
from modelscribes.metamodels.usecases import (
    Actor,
    UsecaseModel,
)

__all__=(
    'ScenarioModel',
    'ActorInstance',
)

DEBUG=3

class ScenarioModel(Model, Subject):
    def __init__(self):
        #type: () -> None

        super(ScenarioModel, self).__init__()

        self.usecaseModel=None #type: Optional[UsecaseModel]
        # set later

        self.classModel=None #type: Optional[ClassModel]
        # set later

        self.permissionModel=None #type: Optional[UCPermissionModel]
        # set later

        self.actorInstanceNamed = collections.OrderedDict()
        #type: Dict[Text, ActorInstance]

        self.contextBlocks=[] #type: List[ContextBlock]
        self.mainBlocks=[] #type: List[MainBlock]
        self.originalOrderBlocks=[] #type:List[Block]

        #--- evaluation
        self.scenarioEvaluation=ScenarioEvaluation(self)
        #type: 'ScenarioEvaluation'
        # Create always an empty model to avoid None exception

    @property
    def metamodel(self):
        #type: () -> Metamodel
        return METAMODEL



    @property
    def logicalOrderBlocks(self):
        #type: () -> List[Block]
        return self.contextBlocks+self.mainBlocks

    @property
    def actorInstances(self):
        return self.actorInstanceNamed.values()

    @property
    def actorInstanceNames(self):
        return self.actorInstanceNamed.keys()

    @property
    def metrics(self):
        #type: () -> Metrics
        ms=super(ScenarioModel, self).metrics
        ms.addList((
            ('actorInstance', len(self.actorInstances)),
            ('contextBlock', len(self.contextBlocks) ),
            ('mainBlock', len(self.mainBlocks) ),
        ))
        return ms

    @property
    def isEvaluated(self):
        return self.scenarioEvaluation.isEvaluated

    def evaluate(self, originalOrder=True):
        self.scenarioEvaluation.evaluate(originalOrder)


class ActorInstance(SourceModelElement, Subject):
    def __init__(self, scenario, name, actor,
                 code=None, lineNo=None, docComment=None, eolComment=None):
        SourceModelElement.__init__(self, name, code, lineNo, docComment, eolComment)
        self.scenario=scenario
        #type: ScenarioModel

        self.name=name

        self.actor=actor
        # type: Actor
        self.scenario.actorInstanceNamed[self.name]=self

    @property
    def superSubjects(self):
        return [self.actor]


METAMODEL = Metamodel(
    id='sc',
    label='scenario',
    extension='.scs',
    modelClass=ScenarioModel,
    modelKinds=('', 'informal', 'preliminary', 'detailed')
)
MetamodelDependency(
    sourceId='sc',
    targetId='gl',
    optional=True,
    multiple=True,
)
MetamodelDependency(
    sourceId='sc',
    targetId='cl',
    optional=True,
    multiple=False,
)
MetamodelDependency(
    sourceId='sc',
    targetId='us',
    optional=True,
    multiple=False,
)
MetamodelDependency(
    sourceId='sc',
    targetId='pe',
    optional=True,
    multiple=False,
)