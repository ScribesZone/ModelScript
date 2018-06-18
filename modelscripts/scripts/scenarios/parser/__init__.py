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
from modelscripts.megamodels.elements import (
    Descriptor
)
from modelscripts.metamodels.scenarios import (
    ScenarioModel,
    ActorInstance,
    Story,
    Step,
    UsecaseInstanceStep,
    AnnotatedTextBlockStep,
    METAMODEL
)
from modelscripts.metamodels.scenarios.operations import (
    ObjectCreation,
    ObjectDeletion,
    AttributeAssignment,
    LinkCreation,
    LinkDeletion,
    # TODO: LinkObject
    Check
)
from modelscripts.metamodels.classes import (
    ClassModel
)
from modelscripts.metamodels.usecases import (
    UsecaseModel
)
from modelscripts.metamodels.glossaries import (
    GlossaryModel
)
from modelscripts.metamodels.permissions import (
    PermissionModel
)
from modelscripts.megamodels.sources import (
    ASTBasedModelSourceFile
)
from modelscripts.megamodels.metamodels import Metamodel
from modelscripts.scripts.textblocks.parser import (
    astTextBlockToTextBlock
)

__all__=(
    'ObjectModelSource'
)


DEBUG=0


ISSUES={
    'DESCRIPTOR_TWICE':'sc.syn.Descriptor.Twice',
    'ACTOR_NOT_FOUND':'sc.syn.ActorInstance.NoActor',
    'ACTOR_INSTANCE_NOT_FOUND':'sc.syn.Story.NoActorInstance',
    'USECASE_NOT_FOUND':'sc.syn.Story.NoUsecase',
    'OBJECT_CLASS_NOT_FOUND':'sc.syn.ObjectCreation.NoClass',
    'LINK_ASSOC_NOT_FOUND':'sc.syn.LinkOperation.NoAssoc'
}
def icode(ilabel):
    return ISSUES[ilabel]

