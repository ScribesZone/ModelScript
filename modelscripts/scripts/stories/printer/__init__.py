# coding=utf-8
"""

"""
from __future__ import unicode_literals, print_function, absolute_import, division
from typing import Optional

from modelscripts.base.printers import (
    AbstractPrinter,
    AbstractPrinterConfig,
    Styles
)

from modelscripts.metamodels.stories import (
    Story,
    TextStep,
    VerbStep,
    IncludeStep,
)
from modelscripts.metamodels.stories.operations import (
    ObjectCreationStep,
    ObjectDeletionStep,
    SlotStep,
    LinkCreationStep,
    LinkDeletionStep,
    LinkObjectCreationStep,
    CheckStep,
    ReadStep
)


from modelscripts.scripts.textblocks.printer import (
    TextBlockPrinter
)

__all__=(
    'StoryEvaluationPrinter'
)
class StoryPrinter(AbstractPrinter):


    def __init__(self,
                 story,
                 indent=0,
                 config=None):
        #type: (Story, int, Optional[AbstractPrinterConfig]) -> None
        super(StoryPrinter, self).__init__(
            config=config
        )

        self.story=story
        self.indent=indent

    def do(self):
        self.doStory(
            self.story,
            indent=self.indent,
            recursive=True)
        return self.output


    def doStep(self, step, indent, recursive=True):
        if isinstance(step, Story):
            return self.doStory(step, indent, recursive=recursive)
        elif isinstance(step, IncludeStep):
            return self.doIncludeStep(step, indent)
        elif isinstance(step, VerbStep):
            return self.doVerbStep(step, indent, recursive=recursive)
        elif isinstance(step, TextStep):
            return self.doTextStep(step, indent, recursive=recursive)
        elif isinstance(step, ObjectCreationStep):
            return self.doObjectCreationStep(step, indent)
        elif isinstance(step, ObjectDeletionStep):
            return self.doObjectDeletionStep(step, indent)
        elif isinstance(step, SlotStep):
            return self.doSlotStep(step, indent)
        elif isinstance(step, LinkCreationStep):
            return self.doLinkCreationStep(step, indent)
        elif isinstance(step, LinkDeletionStep):
            return self.doLinkDeletionStep(step, indent)
        elif isinstance(step, LinkObjectCreationStep):
            return self.doLinkObjectCreationStep(step, indent)
        elif isinstance(step, CheckStep):
            return self.doCheck(step, indent)
        else:
            raise NotImplementedError(
                'Unexpected step. type=:"%s"' % step)

    def doVerbStep(self, step, indent, recursive=True):
        self.outLine(
            '%s %s %s' % (
                step.subjectName,
                self.kwd('do'),
                step.verbName
            ),
            indent=indent
        )
        if recursive:
            self._doSubsteps(step, indent+1, recursive=recursive)
        return self.output

    def doIncludeStep(self, step, indent):
        # TODO: does not display kwd properly.
        self.outLine(
            '%s %s' % (
                self.kwd('include'),
                ' '.join(step.words)),
            indent=indent
        )
        return self.output


    def doTextStep(self, step, indent, recursive=True):
        tbp=TextBlockPrinter(step.textBlock, indent=indent)
        text=tbp.do()
        self.outLine(text)
        if recursive:
            self._doSubsteps(step, indent+1, recursive=recursive)
        return self.output

    def doStory(self, step, indent, recursive=True):
        # do something if necessary, link printing story name

        if recursive:
            self._doSubsteps(
                step,
                indent, # no additionaly indent for story steps
                recursive=recursive)
        return self.output

    def _doSubsteps(self, compositeStep, indent, recursive=True):
        for substep in compositeStep.steps:
            self.doStep(substep, indent, recursive=recursive)
        return self.output

    def doObjectCreationStep(self, step, indent):
        action='create ' if step.isAction else ''
        self.outLine(
            '%s%s %s %s' % (
                self.kwd(action),
                step.objectName,
                self.kwd(':'),
                step.class_.name),
            indent=indent
        )
        return self.output

    def doObjectDeletionStep(self, step, indent):
        action='delete ' if step.isAction else ''
        self.outLine(
            '%s%s' % (
                self.kwd(action),
                step.objectName),
            indent=indent
        )
        return self.output

    def doSlotStep(self, step, indent):
        if step.isAction and step.isUpdate:
            action='update '
        elif step.isAction and not step.isUpdate:
            action='set '
        else:
            action=''
        self.outLine(
            '%s%s%s%s %s %s' % (
                self.kwd(action),
                step.objectName,
                self.kwd('.'),
                step.attributeName,
                self.kwd('='),
                str(step.simpleValue)),
            indent=indent)
        return self.output

    def doLinkCreationStep(self, step, indent):
        action='create ' if step.isAction else ''
        self.outLine(
            # create (a,R,b)
            '%s%s%s%s%s%s%s%s' % (
                self.kwd(action),
                self.kwd('('),
                step.sourceObjectName,
                self.kwd(','),
                step.association,
                self.kwd(','),
                step.targetObjectName,
                self.kwd(')')),
            indent=indent)
        return self.output

    def doLinkDeletionStep(self, step, indent):
        action='delete ' if step.isAction else ''
        self.outLine(
            # create (a,R,b)
            '%s%s%s%s%s%s%s%s' % (
                self.kwd(action),
                self.kwd('('),
                step.sourceObjectName,
                self.kwd(','),
                step.association,
                self.kwd(','),
                step.targetObjectName,
                self.kwd(')')),
            indent=indent)
        return self.output

    def doLinkObjectCreationStep(self, step, indent):
        action='create ' if step.isAction else ''
        self.outLine(
            # create x:R(a,b)
            ''.join([
                self.kwd(action),
                step.linkObjectName,
                self.kwd(':'),
                step.associationClass.name,
                self.kwd('('),
                step.sourceObjectName,
                self.kwd(','),
                step.targetObjectName,
                self.kwd(')')]),
            indent=indent)
        return self.output



    def doCheck(self, step, indent):
        _={
            None:'',
            'before': ' (before)',
            'after': ' (after)'
        }[step.position]
        self.outLine(
            '%s%s' % (
                self.kwd('check'),
                self.kwd(_)),
            indent=indent)
        return self.output


