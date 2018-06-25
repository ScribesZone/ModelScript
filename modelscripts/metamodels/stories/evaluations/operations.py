# coding=utf-8
"""
Metamodel package representing the evaluation of operations.
This goes with stories.evaluation.
The evaluation of operation is not detailled, one operation
after each other. This avoids repeating the hierarchy of
Operation class, with only few additional information.
For instance instead of keeping for the deletion of an
object, the reference to this object (which depends on
the evaluation), a generic OperationStepEvaluation is
used instead. This is due to the fact that the details
of the evaluation is not so important. What is important
is the evaluation of "check" operations and the
final state (stored in the StoryEvaluation).

    StepEvaluation
    <|-- OperationStepEvaluation
         <|-- CheckStepEvaluation

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


class OperationStepEvaluation(StepEvaluation):
    """
    The evaluation of an operation. Note that this class
    is concrete while OperationStep is abstract. This is
    due to the fact that we make no difference between
    many operations. OperationStepEvaluation are
    indeed instanciated for all operations apart
    CheckStep which contains interesting information.
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

