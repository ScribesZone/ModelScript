# coding=utf-8
"""Metamodel package representing the evaluation of operations.
This goes with the package "stories.evaluation".

The evaluation of operations is not detailed.
That is, there is no one class for all operation evaluation.

This simplification avoids repeating the hierarchy of
Operation class, with only few additional information.

For instance instead of keeping for the deletion of an
object, the reference to this object (which depends on
the evaluation), a generic OperationStepEvaluation is
used instead.

This strategy is good enough since the details
of the evaluation of each operation is not so important.
What is important is the evaluation of "check" operations as well
as the final state (stored in the StoryEvaluation).

    StepEvaluation
    <|-- OperationStepEvaluation
         <|-- CheckStepEvaluation

"""

from typing import Optional, List, Text
from abc import ABCMeta
from modelscript.megamodels.elements import SourceModelElement
from modelscript.metamodels.permissions.sar import Subject
from modelscript.metamodels.objects import (
    ObjectModel
)
from modelscript.metamodels.stories import (
    Story,
    Step,
    TextStep,
    VerbStep,
)
from modelscript.metamodels.stories.evaluations import (
    StepEvaluation
)


class OperationStepEvaluation(StepEvaluation):
    """ The evaluation of an operation.
    Note that this class
    is concrete while OperationStep is abstract. This is
    due to the fact that we make no difference between
    many operations. OperationStepEvaluation is indeed
    instanciated for operations of all kind ; apart from
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

    frozenState: ObjectModel


    def __init__(self,
                 parent: Optional[StepEvaluation],
                 step: Step,
                 currentState: ObjectModel,
                 name: Optional[Text] = None) -> None:
        """Create a check evaluation by :
        (1) creating a (frozen) copy of the current state
        (2) making an analysis of it
        """
        super(OperationStepEvaluation, self).__init__(
            parent=parent,
            step=step,
            name=name)

        self.frozenState = currentState.copy()
        #assoc: FrozesState

        self.frozenState.checkStepEvaluation = self
        #assoc FrozesState~

        self.frozenState.finalize()

        self.frozenState.storyEvaluation=self.storyEvaluation
        self.metrics=self.frozenState.metrics

        self.storyEvaluation.checkEvaluations.append(self)
        #assoc IsCheckedAt

