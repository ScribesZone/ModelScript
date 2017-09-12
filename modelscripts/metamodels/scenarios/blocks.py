# coding=utf-8
"""
Metamodel elements for block of operations.
Part of the Scenario metamodel.
"""

from abc import ABCMeta

from typing import Optional, List

from modelscripts.base.sources import SourceElement
from modelscripts.metamodels.permissions.sar import Subject
from modelscripts.metamodels.scenarios.operations import (
    Operation,
)


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






