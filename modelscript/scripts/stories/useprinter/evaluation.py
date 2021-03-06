# coding=utf-8

from typing import Optional

from modelscript.base.printers import (
    AbstractPrinter,
    AbstractPrinterConfig,
    Styles
)

from modelscript.metamodels.stories.evaluations import (
    StoryEvaluation,
    CompositeStepEvaluation
)
from modelscript.metamodels.stories.evaluations.operations import (
    OperationStepEvaluation,
    CheckStepEvaluation
)
from modelscript.scripts.stories.printer import (
    StoryPrinter
)


__all__=(
    'StoryEvaluationPrinter'
)


class StoryEvaluationPrinter(AbstractPrinter):

    def __init__(self,
                 storyEvaluation,
                 indent=0,
                 config=None):
        #type: (StoryEvaluation, int, Optional[AbstractPrinterConfig]) -> None
        super(StoryEvaluationPrinter, self).__init__(
            config=config
        )
        self.storyEvaluation=storyEvaluation
        self.story=self.storyEvaluation.step
        self.indent=indent

    def do(self):
        self.doStepEvaluation(
            self.storyEvaluation,
            indent=self.indent)
        return self.output

    def doStepEvaluation(self, stepEval, indent):
        if isinstance(stepEval, StoryEvaluation):
            self.doStoryEvaluation(stepEval, indent)
        elif isinstance(stepEval, CompositeStepEvaluation):
            self.doStoryEvaluation(stepEval, indent)
        elif isinstance(stepEval, CheckStepEvaluation):
            self.doCheckStepEvaluation(stepEval, indent)
        elif isinstance(stepEval, OperationStepEvaluation):
            self.doOperationStepEvaluation(stepEval, indent)
        else:
            raise NotImplementedError('Unexpected type: %s' %
                                      type(stepEval))

    def doStoryEvaluation(self, stepEval, indent):
        self.doCompositeStepEvaluation(stepEval, indent)
        return self.output

    def doCompositeStepEvaluation(self, stepEval, indent):
        p=StoryPrinter(
            story=self.story,
            indent=indent
        )
        text=p.doStep(
            step=stepEval.step,
            indent=indent,
            recursive=False)
        self.out(text, indent)
        for substep_evals in stepEval.stepEvaluations:
            self.doStepEvaluation(substep_evals, indent+1)
        return self.output

    def doOperationStepEvaluation(self, stepEval, indent):
        p=StoryPrinter(
            story=self.story,
            indent=indent
        )
        text=p.doStep(
            step=stepEval.step,
            indent=indent,
            recursive=False)
        self.out(text, indent)
        if len(stepEval.issues)>=1:
            self.outLine(self.kwd('%s issues')
                         % len(stepEval.issues))
        for a in stepEval.accesses:
            self.outLine(self.kwd(a), indent+1)

        return self.output

    def doCheckStepEvaluation(self, stepEval, indent):
        self.outLine('CHECK ---------------- >>>', indent)
        self.outLine(str(stepEval.metrics), indent)
        analysis_messages=stepEval.frozenState.stateCheck.messages
        self.outLine('%s analysis issues' % len(analysis_messages))
        self.outLine('\n    ->  '.join(analysis_messages))
        return self.output


def StoryBestPrinter(
        story,
        storyEvaluation=None,
        useStory=False,
        indent=0):
    """
    Return the most appropriate printer among the
    evaluation printer and regular story printer.
    If the storyEvaluation is None or useStory is True
    then select the StoryPrinter, otherwise select
    StoryEvaluationPrinter.
    """
    choosen_story=(
        storyEvaluation is None
        or useStory)
    if choosen_story:
        return StoryPrinter(
            story=story,
            indent=indent)
    else:
        return StoryEvaluationPrinter(
            storyEvaluation=storyEvaluation,
            indent=indent
        )
