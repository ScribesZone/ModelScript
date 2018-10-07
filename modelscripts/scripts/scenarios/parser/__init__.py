# coding=utf-8
"""
Parser of scenario. This parser package creates ScenarioModelSource.
"""

from __future__ import unicode_literals, print_function, absolute_import, division
from typing import Text, Union, Optional
import os

from modelscripts.base.grammars import AST
from modelscripts.megamodels.models import Model, Placeholder
from modelscripts.base.grammars import (
    ASTNodeSourceIssue)
from modelscripts.base.issues import (
    Levels,)
from modelscripts.base.exceptions import (
    UnexpectedCase)
from modelscripts.megamodels.elements import (
    Descriptor)
from modelscripts.metamodels.scenarios import (
    ScenarioModel,
    ActorInstance,
    Context,
    Fragment,
    Scenario,
    ObjectModelStoryContainer,
    StoryId,
    METAMODEL)
from modelscripts.metamodels.objects import (
    ShadowObjectModel,)
from modelscripts.metamodels.classes import (
    ClassModel)
from modelscripts.metamodels.usecases import (
    UsecaseModel)
from modelscripts.metamodels.glossaries import (
    GlossaryModel)
from modelscripts.metamodels.permissions import (
    PermissionModel)
from modelscripts.metamodels.objects import (
    ObjectModel)
from modelscripts.megamodels.sources import (
    ASTBasedModelSourceFile)
from modelscripts.scripts.textblocks.parser import (
    astTextBlockToTextBlock)
from modelscripts.scripts.stories.parser import (
    StoryFiller)
from modelscripts.metamodels.stories import (
    AbstractStoryId)
from modelscripts.metamodels.stories.evaluations.evaluator import (
    StoryEvaluator,)


__all__=(
    'ObjectModelSource'
)


DEBUG=0