class ScenarioEvaluationModelSource(ASTBasedModelSourceFile):

    def __init__(self, fileName):
        #type: (Text) -> None
        this_dir=os.path.dirname(os.path.realpath(__file__))
        super(ScenarioEvaluationModelSource, self).__init__(
            fileName=fileName,
            grammarFile=os.path.join(this_dir, 'grammar.tx')
        )

    @property
    def scenarioModel(self):
        #type: () -> ScenarioModel
        # usefull for typing checking
        m=self.model #type: ScenarioModel
        return m

    @property
    def classModel(self):
        #type: () -> Optional[ClassModel]
        # TODO: the optional stuff should come from metamdel
        return self.importBox.model('cl', optional='True')

    @property
    def usecaseModel(self):
        #type: () -> Optional[UsecaseModel]
        # TODO: the optional stuff should come from metamdel
        return self.importBox.model('us', optional='True')

    @property
    def glossaryModel(self):
        # TODO: the optional stuff should come from metamdel
        #type: () -> Optional[GlossaryModel]
        return self.importBox.model('gl', optional='True')

    @property
    def permissionModel(self):
        #type: () -> Optional[PermissionModel]
        # TODO: the optional stuff should come from metamdel
        return self.importBox.model('pe', optional='True')

    @property
    def metamodel(self):
        return METAMODEL

    def fillModel(self):

        def define_descriptor(ast_descriptor):
            name=ast_descriptor.name
            tb=astTextBlockToTextBlock(
                container=self.model,
                astTextBlock=ast_descriptor.textBlock)
            if name in self.scenarioModel.descriptorNamed:
                ASTNodeSourceIssue(
                    code=icode('DESCRIPTOR_TWICE'),
                    astNode=ast_descriptor,
                    level=Levels.Error,
                    message=(
                        'Descriptor "%s" already defined.'
                        ' Ignored.' % (
                            name)))
            else:
                d=Descriptor(name, tb)
                self.scenarioModel.descriptorNamed[name]=d

        def define_actor_instance(ast_actori_decl):
            actori_name=ast_actori_decl.actorInstanceName
            actor_name=ast_actori_decl.actorName
            if actor_name not in self.usecaseModel.actorNamed:
                ASTNodeSourceIssue(
                    code=icode('ACTOR_NOT_FOUND'),
                    astNode=ast_actori_decl,
                    level=Levels.Error,
                    message=(
                        'Actor "%s" does not exist.'
                        ' "%s" ignored.' % (
                            actor_name,
                            actori_name
                        )))
            else:
                actor=self.usecaseModel.actorNamed[actor_name]
                #TODO: check not already defined
                ActorInstance(
                    model=self.scenarioModel,
                    name=actori_name,
                    actor=actor,
                    astNode=ast_actori_decl
                )

        def define_story_node(astStep):
            # do not define children steps here
            step= Story(
                model=self.model,
                astNode=astStep)
            return step

        def define_text_block_node(parent, astStep):
            # do not define children steps here
            text_block = astTextBlockToTextBlock(
                container=parent,
                astTextBlock=astStep.textBlock)
            step = AnnotatedTextBlockStep(
                parent=parent,
                textBlock=text_block,
                astNode=astStep)
            return step

        def define_usecase_node(parent, astStep):
            ain=astStep.actorInstanceName
            #TODO: check that actor has to right to perform uc
            if ain not in self.scenarioModel.actorInstanceNamed:
                ASTNodeSourceIssue(
                    code=icode('ACTOR_INSTANCE_NOT_FOUND'),
                    astNode=astStep,
                    level=Levels.Fatal,
                    message=(
                        'Actor instance "%s" does not exist.' % (
                            ain
                        )))
            actor_instance=(
                self.scenarioModel.actorInstanceNamed[ain])
            un=astStep.usecaseName
            if un not in self.usecaseModel.system.usecaseNamed:
                ASTNodeSourceIssue(
                    code=icode('USECASE_NOT_FOUND'),
                    astNode=astStep,
                    level=Levels.Fatal,
                    message=(
                        'Usecase "%s" does not exist.' % (
                            un
                        )))
            usecase=self.usecaseModel.system.usecaseNamed[un]
            step = UsecaseInstanceStep(
                parent=parent,
                actorInstance=actor_instance,
                usecase=usecase,
                astNode=astStep
            )
            return step

        def define_step_hierarchy(parent, astNode):
            #type: (Optional[Step], 'ASTStep') -> Step
            # The parameter parent will be None only for the story
            type_ = astNode.__class__.__name__
            if type_ in [
                'StoryPart',
                'ATextBlockStep',
                'UsecaseInstanceStep']:
                if type_=='StoryPart':
                    step=define_story_node(astNode)
                elif type_=='ATextBlockStep':
                    step=define_text_block_node(parent, astNode)
                elif type_=='UsecaseInstanceStep':
                    step=define_usecase_node(parent, astNode)
                else:
                    raise NotImplementedError(
                        'AST type not expected: %s' % type_)
                for child_ast_step in astNode.steps:
                    define_step_hierarchy(
                        parent=step,
                        astNode=child_ast_step
                    )
                return step
            elif type_=='ObjectCreation':
                return define_object_creation(parent, astNode)
            elif type_=='ObjectDeletion':
                return define_object_deletion(parent, astNode)
            elif type_=='AttributeAssignment':
                return define_attribute_assignment(parent, astNode)
            elif type_=='LinkOperation':
                return define_link_operation(parent, astNode)
            elif type_=='CheckOperation':
                return define_check_operation(parent, astNode)
            else:
                raise NotImplementedError(
                    'AST type not expected: %s' % type_)

        def define_object_creation(parent, ast_operation):
            on=ast_operation.objectDeclaration.name
            cn=ast_operation.objectDeclaration.type
            if cn not in self.classModel.classNamed:
                ASTNodeSourceIssue(
                    code=icode('OBJECT_CLASS_NOT_FOUND'),
                    astNode=ast_operation,
                    level=Levels.Fatal,
                    message=(
                        'Class "%s" does not exist.' % cn))
            else:
                step=ObjectCreation(
                    parent=parent,
                    objectName=on,
                    class_=self.classModel.classNamed[cn],
                    astNode=ast_operation
                )
                return step

        def define_object_deletion(parent, ast_operation):
            #TODO: check if binding object name is good
            #   The name of the object is unique, but it might
            #   be deleted. So replacing the name by the actual
            #   object would imply having a minimal notion of state.
            step=ObjectDeletion(
                    parent=parent,
                    objectName=ast_operation.name,
                    astNode=ast_operation
            )
            return step

        def define_attribute_assignment(parent, ast_operation):
            assert ast_operation.verb in ['set', 'update']
            # TODO: should the name of the object be bound ?
            #     This means checking that it has not been deleted
            #     and therefore this necessitate the notion of
            #     evaluation (this could be beyond simple parsing
            #     as here).
            slot_decl=ast_operation.slotDeclaration
            step=AttributeAssignment(
                parent=parent,
                objectName=slot_decl.object,
                attributeName=slot_decl.attribute,
                value=slot_decl.value,
                update=(ast_operation.verb=='update'),
                astNode=ast_operation
            )
            return step

        def define_link_operation(parent, ast_operation):
            link_decl=ast_operation.linkDeclaration
            an=link_decl.association
            if an not in self.classModel.associationNamed:
                ASTNodeSourceIssue(
                    code=icode('LINK_ASSOC_NOT_FOUND'),
                    astNode=ast_operation,
                    level=Levels.Fatal,
                    message=(
                        'Association "%s" does not exist.' % an))
            assoc=self.classModel.associationNamed[an]
            if ast_operation.verb=='create':
                step=LinkCreation(
                    parent=parent,
                    sourceObjectName=link_decl.source,
                    targetObjectName=link_decl.target,
                    association=assoc,
                    astNode=ast_operation
                )
                return step
            elif ast_operation.verb=='delete':
                step=LinkDeletion(
                    parent=parent,
                    sourceObjectName=link_decl.source,
                    targetObjectName=link_decl.target,
                    association=assoc,
                    astNode=ast_operation
                )
                return step
            else:
                raise NotImplementedError(
                    'Verb not expected: %s' % ast_operation.verb)

        def define_check_operation(parent, ast_operation):
            step=Check(
                parent=parent,
                astNode=ast_operation
            )
            return step

        ast_root=self.ast.model
        # descriptors
        for descriptor in ast_root.descriptors:
            define_descriptor(descriptor)
        # actor instances
        ap = ast_root.actorPart
        if ap is not None:
            for actori_decl in ap.actorInstanceDeclarations:
                define_actor_instance(actori_decl)
        # context
        # TODO: implement the interpretation of context block
        # story and step hierarchy
        if ast_root.storyPart is not None:
            self.scenarioModel.story=define_step_hierarchy(
                parent=None, # set to None anyway, this is ok
                astNode=ast_root.storyPart)
        else:
            self.scenarioModel.story=None

    def resolve(self):
        pass

METAMODEL.registerSource(ScenarioEvaluationModelSource)