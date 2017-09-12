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

# TODO: add support for  'include <x.obm>

import collections

from typing import Optional, Dict, List, Text

from modelscripts.base.sources import (
    SourceFile,
    SourceElement
)
from modelscripts.megamodels import Model, Metamodel
from modelscripts.metamodels.classes import (
    ClassModel,
)
from modelscripts.metamodels.permissions import (
    UCPermissionModel)
from modelscripts.metamodels.permissions.gpermission import PermissionModel
from modelscripts.metamodels.permissions.sar import Subject
from modelscripts.metamodels.scenarios.blocks import (
    Block,
    MainBlock,
    ContextBlock
)
from modelscripts.metamodels.scenarios.operations import (
    Operation
)
from modelscripts.metamodels.usecases import (
    Actor,
    UsecaseModel,
)

DEBUG=3

class ScenarioModel(Model, Subject):
    def __init__(self,
                 classModel,
                 source=None,
                 name=None,
                 usecaseModel=None,
                 permissionModel=None,
                 file=None, lineNo=None,
                 docComment=None,
                 eolComment=None):
        #type: (ClassModel, Optional[SourceFile], Optional[Text], Optional[UsecaseModel], PermissionModel, Text, int) -> None
        super(ScenarioModel, self).__init__(
            source=source,
            name=name,
            lineNo=lineNo, docComment=docComment, eolComment=eolComment
        )
        self.file = file #type: Text
        self.usecaseModel=usecaseModel #type: Optional[UsecaseModel]
        self.classModel=classModel #type: ClassModel
        self.permissionModel=permissionModel #type: UCPermissionModel

        self.actorInstanceNamed = collections.OrderedDict()
        #type: Dict[Text, ActorInstance]

        self.contextBlocks=[] #type: List[ContextBlock]
        self.mainBlocks=[] #type: List[MainBlock]
        self.originalOrderBlocks=[] #type:List[Block]

        #--- evaluation
        self.scenarioEvaluation=None  # filled if evaluation exist
        #type: Optional['ScenarioEvaluation']

    @property
    def metamodel(self):
        return metamodel

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





class ActorInstance(SourceElement, Subject):
    def __init__(self, scenario, name, actor,
                 code=None, lineNo=None, docComment=None, eolComment=None):

        super(ActorInstance, self).__init__(name, code, lineNo, docComment, eolComment)
        self.scenario=scenario
        #type: ScenarioModel

        self.name=name

        self.actor=actor
        # type: Actor
        self.scenario.actorInstanceNamed[self.name]=self

    @property
    def superSubjects(self):
        return [self.actor]


metamodel = Metamodel(
    id='sc',
    label='scenario',
    extension='.scm',
    modelClass=ScenarioModel
)