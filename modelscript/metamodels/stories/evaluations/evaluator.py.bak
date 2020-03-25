# coding=utf-8
"""
Engine performing the evaluation of stories.
The engine basically creates a StoryEvaluation from
an initial state (an ObjectModel). This state is updated
inplace.
"""

from __future__  import print_function
from typing import Union, Optional, Dict, Text
from modelscript.base.grammars import (
    ASTNodeSourceIssue
)
from modelscript.base.issues import (
    Levels,
)
from modelscript.scripts.textblocks.parser import (
    astTextBlockToTextBlock
)
from modelscript.metamodels.stories import (
    # CompositeStory,
    Story,
    IncludeStep,
    Step,
    TextStep,
    VerbStep,
    AbstractStoryId,
    AbstractStoryCollection
)
from modelscript.metamodels.stories.operations import (
    ObjectCreationStep,
    ObjectDeletionStep,
    SlotStep,
    LinkCreationStep,
    LinkDeletionStep,
    CheckStep,
    LinkObjectCreationStep,
    ReadStep
)
from modelscript.metamodels.objects import (
    ObjectModel
)
from modelscript.metamodels.objects.linkobjects import LinkObject
from modelscript.metamodels.objects.links import PlainLink
from modelscript.metamodels.objects.objects import PlainObject, Slot
from modelscript.metamodels.permissions.accesses import (
    AccessSet,
    Access
)
from modelscript.metamodels.permissions.gpermissions import (
    PermissionSet
)
from modelscript.metamodels.permissions import (
    CreateAction,
    # ReadAction,
    UpdateAction,
    DeleteAction,
    # ExecuteAction,
)
from modelscript.metamodels.stories.evaluations import (
    StepEvaluation,
    CompositeStepEvaluation,
    StoryEvaluation,
    StoryIncludeEvaluation
    # CompositeStoryEvaluation
)
from modelscript.metamodels.stories.evaluations.operations import (
    OperationStepEvaluation,
    CheckStepEvaluation
)



ISSUES={
    'OBJECT_TWICE':'st.eval.ObjectCreation.Twice',
    'OBDEL_NO_OBJECT':'st.eval.ObjectDeletion.NoObject',
    'OBDEL_NO_IMPL':'st.eval.ObjectDeletion.NoImpl',
    'SLOT_NO_OBJECT':'st.eval.Slot.NoObject',
    'SLOT_NO_ATT':'st.eval.Slot.NoAtt',
    'SLOT_DEF_TWICE':'st.eval.Slot.Twice',
    'SLOT_NO_INIT':'st.eval.Slot.NoInit',
    'LINK_NO_SOURCE':'st.eval.Link.NoSource',
    'LINK_NO_TARGET':'st.eval.Link.NoTarget',
    'LINKDEL_NOT_IMPL':'st.eval.LinkDeletion.NoImpl',
    'NO_STORY':'st.eval.Include.NoStory',
}
def icode(ilabel):
    return ISSUES[ilabel]

# class StoryCollection(object):
#
#     def __init__(self,
#                  objectsStory=None,
#                  contextMap={},
#                  storyMap={}):
#
#         self.objectStory=objectsStory
#         #type: Optional[Story]
#
#         self.contextMap=contextMap
#         #type: Dict[Text, Story]
#
#         self.storyMap=storyMap
#         #type: Dict[Text, Story]
#
#     def setStory(self, kind, name, story):
#         if kind=='object model':
#             self.objectStory=story
#         elif kind in ['context']:
#             self.contextMap[name]=story
#         elif kind=='story':
#             self.storyMap[name]=story
#         else:
#             raise NotImplementedError('unknown story kind: "%s".' % kind)
#
#     def getStory(self, kind, name):
#         #type: (Text, Optional[Text]) -> Optional[Story]
#         """
#         Return the story associated with the kind and name.
#         Return None if the story does not exists.
#         In that case use getGetIssueMessage.
#         Name is not taken into account for "object model" kind.
#         Providing None is OK.
#         """
#         if kind=='object model':
#             return self.objectStory
#         elif kind=='context':
#             if name in self.contextMap:
#                 return self.contextMap[name]
#             else:
#                 return None
#         elif kind=='story':
#             if name in self.storyMap:
#                 return self.storyMap[name]
#             else:
#                 return None
#         else:
#             raise NotImplementedError('unknown story kind: "%s".' % kind)
#
#     def getGetIssueMessage(self, kind, name):
#         #type: (Text, Optional[Text]) -> Text
#         """
#         Return an suitable issue message when using "getStory"
#         and when there is no such story.
#         To be used when getStory(kind, name) returned None.
#         """
#         if kind=='object model':
#             return 'No object model provided. Include is invalid.'
#         elif kind in ['context', 'story']:
#             return ('Failed to include %s "%s".' % (kind, name))
#         else:
#             raise NotImplementedError('unknown story kind: "%s".' % kind)

    # def getSetIssueMessage(self, kind, name):
    #     #type: (Text, Optional[Text]) -> Text
    #     """
    #     Return an suitable issue message when using "setStory".
    #     and when a story with that name is already defined.
    #     To be used when getStory(kind, name) does not returned None.
    #     """
    #     if kind=='object model':
    #         raise RuntimeError('Object model must not be set twice.')
    #     elif kind in ['context', 'story']:
    #         return ('%s %s is already defined".' % (kind, name))
    #     else:
    #         raise NotImplementedError('unknown story kind: "%s".' % kind)


