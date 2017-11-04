# coding=utf-8

from abc import ABCMeta

from modelscribes.metamodels.permissions.accesses import (
    AccessSet
)
from modelscribes.metamodels.scenarios.blocks import (
    Block,
    ContextBlock,
    UsecaseInstanceBlock,
    TopLevelBlock
)
from modelscribes.metamodels.scenarios.evaluations.operations import (
    evaluateOperation,
)


# TODO: check how to create nested AccessSet so that block can have their own access set
def evaluateBlock(scenarioEvaluation, block):
    #type: ('ScenarioEvaluation', Block) -> BlockEvaluation
    if isinstance(block, ContextBlock):
        return ContextBlockEvaluation(scenarioEvaluation, block)
    elif isinstance(block, UsecaseInstanceBlock):
        return UsecaseInstanceBlockEvaluation(scenarioEvaluation, block)
    elif isinstance(block, TopLevelBlock):
        return TopLevelBlockEvaluation(scenarioEvaluation, block)
    else:
        raise NotImplementedError()


#----------------------------------------------------------------------------
#   Block evaluation
#-----------------------------------------------------------------------------

class BlockEvaluation(object):
    __metaclass__ = ABCMeta

    def __init__(self, scenarioEvaluation, block):
        #type: ('ScenarioEvaluation', Block) -> None

        self.block=block
        #type: Block
        self.block.blockEvaluation=self

        self.scenarioEvaluation=scenarioEvaluation
        #type: 'ScenarioEvaluation'

        # self.operationEvaluationByOperation = OrderedDict()
        # #type: Dict[Operation, OperationEvaluation]



        # environment and state are just modified, not stored
        # but it could be convenient to make a copy if needed

        self._eval()

    @property
    def accessSet(self):
        #type: () -> AccessSet
        return self.scenarioEvaluation.accessSet

    def _eval(self):
        for op in self.block.operations:
            opeval=evaluateOperation(self, op)
            op.operationEvaluation=opeval

    def _env(self):
        return self.scenarioEvaluation.environment

    def _state(self):
        return self.scenarioEvaluation.state


class ContextBlockEvaluation(BlockEvaluation):
    def __init__(self, scenarioEvaluation, block):
        super(ContextBlockEvaluation, self).__init__(
            scenarioEvaluation, block)


class MainBlockEvaluation(BlockEvaluation):
    __metaclass__ = ABCMeta

    def __init__(self, scenarioEvaluation, block):
        super(MainBlockEvaluation, self).__init__(
            scenarioEvaluation, block)


class UsecaseInstanceBlockEvaluation(MainBlockEvaluation):
    def __init__(self, scenarioEvaluation, block):
        super(UsecaseInstanceBlockEvaluation, self).__init__(
            scenarioEvaluation, block)


class TopLevelBlockEvaluation(MainBlockEvaluation):
    def __init__(self, scenarioEvaluation, block):
        super(TopLevelBlockEvaluation, self).__init__(
            scenarioEvaluation, block)
