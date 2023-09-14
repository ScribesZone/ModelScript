# coding=utf-8

from typing import Optional

from modelscript.base.exceptions import (
    UnexpectedCase)
from modelscript.base.printers import (
    AbstractPrinter,
    AbstractPrinterConfig)
from modelscript.metamodels.stories.evaluations import (
    StoryEvaluation,
    CompositeStepEvaluation)
from modelscript.metamodels.stories.evaluations.operations import (
    OperationStepEvaluation,
    CheckStepEvaluation)
from modelscript.scripts.stories.printer import (
    StoryPrinter)

__all__=(
    'StoryEvaluationPrinter'
)


class StoryEvaluationPrinter(AbstractPrinter):

    def __init__(self,
                 storyEvaluation: StoryEvaluation,
                 indent: int = 0,
                 config: Optional[AbstractPrinterConfig] = None):
        super(StoryEvaluationPrinter, self).__init__(
            config=config
        )
        self.storyEvaluation = storyEvaluation
        self.story = self.storyEvaluation.step
        self.indent = indent

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
            raise UnexpectedCase(  # raise:OK
                'Unexpected type: %s' % type(stepEval))

    def doStoryEvaluation(self, stepEval, indent):
        self.doCompositeStepEvaluation(stepEval, indent)
        return self.output

    def doCompositeStepEvaluation(self, stepEval, indent):
        p = StoryPrinter(
            story=self.story,
            indent=indent)
        text = p.doStep(
            step=stepEval.step,
            indent=indent,
            recursive=False)
        self.out(text, indent)
        for substep_evals in stepEval.stepEvaluations:
            self.doStepEvaluation(substep_evals, indent+1)
        return self.output

    def doOperationStepEvaluation(self, stepEval, indent):
        p = StoryPrinter(
            story=self.story,
            config=self.config,
            indent=0
        )
        text = p.doStep(
            step=stepEval.step,
            indent=0,
            recursive=False)
        self.outLine(text, removeLastEOL=True)
        if len(stepEval.issues) >= 1:
            self.outLine(self.kwd('%s issues')
                         % len(stepEval.issues))
        for a in stepEval.accesses:
            self.outLine(self.cmt(str(a)), indent=indent)

        return self.output

    def doCheckStepEvaluation(self, stepEval, indent):
        pos = {
            None: '',
            'after': '(after)',
            'before': '(before)'
        }[stepEval.step.position]
        self.outLine('%s %s' % (
                self.kwd('check'),
                self.cmt(pos)),
            indent=0)
        # self.outLine(str(stepEval.metrics), indent=indent)
        analysis_messages = stepEval.frozenState.stateCheck.messages
        self.outLine(
            self.cmt('%s analysis issues' % len(analysis_messages)),
            indent=1)
        for am in analysis_messages:
            self.outLine(
                self.cmt('-> '+am),
                indent=2)
        return self.output


def StoryBestPrinter(
        story,
        storyEvaluation=None,
        config=None,
        useStory=False,
        indent=0,
        forceStory=False):
    """Returns the most appropriate printer among the
    evaluation printer and regular story printer.
    """
    chosen_story = (
        storyEvaluation is None
        or useStory)
    if chosen_story or forceStory:
        return StoryPrinter(
            story=story,
            indent=indent,
            config=config)
    else:
        return StoryEvaluationPrinter(
            storyEvaluation=storyEvaluation,
            indent=indent,
            config=config
        )
