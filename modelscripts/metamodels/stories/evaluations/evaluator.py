from typing import Union, Optional
from modelscripts.base.grammars import (
    ASTNodeSourceIssue
)
from modelscripts.base.issues import (
    Levels,
)
from modelscripts.scripts.textblocks.parser import (
    astTextBlockToTextBlock
)
from modelscripts.metamodels.stories import (
    Story,
    Step,
    TextStep,
    VerbStep,
)
from modelscripts.metamodels.stories.operations import (
    ObjectCreationStep,
    ObjectDeletionStep,
    SlotStep,
    LinkCreationStep,
    LinkDeletionStep,
    CheckStep,
    LinkObjectCreationStep,
    ReadStep
)
from modelscripts.metamodels.objects import (
    ObjectModel
)
from modelscripts.metamodels.objects.linkobjects import LinkObject
from modelscripts.metamodels.objects.links import PlainLink
from modelscripts.metamodels.objects.objects import PlainObject, Slot
from modelscripts.metamodels.permissions.accesses import (
    AccessSet,
    Access
)
from modelscripts.metamodels.permissions.gpermissions import (
    PermissionSet
)
from modelscripts.metamodels.permissions import (
    CreateAction,
    # ReadAction,
    UpdateAction,
    DeleteAction,
    # ExecuteAction,
)
from modelscripts.metamodels.stories.evaluations import (
    StepEvaluation,
    CompositeStepEvaluation,
    StoryEvaluation
)
from modelscripts.metamodels.stories.evaluations.operations import (
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
}
def icode(ilabel):
    return ISSUES[ilabel]


class StoryEvaluator(object):

    def __init__(self, initialState, permissionSet=None):
        #type: (ObjectModel) -> None
        """
        Create a story evaluation given an initial state (an object model).
        All steps in the story are executed one after the other.
        The object model is modified in place.
        :param initialState:
        :param permissionSet:
        """
        assert initialState is not None
        self.state=initialState
        self.permissionSet=permissionSet
        self.accessSet=AccessSet(permissionSet)
        self.storyEvaluation=None

    def evaluateStory(self, storyStep):
        self.storyEvaluation=(
            self._eval_step(storyStep, parent=None)
        )
        return self.storyEvaluation

    def _eval_step(self, step, parent):
        #type: (Step, Optional[StepEvaluation]) -> StepEvaluation
        if isinstance(step, Story):
            return self._eval_story(step)
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
            raise NotImplementedError(
                'Unexpected step. type=:"%s"' % type(step))

    def _eval_story(self, step):
        seval=StoryEvaluation(step=step)
        for substep in step.steps:
            self._eval_step(substep, seval)
        return seval

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
        # TODO: Implement object deletion
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
        Slot(   # TODO: (?) check old self.object.assign
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
            #TODO: Implement link deletion
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
            raise NotImplementedError(
                'Unexpected type: "%s"' % type(step))
        return step_eval

    def _eval_check(self, step, parent):
        seval=CheckStepEvaluation(
            parent=parent,
            step=step,
            currentState=self.state)
        return seval