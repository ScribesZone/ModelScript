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
from abc import ABCMeta

from modelscripts.base.metrics import Metrics
from modelscripts.megamodels.elements import SourceModelElement
from modelscripts.megamodels.metamodels import Metamodel
from modelscripts.megamodels.models import Model
from modelscripts.megamodels.dependencies.metamodels import (
    MetamodelDependency
)
from modelscripts.metamodels.classes import (
    ClassModel,
)
from modelscripts.metamodels.scenarios.evaluations import (
    ScenarioEvaluation
)
from modelscripts.metamodels.permissions import (
    UCPermissionModel)
from modelscripts.metamodels.permissions.sar import Subject
from modelscripts.metamodels.usecases import (
    Actor,
    System,
    UsecaseModel,
)

META_CLASSES=(
    'ScenarioModel',
    'ActorInstance',
    'SystemInstance',
)

__all__=META_CLASSES

DEBUG=3

Block='Block'
MainBlock='MainBlock'
ContextBlock='ContextBlock'

class ScenarioModel(Model, Subject):
    META_COMPOSITIONS=[
        'actorInstances',
        'systemInstance',
        'originalOrderBlocks',
        'scenarioEvaluation',
    ]

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

        self.systemInstance=None
        #type: Optional[System]

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


class ScenarioTopLevelElement(SourceModelElement):
    __metaclass__ = ABCMeta

    def __init__(self, model, name,
                 code=None, lineNo=None,
                 docComment=None, eolComment=None):
        self.scenario=model
        #type: ScenarioModel
        SourceModelElement.__init__(self,
            model=self.scenario,
            name=name,
            code=code,
            lineNo=lineNo,
            docComment=docComment,
            eolComment=eolComment)


class ActorInstance(ScenarioTopLevelElement, Subject):
    def __init__(self, model, name, actor,
                 code=None, lineNo=None, docComment=None, eolComment=None):
        ScenarioTopLevelElement.__init__(self,
            model=model,
            name=name,
            code=code,
            lineNo=lineNo,
            docComment=docComment,
            eolComment=eolComment)

        self.actor=actor
        # type: Actor
        self.scenario.actorInstanceNamed[self.name]=self

    @property
    def superSubjects(self):
        return [self.actor]


class SystemInstance(ScenarioTopLevelElement): #TODO: check if Resource
    def __init__(self, model, name, system,
                 code=None, lineNo=None,
                 docComment=None, eolComment=None):
        ScenarioTopLevelElement.__init__(self,
            model=model,
            name=name,
            code=code,
            lineNo=lineNo,
            docComment=docComment,
            eolComment=eolComment)

        self.system = system
        # type: System
        self.scenario.systemInstance = self


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