ISSUES={
    'DESCRIPTOR_TWICE':'sc.syn.Descriptor.Twice',
    'ACTOR_NOT_FOUND':'sc.syn.ActorInstance.NoActor',
    'CONTEXT_TWICE':'sc.syn.Context.Twice',
    'FRAGMENT_TWICE':'sc.syn.Fragment.Twice',
    'SCENARIO_TWICE':'sc.syn.Scenario.Twice',

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
        # TODO:- the optional stuff should come from metamdel
        #   This is the same in all methods below
        return self.importBox.model('cl', optional='True')

    @property
    def usecaseModel(self):
        #type: () -> Optional[UsecaseModel]
        return self.importBox.model('us', optional='True')

    @property
    def glossaryModel(self):
        #type: () -> Optional[GlossaryModel]
        return self.importBox.model('gl', optional='True')

    @property
    def permissionModel(self):
        #type: () -> Optional[PermissionModel]
        return self.importBox.model('pe', optional='True')

    @property
    def objectModel(self):
        #type: () -> Optional[ObjectModel]
        return self.importBox.model('ob', optional='True')

    @property
    def metamodel(self):
        return METAMODEL

    def fillModel(self):
        """
        Parse the scenario source model.
        Use StoryFiller for parts that are stories.
        """

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
                #TODO:3 scenarios: check actor not already defined
                ActorInstance(
                    model=self.scenarioModel,
                    name=actori_name,
                    actor=actor,
                    astNode=ast_actori_decl
                )

        #TODO:2 scenarios: validate the existence of Actor
        #TODO:2 scenarios: validate the existence of Verb

        def define_usecase_node(parent, astStep):
            ain=astStep.actorInstanceName
            #TODO:2 check that actor has to right to perform uc
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
                storyKind='context',
                ensureCheckAfter=False,
                infoIfCheckAdded=True,
                allowDefinition=True,
                allowAction=False,
                allowVerb=False,
                allowedIncludeKinds=[],
                getStoryId=self.getStoryId,
                astStory=ast_context.story)
            story=context_filler.story()
            c=self.scenarioModel.context(name)
            if c is not None:
                ASTNodeSourceIssue(
                    code=icode('CONTEXT_TWICE'),
                    astNode=ast_context,
                    level=Levels.Error,
                    message='Context "%s" already defined.'
                            ' Previous definition ignored.' % name)
            context=\
                Context(
                    model=self.scenarioModel,
                    name=name,
                    story=story,
                    storyEvaluation=None, # filled in resolve
                    astNode=ast_context)
            story.storyContainer=context
            self.scenarioModel.containerCollection.add(
                kind='context',
                name=name,
                container=context)

        def define_fragment(ast_fragment):
            # NOTE:  While the keyword "story" is used externaly,
            # in the metamodel the term used is "fragment"
            # (Fragment inherits from Story). In the
            # concrete syntax the keyword "story" looks better.
            name=ast_fragment.name
            context_filler = StoryFiller(
                model=self.scenarioModel,
                storyKind='story', # "stories": see above
                ensureCheckAfter=False,
                infoIfCheckAdded=True,
                allowDefinition=False,
                allowAction=True,
                allowVerb=True,
                allowedIncludeKinds=[],
                getStoryId=self.getStoryId,
                astStory=ast_fragment.story)
            story=context_filler.story()
            c=self.scenarioModel.fragment(name)
            if c is not None:
                ASTNodeSourceIssue(
                    code=icode('FRAGMENT_TWICE'),
                    astNode=ast_fragment,
                    level=Levels.Error,
                    # 'Story" instead of 'fragment': see above
                    message='Story "%s" already defined.'
                            ' Previous definition ignored.'
                            % name)
            fragment=\
                Fragment(
                    model=self.scenarioModel,
                    name=name,
                    story=story,
                    storyEvaluation=None,  # filled in resolve
                    astNode=ast_fragment)
            story.storyContainer = fragment

            self.scenarioModel.containerCollection.add(
                kind='fragment',
                name=name,
                container=fragment)

        def define_scenario(ast_scenario):
            name='' if ast_scenario.name is None else ast_scenario.name
            scenario_filler = StoryFiller(
                model=self.scenarioModel,
                storyKind='scenario',
                ensureCheckAfter=True,
                infoIfCheckAdded=True,
                allowDefinition=False,
                allowAction=True,
                allowVerb=True,
                allowedIncludeKinds=[
                    'objectModel',
                    'context',
                    'fragment'],
                getStoryId=self.getStoryId,
                astStory=ast_scenario.story)
            story=scenario_filler.story()
            s=self.scenarioModel.scenario(name)
            if s is not None:
                ASTNodeSourceIssue(
                    code=icode('SCENARIO_TWICE'),
                    astNode=ast_scenario,
                    level=Levels.Error,
                    message='Scenario "%s" already defined.'
                            ' Previous definition ignored.' % name)
            scenario=\
                Scenario(
                    model=self.scenarioModel,
                    name=name,
                    story=story,
                    storyEvaluation=None,  # filled in resolve
                    astNode=ast_scenario)
            story.storyContainer = scenario

            self.scenarioModel.containerCollection.add(
                kind='scenario',
                name=name,
                container=scenario)


        ast_root=self.ast.model

        #  Initialized
        # with the object model if there is one. Otherwise nothing
        # is added, so that no object model container will be found later.
        # The parser should later
        # add contexts, fragments and scenarios.
        if self.objectModel is not None:
            container=ObjectModelStoryContainer(
                scenarioModel=self.scenarioModel,
                objectModel = self.objectModel)
            self.scenarioModel.containerCollection.add(
                kind='objectModel',
                name='',
                container=container
            )

        #---- descriptors -----------------------------------
        for descriptor in ast_root.descriptors:
            define_descriptor(descriptor)

        for declaration in ast_root.declarations:
            type_=declaration.__class__.__name__
            if type_=='ActorInstancePart':
                define_actor_part(declaration)
            elif type_=='Context':
                define_context(declaration)
            elif type_=='Fragment':
                define_fragment(declaration)
            elif type_=='Scenario':
                define_scenario(declaration)
            else:
                raise UnexpectedCase( #raise:OK
                    'AST type not expected: %s' % type_)


    #     ######################################################
    # def resolveOLD(self): ####################################
    #     ######################################################
    #
    #
    #     def state_after_object_model():
    #         # object model copy or new empty one
    #         if self.objectModel is not None:
    #             state=self.objectModel.copy()
    #         else:
    #             state=ShadowObjectModel(
    #                 classModel=self.classModel
    #             )
    #         return state
    #
    #     def resolve_context(context):
    #         # object
    #         #   then context
    #         evaluator = StoryEvaluator(
    #             initialState=state_after_object_model(),
    #             permissionSet=None)
    #         context.storyEvaluation = evaluator.evaluateStory(
    #             context.story)
    #
    #     def resolve_scenario(scenario):
    #         # context with same name if any otherwise object
    #         #   then scenario
    #         context=self.scenarioModel.context(scenario.name)
    #         if context is None:
    #             state=state_after_object_model()
    #         else:
    #             state=context.storyEvaluation.finalState.copy()
    #         evaluator = StoryEvaluator(
    #             initialState=state,
    #             permissionSet=None)
    #         scenario.storyEvaluation = evaluator.evaluateStory(
    #             scenario.story)
    #
    #     for context in self.scenarioModel.contexts:
    #         resolve_context(context)
    #
    #     for scenario in self.scenarioModel.scenarios:
    #         resolve_scenario(scenario)

    def resolve(self):

        super(ScenarioModelSource, self).resolve()

        def resolve_scenario(scenario):
            """
            Evaluate a given scenario in the context of a given
            story collection.
            """
            #---- (1) the container collection serve as the
            # story collection thanks to the method 'getStory()'.
            story_collection=self.scenarioModel.containerCollection

            #---- (1) start with an empty objec model
            initial_state=ShadowObjectModel(
                classModel=self.classModel)
            #---- (2) evaluate the given scenario
            evaluator = StoryEvaluator(
                initialState=initial_state,
                storyCollection=story_collection,
                permissionSet=None)
            #TODO:3 scenario must refer to permission model
            scenario.storyEvaluation = \
                evaluator.evaluateStory(
                    scenario.story)

        for scenario in self.scenarioModel.scenarios:
            resolve_scenario(scenario)


    def getStoryId(self, kind, name):
        """
        "Parse" and "validate" syntactically the string pair
        and return a StoryId. Note that "story" is the external way
        for user to denotes "fragments".
        This function returns None if case or "error", that is,
        when no StoryId can be build.
        This function is used as a parameter to StoryFiller.
        """
        if kind=='object':
            if name!='model':
                return None
            else:
                return StoryId('objectModel', '')
        elif kind=='story':
            return StoryId('fragment', name)
        elif kind in ['context', 'scenario']:
            return StoryId(kind, name)
        else:
            return None

METAMODEL.registerSource(ScenarioModelSource)