class StoryEvaluator(object):
    """
    Engine performing the evaluation of a story.

    After creating the evaluator with a given state,
    "evaluateStory()" must be used to perform the
    evaluation itself.

    The storyCollection given is used to interpret the
    'include' statement.

    The initialState parameter is used to initialize self.state.
    This variable is then modified in place to the step executed
    so that a typical usage is to give the state to be filled by
    the story evaluator.
    """

    def __init__(self,
                 initialState,
                 storyCollection=None,
                 permissionSet=None):
        #type: (ObjectModel, AbstractStoryCollection, Optional[PermissionSet]) -> None
        """
        Create the evaluator object. Use evaluateStory() to launch
        the evaluation itself.
        :param initialState:
            The object model in which the story is evaluated.
            This object model will be updated during the evaluation.
        :param storyCollection:
            The environment used for include statements.
        :param permissionSet:
            A permissionSet to check the accesses against. If set
            some access Authorization/Denial can be created.
        """
        self.storyCollection=storyCollection
        #type: AbstractStoryCollection

        assert initialState is not None
        self.state=initialState
        #type: ObjectModel
        # The state in which each step is evaluated.
        # This state evolves step after step, so this will be
        # the final state at the end of the evaluation.

        self.permissionSet=permissionSet
        #type: Optional[PermissionSet]

        self.accessSet=AccessSet(permissionSet)
        #type: AccessSet

        self.storyEvaluation=None
        #type: Optional[StoryEvaluation]
        # Filled by evaluateStory

    def evaluateStory(self, story):
        #type: (Story) -> StepEvaluation
        """
        Evaluate a whole story and return a StoryEvaluation.
        Create a story evaluation given an initial state
        (an object model).
        All steps in the story are executed one after the other.
        The state self.state is modified in place, step after step.
        """
        self.storyEvaluation=(
            self._eval_step(story, parent=None))
        return self.storyEvaluation

    def _eval_step(self, step, parent):
        #type: (Step, Optional[StepEvaluation]) -> StepEvaluation
        if isinstance(step, Story):
            return self._eval_story(step, parent)
        elif isinstance(step, IncludeStep):
            return self._eval_include(step, parent)
        elif isinstance(step, TextStep):
            return self._eval_text(step, parent)
        elif isinstance(step, VerbStep):
            return self._eval_verb(step, parent)
        elif isinstance(step, ObjectCreationStep):
            return self._eval_object_creation(step, parent)
        elif isinstance(step, ObjectDeletionStep):
            return self._eval_object_deletion(step, parent)
        elif isinstance(step, SlotStep):
            return self._eval_slot(step, parent)
        elif isinstance(step, LinkCreationStep)\
                or isinstance(step, LinkDeletionStep) :
            return self._eval_link_operation(step, parent)
        elif isinstance(step, LinkObjectCreationStep):
            return self._eval_link_object_creation(step, parent)
        elif isinstance(step, CheckStep):
            return self._eval_check(step, parent)
        else:
            raise NotImplementedError( #raise:OK
                'INTERNAL ERROR: Unexpected step. type=:"%s"' % type(step))

    def _eval_story(self, step, parent):
        #type: (Story, Optional[StoryIncludeEvaluation]) -> StoryEvaluation
        seval=StoryEvaluation(step=step, parent=parent)
        for substep in step.steps:
            self._eval_step(substep, seval)
        return seval

    def _eval_include(self, step, parent):
        #---- (1) Create the (empty) Include Evaluation
        include_evaluation=StoryIncludeEvaluation(
            parent=parent,
            step=step)

        #---- (2) Get the story to be included
        sc=self.storyCollection
        story_to_included=\
            sc.story(step.storyId)
        if story_to_included is None:
            ASTNodeSourceIssue(
                code=icode('NO_STORY'),
                astNode=step.astNode,
                level=Levels.Fatal,
                message='Include failed.')
            # The message could be improved but only with
            # various modifications. This would imply maintaining
            # a map between StoryId (which is in a metamodel) and
            # its external representation. The message above is
            # good enough...
            #
            # This is a fatal issue. This means that
            # the step commented below are not relevant:
            #    step_eval.issues.append(i)
            #    self.accesses=[]

        #---- (3) Evaluate the selected story

        print('OO'*10, type(story_to_included))
        story_evaluation_included=\
            self._eval_story(
                step=story_to_included,
                parent=include_evaluation)
        include_evaluation \
            .storyEvaluationIncluded=story_evaluation_included
        return include_evaluation


    def _eval_text(self, step, parent):
        return self._eval_composite(step, parent)

    def _eval_verb(self, step, parent):
        return self._eval_composite(step, parent)

    def _eval_composite(self, step, parent):
        seval=CompositeStepEvaluation(
            parent=parent,
            step=step)
        for substep in step.steps:
            self._eval_step(substep, seval)
        return seval

    def _eval_object_creation(self, step, parent):
        name=step.objectName
        step_eval=OperationStepEvaluation(
            parent=parent,
            step=step)
        existing_object=self.state.object(name)
        if existing_object is not None:
            i=ASTNodeSourceIssue(
                code=icode('OBJECT_TWICE'),
                astNode=step.astNode,
                level=Levels.Error,
                message=(
                    'Object "%s" already exist.'
                    ' Previous definition replaced.' % name))
            step_eval.issues.append(i)
        PlainObject(
            model=self.state,
            name=step.objectName,
            class_=step.class_,
            package=None,
            step=step)
        step_eval.accesses=[
            Access(
                step_eval,
                CreateAction,
                step.class_,
                self.accessSet)]

        return step_eval

    def _eval_link_object_creation(self, step, parent):
        name=step.linkObjectName
        step_eval=OperationStepEvaluation(
            parent=parent,
            step=step)
        source= self.state.object(step.sourceObjectName)
        target= self.state.object(step.targetObjectName)
        if source is None:
            i = ASTNodeSourceIssue(
                code=icode('LINK_NO_SOURCE'),
                astNode=step.astNode,
                level=Levels.Error,
                message=(
                    'Source object "%s" does not exist.'
                    ' Link object ignored.' % step.sourceObjectName))
            step_eval.issues.append(i)
            self.accesses=[]
            return step_eval
        if target is None:
            i = ASTNodeSourceIssue(
                code=icode('LINK_NO_TARGET'),
                astNode=step.astNode,
                level=Levels.Error,
                message=(
                    'Target object "%s" does not exist.'
                    ' Link object ignored.' % step.targetObjectName))
            step_eval.issues.append(i)
            self.accesses=[]
            return step_eval

        existing_object=self.state.object(name)
        if existing_object is not None:
            i=ASTNodeSourceIssue(
                code=icode('OBJECT_TWICE'),
                astNode=step.astNode,
                level=Levels.Error,
                message=(
                    'Object "%s" already exist.'
                    ' Previous definition replaced.' % name))
            step_eval.issues.append(i)
        LinkObject(
            model=self.state,
            name=name,
            associationClass=step.associationClass,
            sourceObject=source,
            targetObject=target,
            package=None,
            step=step)
        step_eval.accesses=[
            Access(
                step_eval,
                CreateAction,
                step.associationClass,
                self.accessSet)]

    def _eval_object_deletion(self, step, parent):
        step_eval=OperationStepEvaluation(
            parent=parent,
            step=step)
        obj=self.state.object(step.objectName)
        if obj is None:
            i = ASTNodeSourceIssue(
                code=icode('OBDEL_NO_OBJECT'),
                astNode=step.astNode,
                level=Levels.Error,
                message=(
                    'Object "%s" does not exist.'
                    ' Deletion ignored.' % step.objectName))
            step_eval.issues.append(i)
            self.accesses=[]
            return step_eval
        # TODO:3 Implement object deletion
        i = ASTNodeSourceIssue(
            code=icode('OBDEL_NOT_IMPL'),
            astNode=step.astNode,
            level=Levels.Error,
            message=(
                'Object deletion is not implemented yet.'
                ' Deletion of "%s" ignored.' % step.objectName))
        step_eval.issues.append(i)
        step_eval.accesses=[
            Access(
                step_eval,
                DeleteAction,
                obj.class_,
                self.accessSet)]
        return step_eval

    def _eval_slot(self, step, parent):
        step_eval=OperationStepEvaluation(
            parent=parent,
            step=step)
        obj=self.state.object(step.objectName)
        if obj is None:
            i = ASTNodeSourceIssue(
                code=icode('SLOT_NO_OBJECT'),
                astNode=step.astNode,
                level=Levels.Error,
                message=(
                    'Object "%s" does not exist.'
                    ' Assignment ignored.' % step.objectName))
            step_eval.issues.append(i)
            self.accesses=[]
            return step_eval
        att=obj.class_.attribute(step.attributeName)
        if att is None:
            i = ASTNodeSourceIssue(
                code=icode('SLOT_NO_ATT'),
                astNode=step.astNode,
                level=Levels.Error,
                message=(
                    'Attribute "%s" does not exist.'
                    ' Assignment ignored.' % step.attributeName))
            step_eval.issues.append(i)
            self.accesses=[]
            return step_eval
        slot=obj.slot(step.attributeName)
        if slot is not None:
            # The slot has already been initialized
            if not step.isUpdate:
                i = ASTNodeSourceIssue(
                    code=icode('SLOT_DEF_TWICE'),
                    astNode=step.astNode,
                    level=Levels.Error,
                    message=(
                        'Attribute "%s" already initialized.'
                        ' Assignment ignored.' % step.attributeName))
                step_eval.issues.append(i)
                self.accesses = []
                return step_eval
        else:
            # The slot is empty
            if step.isUpdate:
                if not step.isUpdate:
                    i = ASTNodeSourceIssue(
                        code=icode('SLOT_NO_INIT'),
                        astNode=step.astNode,
                        level=Levels.Error,
                        message=(
                            'Attribute "%s" not initialized.'
                            ' Assignment ignored.' % step.attributeName))
                    step_eval.issues.append(i)
                    self.accesses = []
                    return step_eval
        Slot(   #TODO:- check old self.object.assign
            object=obj,
            attribute=att,
            simpleValue=step.simpleValue,
            step=step)
        step_eval.accesses=[
            Access(
                step_eval,
                UpdateAction,
                att,
                self.accessSet)]
        return step_eval

    def _eval_link_operation(self, step, parent):
        step_eval=OperationStepEvaluation(
            parent=parent,
            step=step)
        assoc=step.association
        source= self.state.object(step.sourceObjectName)
        target= self.state.object(step.targetObjectName)
        if source is None:
            i = ASTNodeSourceIssue(
                code=icode('LINK_NO_SOURCE'),
                astNode=step.astNode,
                level=Levels.Error,
                message=(
                    'Source object "%s" does not exist.'
                    ' Link ignored.' % step.sourceObjectName))
            step_eval.issues.append(i)
            self.accesses=[]
            return step_eval
        if target is None:
            i = ASTNodeSourceIssue(
                code=icode('LINK_NO_TARGET'),
                astNode=step.astNode,
                level=Levels.Error,
                message=(
                    'Target object "%s" does not exist.'
                    ' Link ignored.' % step.targetObjectName))
            step_eval.issues.append(i)
            self.accesses=[]
            return step_eval
        if isinstance(step, LinkCreationStep):
            PlainLink(
                model=self.state,
                association=assoc,
                sourceObject=source,
                targetObject=target,
                step=step)
            step_eval.accesses = [
                Access(
                    step_eval,
                    CreateAction,
                    assoc,
                    self.accessSet)]
        elif isinstance(step, LinkDeletionStep):
            #TODO:3 Implement link deletion
            i = ASTNodeSourceIssue(
                code=icode('LINKDEL_NOT_IMPL'),
                astNode=step.astNode,
                level=Levels.Error,
                message=(
                    'Link deletion is not implemented yet.'
                    ' Deletion ignored.'))
            step_eval.issues.append(i)
            step_eval.accesses = [
                Access(
                    step_eval,
                    DeleteAction,
                    assoc,
                    self.accessSet)]
            pass
        else:
            raise NotImplementedError(  #raise:OK
                'INTERNAL ERROR: Unexpected type: "%s"' % type(step))
        return step_eval

    def _eval_check(self, step, parent):
        seval=CheckStepEvaluation(
            parent=parent,
            step=step,
            currentState=self.state)
        return seval