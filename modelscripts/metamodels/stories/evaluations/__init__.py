# coding=utf-8
"""
Code of the Scenario metamodel.

The global structure of this metamodel is as following::

    StepEvaluation
    <|-- CompositeEvaluation
        <>--* StepEvaluation
    <|-- OperationEvaluation



TODO: TO UPDATE OR REOVE
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
    ----- evaluate()
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

from typing import Optional, List, Text
from abc import ABCMeta
from modelscripts.megamodels.elements import SourceModelElement
from modelscripts.metamodels.permissions.sar import Subject
from modelscripts.metamodels.permissions.accesses import (
    AccessSet,
    Access
)
from modelscripts.base.issues import (
    Issue
)

from modelscripts.metamodels.stories import (
    # Story,
    Step,
    # TextStep,
    # VerbStep,
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
        #type: StepEvaluation
        # Origin of this evaluation.
        # This is always defined.

        self.parent=parent
        #type: Optional[CompositeStepEvaluation]
        # The parent evaluation.
        # Not defined in the case of StoryEvaluation as this is the root.
        # This parent mimics steps' parent, but it is
        # necessary and cannot be replaced by navigation through
        # because there are potentially many
        # StepEvaluation per step.

        self.name=name
        #type: Optional[Text]
        # An optional name for the evaluation. For further
        # usage. It could be for instance the name of a
        # scenario for a story, or a label given to a step.
        # The name is used by subjectLabel

        self.accesses=accesses
        #type: List[Access]
        # TODO: check how it work
        # Not sure if it sould be on leaf steps or composite as well.

        self.issues=[]
        #type: List[Issue]

        if parent is not None:
            self.parent.stepEvaluations.append(self)

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
            #type: List[Step]


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

        self.finalState=None
        # This will be filled by the evaluator, at the end of the eval.
