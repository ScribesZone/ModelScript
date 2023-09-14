# coding=utf-8
"""Model elements resulting from the evaluation of a story.
Each StepEvaluation is associated with the Step at its origin.
Each StepEvaluation additionally has :
    * a list of issues that the evaluation raise for this step
    * a list of accesses made by the step.

While steps are syntactical elements and have various elements
unbound (e.g. ('x', A, 'y')) these elements are then bound in
evaluation steps (e.g. x and y have been resolved).

However, the result of the binding for each step is not stored
because:
    * this avoid to have a evaluation class for each step class
      (e.g. ObjectCreation -> ObjectCreationEvaluation),
    * the binding itself is not so important,
    * what is important is the result of the step evaluation.

Instead of having specialized step evaluation for each step
(e.g. ObjectCreationEvaluation) a generic StepEvaluation is used.

The global structure of this metamodel package is as following::

    StepEvaluation
    --->1 Step (step)
    --->* Access
    --->* Issue
    <---> 0..1 CompositeStepEvaluation (parent)

    StepEvaluation
    <|-- CompositeStepEvaluation
        <>--* StepEvaluation (stepEvaluations)
        <|-- StoryEvaluation
            ----1 ObjectModel (finalState)
    <|-- IncludeEvaluation
        ----1 Story
    <|-- OperationStepEvaluation  (see "operations" package)


The evaluation hierarchy goes in "parallel" with the step
hierarchy, with the same parent relationship but in parallel.
There is simplfy less-typed nodes, one unique type for all operation
steps.
"""

from typing import Optional, List, Text
from abc import ABCMeta
from modelscript.megamodels.elements import SourceModelElement
from modelscript.metamodels.permissions.sar import Subject
from modelscript.metamodels.permissions.accesses import (
    Access
)
from modelscript.base.issues import (
    Issue
)

from modelscript.metamodels.stories import (
    Step,
)


class StepEvaluation(SourceModelElement, Subject, metaclass=ABCMeta):
    """The evaluation of a step. """

    step: Step
    """Step at the origin of this evaluation.
    The "step" is always defined as all StepEvaluations result from
    a Step. The opposite of this reference is not stored and
    not really useful since a Step can have various StepEvaluation.
    """

    parent: Optional['CompositeStepEvaluation']
    """The parent evaluation.
    Not defined in the case of StoryEvaluation as this is the root.
    This parent mimics steps' parent, but it is
    necessary and cannot be replaced by navigation through
    because there are potentially many StepEvaluation per step
    so the parent may not be the same in different evaluation."""

    name: Optional[Text]
    """An optional name for the evaluation. 
    For further usage. It could be for instance the name of a
    scenario for a story, or a label given to a step.
    The name is used by subjectLabel """
    # TODO:4 this attribute should better go to Story
    #   Not sure why this attribute got here.
    #   Make more sense to have

    issues: List[Issue]

    accesses: List[Access]
    # TODO 3 check if accesses works
    #        Not sure if it should be on leaf steps or composite as well

    def __init__(self,
                 parent: Optional['CompositeStepEvaluation'],
                 step: Step,
                 accesses: List[Access] = [],
                 name: Optional[Text] = None):
        super(StepEvaluation, self).__init__(
            model=step.model,
            name=None,
            astNode=step.astNode,
            lineNo=step.lineNo,
            description=step.description)

        self.step = step
        self.parent = parent
        self.name = name
        self.accesses = accesses
        self.issues = []
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
    def superSubjects(self) -> List[Subject]:
        # Wrt to access control, the evaluation is related
        # to the corresponding step. Not to the hierarchy of
        # evaluation which is not really meaningful.
        return self.step.superSubjects

    @property
    def subjectLabel(self):
        # the label is the same as the step label + a opt name.
        # In principle we should add a label for the
        return '%s%s' % (
            '' if self.name is None else self.name,
            self.step.subjectLabel)


class CompositeStepEvaluation(StepEvaluation):

    stepEvaluations: List[StepEvaluation]
    """Composite evaluations have substeps "stepEvaluations".
    On the opposite, all step evaluation have parents
    (see stepEvaluation).
    """
    def __init__(self, parent, step):
        super(CompositeStepEvaluation, self).__init__(
            parent=parent,
            step=step)

        self.stepEvaluations = []



class StoryEvaluation(CompositeStepEvaluation):
    """
    The evaluation of the story.
    This particular case of CompositeStepEvaluation is
    (1) handy for typing at the story level
    (2) contains a reference to the object model
        created by the evaluation
    Although Story (not StoryEvaluation) are always at the top level,
    StoryEvaluation can be nested in some other StoryEvaluation
    through the include mechanism. In this case "parent" is not None.
    Story evaluations have CheckEvaluations
    """

    checkEvaluations: List['CheckStepEvaluation']

    def __init__(self, step, parent=None):
        super(StoryEvaluation, self).__init__(
            parent=parent,
            step=step)

        self.checkEvaluations = []

    # @property
    # def finalState(self):
    #     fs = self.checkEvaluations[-1].frozenState
    #     return fs


class StoryIncludeEvaluation(CompositeStepEvaluation):
    """The evaluation of an include.
    This evaluations references a story evaluation.
    This story evaluation is also stored as a sub-step
    since the parent of the story evaluation is the include.
    This is why this class inherits from CompositeStepEvaluation.
    """

    storyEvaluationIncluded: Optional[StoryEvaluation]

    def __init__(self, parent, step):
        super(StoryIncludeEvaluation, self).__init__(
            parent=parent,
            step=step)

        self.storyEvaluationIncluded = None
        # This value is not set directly by the constructor
        # but it is set just after. See _eval_include
