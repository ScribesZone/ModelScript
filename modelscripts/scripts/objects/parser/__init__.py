# coding=utf-8

from __future__ import unicode_literals, print_function, absolute_import, division
from typing import Text, Union, Optional
import os

from modelscripts.megamodels.models import Model, Placeholder
from modelscripts.base.grammars import (
    # ModelSourceAST, \
    # ASTBasedModelSourceFile,
    ASTNodeSourceIssue
)
from modelscripts.base.issues import (
    Levels,
)
from modelscripts.metamodels.objects import (
    ObjectModel,
    METAMODEL
)
from modelscripts.metamodels.objects.linkobjects import LinkObject
from modelscripts.metamodels.objects.links import PlainLink
from modelscripts.metamodels.objects.objects import PlainObject, Slot
from modelscripts.megamodels.sources import (
    ASTBasedModelSourceFile
)
from modelscripts.megamodels.metamodels import Metamodel
from modelscripts.scripts.textblocks.parser import (
    astTextBlockToTextBlock
)
from modelscripts.scripts.stories.parser import (
    StoryFiller
)
from modelscripts.metamodels.stories.evaluations.evaluator import (
    StoryEvaluator
)
__all__=(
    'ObjectModelSource'
)


DEBUG=0


ISSUES={
    'OBJECT_NO_CLASS':'o.res.Object.NoClass',
    'SLOT_NO_OBJECT':'o.syn.Slot.NoObject',
    'SLOT_NO_ATTRIBUTE':'o.res.Slot.NoAttribute',
    'LINK_NO_OBJECT':'o.syn.Link.NoObject'
}
def icode(ilabel):
    return ISSUES[ilabel]

class ObjectModelSource(ASTBasedModelSourceFile):

    def __init__(self, fileName):
        #type: (Text) -> None
        this_dir=os.path.dirname(os.path.realpath(__file__))
        super(ObjectModelSource, self).__init__(
            fileName=fileName,
            grammarFile=os.path.join(this_dir, 'grammar.tx')
        )

        self.storyModel=None
        #type: Optional['Story']
        # The story filled by "fillModel"

        self.storyEvaluation=None
        #type: Optional['StoryEvaluation']
        # The evaluation of the story filled by "fillModel"

    @property
    def objectModel(self):
        #type: () -> ObjectModel
        # usefull for typing checking
        m=self.model #type: ObjectModel
        return m

    @property
    def classModel(self):
        return self.importBox.model('cl')

    @property
    def metamodel(self):
        return METAMODEL

    def fillModel(self):
        # The model "self.model" (e.g. "self.objectModel" is filled
        # "inplace" by the execution below).

        # First fill the story model  with StoryFiller
        # then evaluate the story model leading to the object model

        #--- (1) fill the story model
        filler=StoryFiller(
            model=self.objectModel,         # use this actual object model
            contextMessage='object models',
            allowDefinition=True,
            allowAction=False,
            allowVerb=False,
            astStory=self.ast.model.story)
        self.story=filler.story()

        #--- (2) evaluate the story model to get the object model
        evaluator=StoryEvaluator(
            initialState=self.objectModel,
            permissionSet=None)
        self.storyEvaluation=evaluator.evaluateStory(self.story)

        # At this point the object model contains the final state
        # This is due to the face that the model self.objectModel
        # as been given from the beginning to the StoryFiller

        self.objectModel.storyEvaluation=self.storyEvaluation
        # register this evaluation so that the model know from
        # where it comes from. This is useful for instance if one
        # try to display de story (evaluation) from the model.


METAMODEL.registerSource(ObjectModelSource)
