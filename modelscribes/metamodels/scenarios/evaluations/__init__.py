# coding=utf-8

"""
Meta elements for modeling results of a scenario evaluation.
Information come from different sources:
- CardinalityEvaluation come from USE OCL execution
- InvariantEvaluation come from USE OCL execution
- BlockEvaluation come from abstract execution (evaluate on Operation)

The structure of the metamodel is::

    ScenarioEvaluation
    <>--* CheckEvaluation   (soil command "check")
          <>--* CardinalityEvaluation
                <|-- CardinalityViolation
          <>--* InvariantEvaluation
                <|-- InvariantValidation
                <|-- InvariantViolation
    <>--* QueryEvaluation   (soil command "??")
    <>--* BlockEvaluation   (with accessModel)
          ----> Block
          ----> AccessSet
"""
from __future__ import print_function, division

from collections import OrderedDict

from typing import Text, Dict

from modelscribes.metamodels.objects import (
    ObjectModel,
    Object
)
# from modelscribes.metamodels.scenarios import (
#     ScenarioModel
# )
from modelscribes.metamodels.scenarios.blocks import (
    Block,
)
from modelscribes.metamodels.scenarios.evaluations.blocks import (
    BlockEvaluation,
    evaluateBlock,
)
from modelscribes.metamodels.scenarios.evaluations.operations import (
    OperationEvaluation,
)
from modelscribes.metamodels.permissions.gpermissions import PermissionSet

from modelscribes.metamodels.permissions.accesses import (
    AccessSet
)

__all__=(
    'ScenarioEvaluation',
)
# TODO: Change comment, remove dead code, etc.
#       This should lead to a general metamodel (conformance ?)






#------------------------------------------------------------------------------
#   Class Model level
#------------------------------------------------------------------------------


class ScenarioEvaluation(object):
    """
    Result of the evaluation of a scenario in the context of
    a class model. Contains results of the evaluation::

    * query results
    * invariant results
    * cardinality results

    """

    # @classmethod
    # def evaluate(cls, scenario, originalOrder=True):
    #     #type: (ScenarioModel, bool) -> None
    #     if scenario.scenarioEvaluation is None:
    #         scenario.scenarioEvaluation = ScenarioEvaluation(
    #             scenario=scenario,
    #             originalOrder=originalOrder
    #         )

    def __init__(self, scenario):
        #type: ('ScenarioModel') -> None
        """ Create an "Empty" model. It will be filled by .evaluate() """

        self.isEvaluated = False
        self.scenario = scenario  #type: 'ScenarioModel'
        self.scenario.scenarioEvaluation = self

        self.originalOrder = None  #type: Optional[bool]
        # This will be known when the evaluation is done y evaluate()

        self.blockEvaluationByBlock = OrderedDict()
        #type: Dict[Block, BlockEvaluation]

        self.environment = OrderedDict()
        #type: Dict[Text, Object]
        #: Final state.
        #: This attribute is set by _eval
        #: It will be the final environment at the end

        self.state = ObjectModel()
        #type: ObjectModel
        #: Final state.
        #: This attribute is set by _eval
        #: It will be the final state at the end

        self.permissionSet = (
            None if scenario.permissionModel is None
            else scenario.permissionModel.permissionSet)
        #type: Optional(PermissionSet)

        #: The permission set to control the operation access

        self.accessSet=AccessSet(
            permissionSet=self.permissionSet)


    def evaluate(self, originalOrder=True):
        #type: ('ScenarioModel', bool) -> None
        if self.originalOrder is not None and self.originalOrder!=originalOrder:
            # raise an ValueError if evaluate is called more than
            # twice or more but with different evaluation order
            raise ValueError('Inconsistent use of ScenarioModel.evaluate()')
        if not self.isEvaluated:
            if self.originalOrder:
                blocks = self.scenario.originalOrderBlocks
            else:
                blocks = self.scenario.logicalOrderBlocks
            for block in blocks:
                blockeval = evaluateBlock(self, block)
                self.blockEvaluationByBlock[block]=blockeval
        self.isEvaluated=True

