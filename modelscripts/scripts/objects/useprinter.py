# coding=utf-8
from __future__ import unicode_literals, print_function, absolute_import, \
    division

from typing import Optional

from modelscripts.base.modelprinters import (
    ModelPrinter,
    ModelSourcePrinter,
    ModelPrinterConfig,)
from modelscripts.scripts.textblocks.printer import (
    TextBlockPrinter)
from modelscripts.metamodels.objects import (
    ObjectModel,
    METAMODEL
)
from modelscripts.metamodels.objects.linkobjects import LinkObject
from modelscripts.metamodels.objects.objects import Object, Slot
from modelscripts.metamodels.objects.links import Link
from modelscripts.megamodels.models import (
    Placeholder
)
# from modelscripts.scripts.stories.printer import (
#     StoryPrinter
# )
from modelscripts.scripts.stories.printer.evaluation import (
    #StoryEvaluationPrinter
    StoryBestPrinter
)

class ObjectModelPrinter(ModelPrinter):

    def __init__(self,
                 theModel,
                 config=None):
        #type: (ObjectModel, Optional[ModelPrinterConfig]) -> None
        super(ObjectModelPrinter, self).__init__(
            theModel=theModel,
            config=config
        )



    def doModelContent(self):
        super(ObjectModelPrinter, self).doModelContent()

        if self.theModel.storyEvaluation is not None:
            text=StoryBestPrinter(
                story=self.theModel.storyEvaluation.step,
                storyEvaluation=self.theModel.storyEvaluation,
                #TODO:- add selection to configuraiton
                # useStory=XXX
            ).do()
            self.outLine(text)
            return self.output
        else:
            # the model does not come from a story
            # It can still be printed, using the code below
            #TODO:- reimplement the raw object model printer
            print(('^^'*40+'\n')*20)
            print( """*** NO STORY TO PRINT. See TODO""" )

    #-------------------------------------------------------------------
    #                The code below is not used anymore.
    #  Some parts could be interesting (?) to print the object model
    #  as is, and not with a story, e.g. all objects, all



    def doStoryObjectModel(self, objectModel):
        for d in objectModel.definitions:
            if isinstance(d, AnnotatedTextBlock):
                self.doAnnotatedTextBlocks(d)
            else:
                self.doCoreDefinition(d, indent=0)
        return self.output

    def doAbstractObjectModel(self, objectModel):
        for o in objectModel.objects:
            self.doFullObject(o)
        for l in objectModel.links:
            self.doLinkDefinition(l)
        #TODO:3 add doObjectLinks


    def doCoreDefinition(self, d, indent=0):
        if isinstance(d, Object):
            self.doObjectDefinition(d, indent=indent)
        elif isinstance(d, Slot):
            self.doSlotDefinition(d, indent=indent)
        elif isinstance(d, Link):
            self.doLinkDefinition(d, indent=indent)
            #TODO:3 check what to do with LinkObject
        else:
            raise NotImplementedError(
                'Unexpected type: %s' % type(d))


    def doObjectDefinition(self, o, indent=0):
        class_name=(
            str(o.class_)
                if isinstance(o.class_, Placeholder)
            else o.class_.name)
        self.outLine('%s %s %s' % (
                 o.name,
                 self.kwd(':'),
                 class_name),
            indent=indent)
        return self.output

    def doFullObject(self, o, indent=0):
        self.doObjectDefinition(o, indent)
        for s in o.slots:
            self.doNestedSlot(s, indent=indent+1)
        return self.output

    def doNestedSlot(self, slot, indent=0):
        attribute_name=(
            str(slot.attribute)
            if isinstance(slot.attribute, Placeholder)
            else slot.attribute.name)
        self.outLine('%s %s %s' % (
                    attribute_name,
                    self.kwd('='),
                    str(slot.value)),
                indent=indent)
        return self.output

    def doSlotDefinition(self, slot, indent=0):
        attribute_name=(
            str(slot.attribute)
            if isinstance(slot.attribute, Placeholder)
            else slot.attribute.name)
        self.outLine('%s%s%s %s %s' % (
                slot.object.name,
                self.kwd('.'),
                attribute_name,
                self.kwd('='),
                str(slot.value)),
            indent=indent)
        return self.output

    def doLinkDefinition(self, l, indent=0):
        association_name=(
            str(l.association)
                if isinstance(l.association, Placeholder)
            else l.association.name)
        self.outLine('%s%s%s %s%s %s%s' % (
                    self.kwd('('),
                    l.sourceObject.name,
                    self.kwd(','),
                    association_name,
                    self.kwd(','),
                    l.targetObject.name,
                    self.kwd(')')),
            indent=indent)
        return self.output

        # TODO:2 add object links

    def doAnnotatedTextBlocks(self, atb):
        block_text=TextBlockPrinter(
            textBlock=atb.textBlock,
            config=self.config).do()
        self.outLine(block_text, indent=0)

        for d in atb.definitions:
            self.doCoreDefinition(d, indent=1)
        return self.output


METAMODEL.registerModelPrinter(ObjectModelPrinter)
METAMODEL.registerSourcePrinter(ModelSourcePrinter)
