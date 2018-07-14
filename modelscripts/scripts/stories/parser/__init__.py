# coding=utf-8

"""
Parser package dealing with the parsing of stories.
This package provides a single class StoryFiller that allow,
given an AST Story provided by the parser, to get a "Story".

This module allows to share this parsing among various parsers.
At the moment stories are used inside ObjectModel parser
and Scenario parser. Both module call the StoryFiller to parse
the subset(s) of the AST corresponding to the story.
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
from modelscripts.metamodels.classes.core import (
    dataTypeFromDataValueName
)
from modelscripts.metamodels.stories import (
    Story,
    TextStep,
    VerbStep,
)
from modelscripts.metamodels.classes.types import EnumerationValue

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

ISSUES={
    # 'DESCRIPTOR_TWICE':'st.syn.Descriptor.Twice',
    # 'ACTOR_NOT_FOUND':'st.syn.ActorInstance.NoActor',
    # 'ACTOR_INSTANCE_NOT_FOUND':'st.syn.Story.NoActorInstance',
    'NO_VERB':'st.syn.Story.NoVerb',
    'NO_ACTION':'st.syn.Story.NoAction',
    'NO_DEFINITION':'st.syn.Story.NoDefinition',
    'NO_CLASS_MODEL':'st.syn.Story.NoClassModel',
    'OBJECT_CLASS_NOT_FOUND':'st.syn.ObjectCreation.NoClass',
    'LINK_ASSOC_NOT_FOUND':'st.syn.LinkOperation.NoAssoc',
    'BAD_VALUE':'st.syn.Value.Bad',
    'NO_ENUM':'st.syn.Value.NoEnum',
    'NO_LITERAL':'st.syn.Value.NoLiteral',


}
def icode(ilabel):
    return ISSUES[ilabel]


class StoryFiller():
    """
    Creator of stories AST model.
    Various parameters allows to tune what story steps are valid or not.
    Virtual "check" statements are added where appropriate.
    """

    def __init__(self,
                 model,
                 contextMessage,
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

        self.contextMessage=contextMessage
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
        elif type_ == 'LinkObjectCreationStep':
            step=self._fill_link_object_creation_step(
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
                    % self.contextMessage))

    def _fill_object_creation_step(self, parent, astStep):
        self._is_check_needed=True
        self._check_definition_action(astStep)
        self._check_class_model(astStep)
        on = astStep.objectDeclaration.name
        cn = astStep.objectDeclaration.type
        class_model=self.model.classModel

        c=class_model.class_(cn)
        if c is None:
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
                class_=c,
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

        def get_simple_value(ast_simple_value):
            simple_value_type = \
                ast_simple_value.__class__.__name__
            if simple_value_type=='EnumerationValue':
                #-- process EnumerationValue
                enum_name=ast_simple_value.enumerationName
                enum_literal_name=ast_simple_value.literalName
                class_model = self.model.classModel
                enum=class_model.enumeration(enum_name)
                if enum is None:
                    ASTNodeSourceIssue(
                        code=icode('NO_ENUM'),
                        astNode=astStep,
                        level=Levels.Fatal,
                        message='Enumeration "%s" does not exist.'
                                % enum_name)
                print("RR"*10, enum)
                enum_literal=enum.literal(enum_literal_name)
                if enum_literal is None:
                    ASTNodeSourceIssue(
                        code=icode('NO_LITERAL'),
                        astNode=astStep,
                        level=Levels.Fatal,
                        message='Enumeration literal '
                                '"%s" does not exist.'
                                % enum_literal_name)

                return EnumerationValue(
                    literal=enum_literal)
            else:
                #-- process DataValue
                repr = ast_simple_value.repr
                # get the datatype, for example the instance
                # of DataType (see metamodel) with name
                # 'StringValue' or 'NullValue'.
                # The result is an instance of DataType.
                datatype=dataTypeFromDataValueName(
                    model=self.model.classModel,
                    datavalue_name=simple_value_type)
                try:
                    # Instanciate an object via the python
                    # implementation class.
                    pyclass=datatype.implementationClass
                    #TODO: optimize creation if required
                    # here we create a distinct
                    # datavalue for each occurence.
                    # This means that there will be
                    # many 5 integer values and many null
                    # values. Care should be taken with
                    # comparisons.
                    datavalue=pyclass(
                        stringRepr=repr,
                        type=datatype)
                    return datavalue
                except ValueError as e:
                    ASTNodeSourceIssue(
                        code=icode('BAD_VALUE'),
                        astNode=astStep,
                        level=Levels.Fatal,
                        message=e.message)

        self._is_check_needed=True
        self._check_definition_action(astStep)
        self._check_class_model(astStep)
        slot_decl = astStep.slotDeclaration
        step = SlotStep(
            parent=parent,
            isAction=astStep.action is not None,
            objectName=slot_decl.object,
            attributeName=slot_decl.attribute,
            value=get_simple_value(slot_decl.simpleValue),
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
        assoc=class_model.association(an)
        if assoc is None:
            ASTNodeSourceIssue(
                code=icode('LINK_ASSOC_NOT_FOUND'),
                astNode=astStep,
                level=Levels.Fatal,
                message=(
                    'Association "%s" does not exist.' % an))
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

    def _fill_link_object_creation_step(self, parent, astStep):
        self._is_check_needed=True
        self._check_definition_action(astStep)
        self._check_class_model(astStep)
        ast_decl=astStep.linkObjectDeclaration
        lo_name = ast_decl.name
        ac_name = ast_decl.associationClass
        class_model=self.model.classModel

        ac=class_model.associationClass(ac_name)
        if ac is None:
            ASTNodeSourceIssue(
                code=icode('OBJECT_ASSCLASS_NOT_FOUND'),
                astNode=astStep,
                level=Levels.Fatal,
                message=(
                    'Association class "%s" does not exist.' % ac_name))
        else:
            step = LinkObjectCreationStep(
                parent=parent,
                isAction=astStep.action is not None,
                linkObjectName=lo_name,
                sourceObjectName=ast_decl.source,
                targetObjectName=ast_decl.target,
                associationClass=ac,
                astNode=astStep
            )
            return step

    def _fill_read_step(self, parent, astStep):
        step=ReadStep(
            parent=parent,
            astNode=astStep
        )
        return step

    def _fill_check_step(self, parent, astStep):
        step=CheckStep(
            parent=parent,
            position=None,
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
                        self.contextMessage)))
        if not self.allowDefinition and not isAction:
            ASTNodeSourceIssue(
                code=icode('NO_DEFINITION'),
                astNode=astStep,
                level=Levels.Fatal,
                message=(
                    'Definitions are forbidden in %s.' % (
                        self.contextMessage)))

    def _add_check_if_needed(self, parent, kind, astNode):
        if self._is_check_needed:
            CheckStep(
                parent=parent,
                position=kind,
                astNode=astNode,
            )
        self._is_check_needed=False
