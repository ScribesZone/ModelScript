# coding=utf-8

from typing import Optional

from modelscript.base.exceptions import (
    UnexpectedCase)
from modelscript.base.printers import (
    AbstractPrinter,
    AbstractPrinterConfig,
    Styles)
from modelscript.metamodels.stories import (
    Story,
    TextStep,
    VerbStep,)
from modelscript.metamodels.stories.operations import (
    ObjectCreationStep,
    ObjectDeletionStep,
    SlotStep,
    LinkCreationStep,
    LinkDeletionStep,
    LinkObjectCreationStep,
    CheckStep,
    ReadStep)


from modelscript.scripts.textblocks.printer import (
    TextBlockPrinter
)

__all__=(
    'UseStoryPrinter'
)

class TextConfig(AbstractPrinterConfig):
    def __init__(self):
        super(TextConfig, self).__init__(
            styled=False,
            displayLineNos=False
        )
class UseStoryPrinter(AbstractPrinter):


    def __init__(self,
                 story,
                 indent=0):
        #type: (Story, int) -> None
        super(UseStoryPrinter, self).__init__(
            config=TextConfig()
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
            raise UnexpectedCase( #raise:OK
                'Unexpected step. type=:"%s"' % type(step))

    def doVerbStep(self, step, indent, recursive=True):
        self.outLine(
            '-- %s %s %s' % (
                step.subjectName,
                self.kwd('do'),
                step.verbName
            ),
            indent=indent
        )
        if recursive:
            self._doSubsteps(step, indent+1, recursive=recursive)
        return self.output

    def doTextStep(self, step, indent, recursive=True):
        # tbp=TextBlockPrinter(step.textBlock, indent=indent)
        # text=tbp.do()
        # self.outLine(text)
        self.outLine('-- text')
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
            '! %s := new %s(\'%s\')' % (
                step.objectName,
                step.class_.name,
                step.objectName),
            indent=indent)
        return self.output

    def doObjectDeletionStep(self, step, indent):
        action='delete ' if step.isAction else ''
        self.outLine(
            '! destroy %s' % step.objectName,
            indent=indent
        )
        return self.output

    def doSlotStep(self, step, indent):
        self.outLine(
            '! %s.%s := %s' % (
                step.objectName,
                step.attributeName,
                str(step.simpleValue)),
            indent=indent)
        return self.output

    def doLinkCreationStep(self, step, indent):
        action='create ' if step.isAction else ''
        self.outLine(
            # create (a,R,b)
            '! insert(%s,%s) into %s' % (
                step.sourceObjectName,
                step.targetObjectName,
                step.association.name),
            indent=indent)
        return self.output

    def doLinkDeletionStep(self, step, indent):
        action='delete ' if step.isAction else ''
        self.outLine(
            # create (a,R,b)
            '! delete (%s,%s) from %s' % (
                step.sourceObjectName,
                step.targetObjectName,
                step.association.name),
            indent=indent)
        return self.output

    def doLinkObjectCreationStep(self, step, indent):
        self.outLine(
            '! %s := new %s(\'%s\') between (%s,%s)' % (
                step.linkObjectName,
                step.associationClass.name,
                step.linkObjectName,
                step.sourceObjectName,
                step.targetObjectName,
            ),
            indent=indent
        )
        return self.output



    def doCheck(self, step, indent):
        self.outLine(
            'check -a -v -d',
            indent=indent)
        return self.output


