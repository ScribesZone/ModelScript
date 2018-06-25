# coding=utf-8

"""
Parser package dealing with the paring of stories.
This package provides a single class StoryFiller that allow to
get a "Story" giving a AST Story. This allow to share this
parsing among various parser. At the moment stories are used
inside ObjectModel parser and Scenario parser.
"""
from typing import Union
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
    ReadStep
)

ISSUES={
    # 'DESCRIPTOR_TWICE':'st.syn.Descriptor.Twice',
    # 'ACTOR_NOT_FOUND':'st.syn.ActorInstance.NoActor',
    # 'ACTOR_INSTANCE_NOT_FOUND':'st.syn.Story.NoActorInstance',
    'NO_VERB':'st.syn.Story.NoVerb',
    'NO_ACTION':'st.syn.Story.NoAction',
    'NO_DEFINITION':'st.syn.Story.NoDefinition',
    'NO_CLASS_MODEL':'st.syn.Story.NoClassModel',
    'OBJECT_CLASS_NOT_FOUND':'st.syn.ObjectCreation.NoClass',
    'LINK_ASSOC_NOT_FOUND':'st.syn.LinkOperation.NoAssoc'
}
def icode(ilabel):
    return ISSUES[ilabel]


class StoryFiller():

    def __init__(self,
                 model,
                 contextName,
                 allowDefinition,
                 allowAction,
                 allowVerb,
                 astStory):
        #type: ('Model', Union['definition','action'], 'ASTStory') -> None
        """
        Create a StoryFiller with various parameters controlling what
        is accepted or not. The AST story to be parsed must be given.
        use story() method to launch the parsing and get the result.
        """
        self.astStory=astStory
        self.model=model

        self.contextName=contextName
        # some string like "object model" or "context"
        # string used for error message

        self.allowDefinition=allowDefinition
        self.allowAction=allowAction
        self.allowVerb=allowVerb

        self._is_check_needed=False
        # This is used to control the creation of implicit check
        # statement and create these statements only if at least
        # an operation was issued before the potential check point.
        # Variable to keep along the creation of statements the
        # need to create an implict check statement. This is the
        # case when a new operation occur. Otherwise text block
        # don't count, and check statements set it to no.
        # See _add_check_if_needed.

    def story(self):
        #type: () -> Story
        self.story=Story(
            model=self.model,
            astNode=self.astStory)
        # textx => could be None even if it should not. => test
        if self.astStory is not None:
            for ast_step in self.astStory.steps:
                self._fill_step(
                    parent=self.story,
                    astStep=ast_step
                )
        self._add_check_if_needed(self.story, 'after', self.astStory)
        return self.story



    def _fill_step(self, parent, astStep):
        type_ = astStep.__class__.__name__
        if type_=='TextStep':
            step=self._fill_text_step(
                parent, astStep)
        elif type_=='VerbStep':
            step=self._fill_verb_step(
                parent, astStep)
        elif type_=='ObjectCreationStep':
            step=self._fill_object_creation_step(
                parent, astStep)
        elif type_=='ObjectDeletionStep':
            step=self._fill_object_deletion_step(
                parent, astStep)
        elif type_=='SlotStep':
            step=self._fill_slot_step(
                parent, astStep)
        elif type_=='LinkOperationStep':
            step=self._fill_link_operation_step(
                parent, astStep)
        elif type_=='ReadStep':
            step=self._fill_read_step(
                parent, astStep)
        elif type_=='CheckStep':
            step=self._fill_check_step(
                parent, astStep)
        else:
            raise NotImplementedError(
                'AST type not expected: %s' % type_)
        return step

    def _fill_text_step(self, parent, astStep):
        text_block = astTextBlockToTextBlock(
            container=parent,
            astTextBlock=astStep.textBlock)
        step = TextStep(
            parent=parent,
            textBlock=text_block,
            astNode=astStep)
        for sub_ast_step in astStep.steps:
            self._fill_step(
                parent=step,
                astStep=sub_ast_step
            )
        return step

    def _fill_verb_step(self, parent, astStep):
        if self.allowVerb:
            self._add_check_if_needed(
                parent,
                'before',
                astStep)
            step=VerbStep(
                parent=parent,
                subjectName=astStep.subjectName,
                verbName=astStep.verbName
            )
            for sub_ast_step in astStep.steps:
                self._fill_step(
                    parent=step,
                    astStep=sub_ast_step
                )
            self._add_check_if_needed(
                parent,
                'after',
                astStep)
            return step
        else:
            ASTNodeSourceIssue(
                code=icode('NO_VERB'),
                astNode=astStep,
                level=Levels.Fatal,
                message=(
                    'Statement not allowed in %s'
                    % self.contextName))

    def _fill_object_creation_step(self, parent, astStep):
        self._is_check_needed=True
        self._check_definition_action(astStep)
        self._check_class_model(astStep)
        on = astStep.objectDeclaration.name
        cn = astStep.objectDeclaration.type
        class_model=self.model.classModel

        if cn not in class_model.classNamed:
            ASTNodeSourceIssue(
                code=icode('OBJECT_CLASS_NOT_FOUND'),
                astNode=astStep,
                level=Levels.Fatal,
                message=(
                    'Class "%s" does not exist.' % cn))
        else:
            step = ObjectCreationStep(
                parent=parent,
                isAction=astStep.action is not None,
                objectName=on,
                class_=class_model.classNamed[cn],
                astNode=astStep
            )
            return step

    def _fill_object_deletion_step(self, parent, astStep):
        self._is_check_needed=True
        self._check_definition_action(astStep)
        self._check_class_model(astStep)
        on = astStep.objectDeclaration.name

        step = ObjectDeletionStep(
                parent=parent,
                objectName=on,
                astNode=astStep
        )
        return step

    def _fill_slot_step(self, parent, astStep):
        self._is_check_needed=True
        self._check_definition_action(astStep)
        self._check_class_model(astStep)
        slot_decl = astStep.slotDeclaration
        step = SlotStep(
            parent=parent,
            isAction=astStep.action is not None,
            objectName=slot_decl.object,
            attributeName=slot_decl.attribute,
            value=slot_decl.value,
            isUpdate=(astStep.action in ['update', 'modifie']),
            astNode=astStep
        )
        return step

    def _fill_link_operation_step(self, parent, astStep):
        self._is_check_needed=True
        self._check_definition_action(astStep)
        self._check_class_model(astStep)
        link_decl = astStep.linkDeclaration
        an = link_decl.association
        action = astStep.action
        class_model=self.model.classModel
        if an not in class_model.associationNamed:
            ASTNodeSourceIssue(
                code=icode('LINK_ASSOC_NOT_FOUND'),
                astNode=astStep,
                level=Levels.Fatal,
                message=(
                    'Association "%s" does not exist.' % an))
        assoc = class_model.associationNamed[an]
        if action == 'create' or action is None:
            step = LinkCreationStep(
                parent=parent,
                isAction=(action == 'create'),
                sourceObjectName=link_decl.source,
                targetObjectName=link_decl.target,
                association=assoc,
                astNode=astStep
            )
            return step
        elif action == 'delete':
            step = LinkDeletionStep(
                parent=parent,
                sourceObjectName=link_decl.source,
                targetObjectName=link_decl.target,
                association=assoc,
                astNode=astStep
            )
            return step
        else:
            raise NotImplementedError(
                'Action not expected: %s' % action)

    def _fill_read_step(self, parent, astStep):
        step=ReadStep(
            parent=parent,
            astNode=astStep
        )
        return step

    def _fill_check_step(self, parent, astStep):
        step=CheckStep(
            parent=parent,
            implicit=None,
            astNode=astStep
        )
        self._is_check_needed=False
        return step

    def _check_class_model(self, astStep):
        if self.model.classModel is None:
            ASTNodeSourceIssue(
                code=icode('NO_CLASS_MODEL'),
                astNode=astStep,
                level=Levels.Fatal,
                message=('No class model is imported.' ))

    def _check_definition_action(self, astStep):
        """
        Check that the presence of the ast node "action"
        conforms to  allowAction and allowDefinition.
        This assume that all ast node provided has an
        action part.
        :param astStep:
        :return:
        """
        isAction = astStep.action is not None
        if not self.allowAction and isAction:
            ASTNodeSourceIssue(
                code=icode('NO_ACTION'),
                astNode=astStep,
                level=Levels.Fatal,
                message=(
                    '"%s" actions are forbidden in %s.' % (
                        astStep.action,
                        self.contextName)))
        if not self.allowDefinition and not isAction:
            ASTNodeSourceIssue(
                code=icode('NO_DEFINITION'),
                astNode=astStep,
                level=Levels.Fatal,
                message=(
                    'Definitions are forbidden in %s.' % (
                        self.contextName)))



    def _add_check_if_needed(self, parent, kind, astNode):
        if self._is_check_needed:
            CheckStep(
                parent=parent,
                implicit=kind,
                astNode=astNode
            )
        self._is_check_needed=False
