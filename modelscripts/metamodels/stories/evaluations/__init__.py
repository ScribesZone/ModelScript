# coding=utf-8
"""
Model elements resulting from the evaluation of a story.
The global structure of this metamodel package is as following::

    StepEvaluation
    --->1 Step (step)
    --->* Access
    --->* Issue
    <--->0..1 StepEvaluation (parent)

    StepEvaluation
    <|-- CompositeStepEvaluation
        <>--* StepEvaluation (stepEvaluations)
        <|-- StoryEvaluation
            ----1 ObjectModel (finalState)
    <|-- OperationStepEvaluation  (see "operations" package)


The evaluation hierarchy goes in "parallel" with the step
hierarchy, with the same parent relationship but in parallel.
"""

from typing import Optional, List, Text
from abc import ABCMeta
from modelscripts.megamodels.elements import SourceModelElement
from modelscripts.metamodels.permissions.sar import Subject
from modelscripts.metamodels.permissions.accesses import (
    Access
)
from modelscripts.base.issues import (
    Issue
)

from modelscripts.metamodels.stories import (
    Step,
)


class StepEvaluation(SourceModelElement, Subject):
    """
    The evaluation of a step.
    """
    __metaclass__ = ABCMeta

    def __init__(self,
                 parent,
                 step,
                 accesses=[],
                 name=None):
        #type: (Optional[CompositeStepEvaluation], Step, List[Access], Optional[Text]) -> None
        super(StepEvaluation, self).__init__(
            model=step.model,
            name=None,
            astNode=step.astNode,
            lineNo=step.lineNo,
            description=step.description)

        self.step=step
        #type: Step
        # Step at the origin of this evaluation.
        # The "step" is always defined as all StepEvaluations result from
        # a Step. The opposite of this reference is not stored and
        # not really useful since a Step can have various StepEvaluation.

        self.parent=parent
        #type: Optional[CompositeStepEvaluation]
        #assoc: HasParentEvaluation

        # The parent evaluation.
        # Not defined in the case of StoryEvaluation as this is the root.
        # This parent mimics steps' parent, but it is
        # necessary and cannot be replaced by navigation through
        # because there are potentially many StepEvaluation per step
        # so the parent may not be the same in different evaluation.

        self.name=name
        #type: Optional[Text]
        # TODO: seems that this should better go to the StoryEvaluation ?
        # An optional name for the evaluation. For further
        # usage. It could be for instance the name of a
        # scenario for a story, or a label given to a step.
        # The name is used by subjectLabel

        self.accesses=accesses
        #type: List[Access]
        #assoc: Accesses
        # TODO: check how it works
        # Not sure if it should be on leaf steps or composite as well.

        self.issues=[]
        #type: List[Issue]
        #assoc: hasIssues
        # The list of issues raised by this step evaluation

        if self.parent is not None:
            self.parent.stepEvaluations.append(self)

    @property
    def storyEvaluation(self):
        if self.parent is None:
            # This object is the storyEvaluation
            return self
        else:
            return self.parent.storyEvaluation

    @property
    def superSubjects(self):
        # type: () -> List[Subject]
        # Wrt to access control, the evaluation is related
        # to the corresponding step. Not to the hierarchy of
        # evaluation which is not really meaningful.
        return self.step.superSubjects

    @property
    def subjectLabel(self):
        # the label is the same as the step label + a opt name.
        # In principle we should add a label for the
        #
        return '%s%s' % (
            '' if self.name is None else self.name,
            self.step.subjectLabel)


class CompositeStepEvaluation(StepEvaluation):

    def __init__(self, parent, step):
        super(CompositeStepEvaluation, self).__init__(
            parent=parent,
            step=step)

        self.stepEvaluations=[]
        #type: List[StepEvaluation]
        #assoc: HasParentEvaluation
        # Composite evaluations have substeps "stepEvaluations".
        # On the opposite, all step evaluation have parents
        # (see stepEvaluation).


class StoryEvaluation(CompositeStepEvaluation):
    """
    The evaluation of the story.
    This particular case of CompositeStepEvaluation is
    (1) handy for typing at the story level
    (2) contains a reference to the object model created by the evaluation
     """
    def __init__(self, step):
        super(StoryEvaluation, self).__init__(
            parent=None,
            step=step)

        self.checkEvaluations=[]
        #type: List['CheckStepEvaluation']
        #assoc: IsCheckedAt

    @property
    def finalState(self):
        return self.checkEvaluations[-1].frozenState