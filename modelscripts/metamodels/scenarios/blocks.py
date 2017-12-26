# coding=utf-8
"""
Metamodel elements for block of operations.
Part of the Scenario metamodel.
"""

from abc import ABCMeta

from typing import Optional, List

from modelscripts.metamodels.permissions.sar import Subject
from modelscripts.metamodels.scenarios.operations import (
    Operation,
)

from modelscripts.megamodels.elements import SourceModelElement

META_CLASSES=[
    'Block',
    'ContextBlock',
    'MainBlock',
    'TopLevelBlock',
    'UsecaseInstanceBlock'
]
__all__=META_CLASSES


class Block(SourceModelElement, Subject): # should be top level but this create a import cycle
    __metaclass__ = ABCMeta

    def __init__(self, model, lineNo=None):
        #type: ('Scenario', Optional[int])->None

        self.scenario=model

        SourceModelElement.__init__(self,
            model=self.scenario,
            name=None,
            lineNo=lineNo)


        self.operations=[]  #type: List[Operation]

        self.scenario.originalOrderBlocks.append(self)

        #--- evaluation
        self.blockEvaluation=None  # filled if evaluation

    @property
    def superSubjects(self):
        return [self.scenario]


class ContextBlock(Block, Subject):
    META_COMPOSITIONS=[
        'operations',
    ]

    def __init__(self, model, lineNo=None):
        #type: ('Scenario',Optional[int])->None
        super(ContextBlock, self).__init__(model, lineNo)
        self.scenario.contextBlocks.append(self)


class MainBlock(Block):
    __metaclass__ = ABCMeta

    def __init__(self, model, lineNo=None):
        #type: ('Scenario',Optional[int])->None
        super(MainBlock, self).__init__(model, lineNo)
        self.scenario.mainBlocks.append(self)


class TopLevelBlock(MainBlock):
    META_COMPOSITIONS=[
        'operations',
    ]

    def __init__(self, model, lineNo=None):
        super(TopLevelBlock, self).__init__(model, lineNo=lineNo)

class UsecaseInstanceBlock(MainBlock):
    META_COMPOSITIONS=[
        'operations',
    ]

    def __init__(self, model, actorInstance, useCase, lineNo=None):
        #type: ('Scenario', 'ActorInstance', 'Usecase', Optional[int]) -> None
        super(UsecaseInstanceBlock, self).__init__(model,lineNo=lineNo)
        self.actorInstance=actorInstance
        self.useCase=useCase

    @property
    def superSubjects(self):
        return super(UsecaseInstanceBlock, self).superSubjects + [self.actorInstance, self.useCase]




