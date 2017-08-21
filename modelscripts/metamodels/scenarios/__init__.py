# coding=utf-8
"""
Code of the Scenario metamodel.

The structure of this module is::

    ScenarioModel
    <>--* ActorInstanceNamed
    <>--* ContextBlock
    <>--* MainBlock
    <>--* Operation

"""

# TODO: add support for  'include <x.obm>

import collections
from typing import Union, Optional, Dict, List, Text

from modelscripts.source.sources import (
    SourceFile,
    SourceElement
)
from modelscripts.utils import Model

from modelscripts.metamodels.classes import (
    ClassModel,
)
from modelscripts.metamodels.usecases import (
    Actor,
    UsecaseModel,
)
from modelscripts.metamodels.objects import (
    ObjectModel,
)

from modelscripts.metamodels.scenarios.operations import (
    Operation
)

from modelscripts.metamodels.scenarios.blocks import (
    MainBlock,
    ContextBlock
)

DEBUG=3

class ScenarioModel(Model):
    def __init__(self,
                 classModel, source=None, name=None, usecaseModel=None, file=None, lineNo=None):
        #type: (ClassModel, Optional[SourceFile], Optional[Text], Optional[UsecaseModel], Text) -> None
        super(ScenarioModel, self).__init__(
            source=source,
            name=name,
            lineNo=lineNo,
        )
        # self.name = name #type: Optional[Text]
        self.file = file #type: Text
        self.usecaseModel=usecaseModel #type: Optional[UsecaseModel]
        self.classModel=classModel #type: ScenarioModel

        self.actorInstanceNamed = collections.OrderedDict()
        #type: Dict[Text,ActorInstance]

        self.contextBlocks=[] #type: List[ContextBlock]
        self.mainBlocks=[] #type: List[MainBlock]
        self.originalOrderOperations=[] #type: List[Operation]

    @property
    def actorInstances(self):
        return self.actorInstanceNamed.values()

    @property
    def actorInstanceNames(self):
        return self.actorInstanceNamed.keys()

    def executeAfterContext(self):
        state = ObjectModel()
        env = collections.OrderedDict()
        # execute context
        for cb in self.contextBlocks:
            for op in cb.operations:
                op.execute(env, state)
        # execute main blocks
        for mb in self.mainBlocks:
            for op in mb.operations:
                op.execute(env, state)


    def execute(self):
        state = ObjectModel()
        env = collections.OrderedDict()
        for op in self.originalOrderOperations:
            op.execute(env, state)
        return state



class ActorInstance(SourceElement):
    def __init__(self, scenario, name, actor,
                 code=None, lineNo=None, docComment=None, eolComment=None):

        super(ActorInstance, self).__init__(name, code, lineNo, docComment, eolComment)
        self.scenario=scenario
        #type: ScenarioModel

        self.name=name

        self.actor=actor
        # type: Actor
        self.scenario.actorInstanceNamed[self.name]=self


