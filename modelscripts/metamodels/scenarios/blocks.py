# coding=utf-8
"""
Metamodel elements for block of operations.
Part of the Scenario metamodel.
"""

from typing import Union, Optional, Dict, List, Text
from abc import ABCMeta, abstractmethod
from modelscripts.sources.sources import SourceElement

from modelscripts.metamodels.scenarios.operations import (
    Operation,
)
from modelscripts.metamodels.permissions import Subject, AccessSet


class Block(SourceElement, Subject):
    __metaclass__ = ABCMeta

    def __init__(self, scenario, lineNo=None):
        #type: ('Scenario', Optional[int])->None
        super(Block, self).__init__(name=None, lineNo=lineNo)

        self.scenario=scenario

        self.operations=[]  #type: List[Operation]

        self.scenario.originalOrderBlocks.append(self)

        #--- evaluation
        self.blockEvaluation=None  # filled if evaluation

    @property
    def superSubjects(self):
        return [self.scenario]




class ContextBlock(Block, Subject):
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


class TopLevelBlock(MainBlock):
    def __init__(self, scenario, lineNo=None):
        super(TopLevelBlock, self).__init__(scenario, lineNo=lineNo)

class UsecaseInstanceBlock(MainBlock):
    def __init__(self, scenario, actorInstance, useCase, lineNo=None):
        #type: ('Scenario', 'ActorInstance', 'Usecase', Optional[int]) -> None
        super(UsecaseInstanceBlock, self).__init__(scenario,lineNo=lineNo)
        self.actorInstance=actorInstance
        self.useCase=useCase

    @property
    def superSubjects(self):
        return super(UsecaseInstanceBlock, self).superSubjects + [self.actorInstance, self.useCase]






