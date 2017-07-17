# coding=utf-8

# TODO; it could make sense to create operations.py and may be block.py
import collections
from typing import Union, Optional, Dict, List, Text

from pyuseocl.source.sources import SourceElement

from pyuseocl.metamodel.usecases import (
    Actor,
    System,
)
from pyuseocl.metamodel.classes import (
    ClassModel,
)
from pyuseocl.metamodel.objects import (
    State,
)

from pyuseocl.metamodel.scenarios.operations import (
    StateOperation
)

from pyuseocl.metamodel.scenarios.blocks import (
    MainBlock,
    ContextBlock
)

DEBUG=3

class Scenario(object):
    def __init__(self,
                 classModel, name=None, system=None, file=None):
        #type: (ClassModel, Optional[Text], Optional[System], Text) -> None
        self.name = name #type: Optional[Text]
        self.file = file #type: Text
        self.system=system #type: Optional[System]
        self.classModel=classModel #type: ClassModel

        self.actorInstanceNamed = collections.OrderedDict()
        #type: Dict[Text,ActorInstance]

        self.mainBlocks=[] #type: List[MainBlock]
        self.contextBlocks=[] #type: List[ContextBlock]
        self.originalOrderOperations=[] #type: List[StateOperation]



    def executeAfterContext(self):
        state = State()
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
        state = State()
        env = collections.OrderedDict()
        for op in self.originalOrderOperations:
            op.execute(env, state)
        return state
    # @property
    # def operations(self):
    #     #type: ()->List[StateOperation]
    #     # _=[]
    #     # for block in self.blocks:
    #     #     for op in block.operations:
    #     #         _.append(op)
    #     _ = [
    #         op for block in self.blocks
    #            for op in block.operations]
    #     return _


class ActorInstance(SourceElement):
    def __init__(self, scenario, name, actor,
                 code=None, lineNo=None, docComment=None, eolComment=None):

        super(ActorInstance, self).__init__(name, code, lineNo, docComment, eolComment)
        self.scenario=scenario
        #type: Scenario

        self.name=name

        self.actor=actor
        # type: Actor
        self.scenario.actorInstanceNamed[self.name]=self


