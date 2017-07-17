# coding=utf-8

from typing import Union, Optional, Dict, List, Text
from abc import ABCMeta, abstractmethod
from pyuseocl.source.sources import SourceElement

from pyuseocl.metamodel.scenarios.operations import (
    StateOperation,
)
from pyuseocl.metamodel.accesses import (
    AccessSet,
)


class Block(SourceElement):
    __metaclass__ = ABCMeta

    def __init__(self, scenario, lineNo=None):
        #type: ('Scenario', Optional[int])->None
        super(Block, self).__init__(name=None, lineNo=lineNo)

        self.scenario=scenario

        self.operations=[]  #type: List[StateOperation]

        self.accessSet=AccessSet(self)    #type: AccessSet
        #: filled after execution

class ContextBlock(Block):
    def __init__(self, scenario, lineNo=None):
        #type: ('Scenario',Optional[int])->None
        super(ContextBlock, self).__init__(scenario, lineNo)
        self.scenario.contextBlocks.append(self)


class MainBlock(Block):
    __metaclass__ = ABCMeta

    def __init__(self, scenario, lineNo=None):
        #type: ('Scenario',Optional[int])->None
        super(MainBlock, self).__init__(scenario, lineNo)
        self.scenario.mainBlocks.append(self)


class UsecaseInstanceBlock(MainBlock):
    def __init__(self, scenario, actorInstance, useCase, lineNo=None):
        #type: ('Scenario', 'ActorInstance', Usecase, Optional[int]) -> None
        super(UsecaseInstanceBlock, self).__init__(scenario,lineNo=lineNo)
        self.actorInstance=actorInstance
        self.useCase=useCase


class TopLevelBlock(MainBlock):
    def __init__(self, scenario, lineNo=None):
        super(TopLevelBlock, self).__init__(scenario, lineNo=lineNo)


from pyuseocl.metamodel.usecases import (
    Usecase,
)

