# coding=utf-8
"""
Parser of scenario. This parser package creates ScenarioModelSource.
"""

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
    Context,
    Scenario,
    METAMODEL
)
# from modelscripts.metamodels.scenarios.operations import (
#     ObjectCreation,
#     ObjectDeletion,
#     AttributeAssignment,
#     LinkCreation,
#     LinkDeletion,
#     # TODO: LinkObject
#     Check
# )
from modelscripts.metamodels.objects import (
    ObjectModel,
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
    'DESCRIPTOR_TWICE':'sc.syn.Descriptor.Twice',
    'ACTOR_NOT_FOUND':'sc.syn.ActorInstance.NoActor',
    # 'ACTOR_INSTANCE_NOT_FOUND':'sc.syn.Story.NoActorInstance',
    # 'USECASE_NOT_FOUND':'sc.syn.Story.NoUsecase',
    # 'OBJECT_CLASS_NOT_FOUND':'sc.syn.ObjectCreation.NoClass',
    # 'LINK_ASSOC_NOT_FOUND':'sc.syn.LinkOperation.NoAssoc'
}
def icode(ilabel):
    return ISSUES[ilabel]


class ScenarioModelSource(ASTBasedModelSourceFile):

    def __init__(self, fileName):
        #type: (Text) -> None
        this_dir=os.path.dirname(os.path.realpath(__file__))
        super(ScenarioModelSource, self).__init__(
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
    def objectModel(self):
        #type: () -> Optional[ObjectModel]
        # TODO: the optional stuff should come from metamdel
        return self.importBox.model('ob', optional='True')

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

        #TODO: validate the existence of Actor
        #TODO: validate the existence of Verb

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


        def define_actor_part(ast_actor_part):
            # ap = ast_actor_part.actorPart
            # if ap is not None:
                for actori_decl in ast_actor_part.actorInstanceDeclarations:
                    define_actor_instance(actori_decl)

        def define_context(ast_context):
            name='' if ast_context.name is None else ast_context.name
            context_filler = StoryFiller(
                model=self.scenarioModel,
                contextMessage='contexts',
                allowDefinition=True,
                allowAction=False,
                allowVerb=False,
                astStory=ast_context.story)
            story=context_filler.story()
            #TODO: check for existing name -> error
            self.scenarioModel._contextNamed[name]=(
                Context(
                    model=self.scenarioModel,
                    name=name,
                    story=story,
                    # TODO: launch evaluation
                    storyEvaluation=None, # filled in resolve
                    astNode=ast_context
                )
            )

        def define_scenario(ast_scenario):
            name='' if ast_scenario.name is None else ast_scenario.name
            scenario_filler = StoryFiller(
                model=self.scenarioModel,
                contextMessage='scenarios',
                allowDefinition=False,
                allowAction=True,
                allowVerb=True,
                astStory=ast_scenario.story)
            story=scenario_filler.story()
            #TODO: check for existing name -> error
            self.scenarioModel._scenarioNamed[name]=(
                Scenario(
                    model=self.scenarioModel,
                    name=name,
                    story=story,
                    # TODO: launch evaluation
                    storyEvaluation=None, # filled in resolve
                    astNode=ast_scenario
                )
            )

        ast_root=self.ast.model

        #---- descriptors -----------------------------------
        for descriptor in ast_root.descriptors:
            define_descriptor(descriptor)

        for declaration in ast_root.declarations:
            type_=declaration.__class__.__name__
            if type_=='ActorInstancePart':
                define_actor_part(declaration)
            elif type_=='Context':
                define_context(declaration)
            elif type_=='Scenario':
                define_scenario(declaration)
            else:
                raise NotImplementedError(
                    'AST type not expected: %s' % type_)

    def resolve(self):

        def resolve_context(context):
            state=ObjectModel()
            evaluator = StoryEvaluator(
                initialState=state,
                permissionSet=None)
            context.storyEvaluation = evaluator.evaluateStory(
                context.story)

        def resolve_scenario(scenario):
            state=ObjectModel()
            print('ZZ'*10, 'Evaluation scenario', scenario)
            evaluator = StoryEvaluator(
                initialState=state,
                permissionSet=None)
            scenario.storyEvaluation = evaluator.evaluateStory(
                scenario.story)

        for context in self.scenarioModel.contexts:
            resolve_context(context)

        for scenario in self.scenarioModel.scenarios:
            resolve_scenario(scenario)

METAMODEL.registerSource(ScenarioModelSource)