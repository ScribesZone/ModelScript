# coding=utf-8

"""
Meta elements resulting from aa scenario evaluation.
Information come from different sources:
- CardinalityEvaluation come from the trace of USE OCL execution
- InvariantEvaluation come from the trace of USE OCL execution
- BlockEvaluation come from abstract execution of operation
  (evaluate() on Operation)

THE DIAGRAM BELOW SEEMS TO BE OBSOLETE :
the Check/QueryEvaluation are in fact directly under
the corresponding operations

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
from modelscripts.megamodels.models import (
    ModelElement
)
from modelscripts.metamodels.objects import (
    ObjectModel,
    Object
)
from modelscripts.metamodels.scenarios.blocks import (
    Block,
)
from modelscripts.metamodels.scenarios.evaluations.blocks import (
    BlockEvaluation,
    evaluateBlock,
)
from modelscripts.metamodels.scenarios.evaluations.operations import (
    OperationEvaluation,
)
from modelscripts.metamodels.permissions.gpermissions import PermissionSet

from modelscripts.metamodels.permissions.accesses import (
    AccessSet
)

META_CLASSES=[
    'ScenarioEvaluation',
]

__all__=META_CLASSES

# TODO: Change comment, remove dead code, etc.
#       This should lead to a general metamodel (conformance ?)






#------------------------------------------------------------------------------
#   Class Model level
#------------------------------------------------------------------------------


class ScenarioEvaluation(ModelElement):
    """
    Result of the evaluation of a scenario in the context of
    a class model. Contains results of the evaluation::

    * query results
    * invariant results
    * cardinality results
    """


    def __init__(self, scenario):
        #type: ('ScenarioModel') -> None
        """ Create an "Empty" model. It will be filled by .evaluate() """

        ModelElement.__init__(
            self,
            model=scenario
        )
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

    # @property
    # def model(self):
    #     return self.scenario.model

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

