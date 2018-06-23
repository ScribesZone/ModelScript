# coding=utf-8
"""
Code of the Scenario metamodel.

The global structure of this metamodel is as following::

TODO: UPDATE

    StepEvaluation
    <|-- CompositeEvaluation
        <>--* StepEvaluation
    <|-- OperationEvaluation

"""

from typing import Optional, List, Text
from abc import ABCMeta
from modelscripts.megamodels.elements import SourceModelElement
from modelscripts.metamodels.permissions.sar import Subject


from modelscripts.metamodels.stories import (
    Story,
    Step,
    TextStep,
    VerbStep,
)
from modelscripts.metamodels.stories.evaluations import (
    StepEvaluation
)
# from modelscripts.metamodels.stories.operations import (
#     ObjectCreationStep,
#     ObjectDeletionStep,
#     SlotStep,
#     LinkCreationStep,
#     LinkDeletionStep,
#     CheckStep,
#     ReadStep
# )
# from modelscripts.metamodels.objects import (
#     ObjectModel,
#     Object,
#     Slot,
#     Link,
#     LinkObject
# )


class OperationStepEvaluation(StepEvaluation):
    """
    The evaluation of an operation. Note that this class
    is concrete while OperationStep is abstract. This is
    due to the fact that we make no difference between
    many operations.
    """

    def __init__(self,
                 parent,
                 step,
                 name=None):
        super(OperationStepEvaluation, self).__init__(
            parent=parent,
            step=step,
            name=name)

class CheckStepEvaluation(OperationStepEvaluation):
    pass

