# coding=utf-8
"""
Metamodel representing scenarios.

The structure of is the following::

    ScenarioModel
    ---> ClassModel
    ---> UseCaseModel
    ---> PermissionModel
    <>--* ActorInstance
    <>--* Story (contexts)
    <>--1 Story (scenarios)

    ActorInstance
    ---- name
    ---- Actor

    StoryBlock A
    ---> Story
    ---> StoryEvaluation
"""

# TODO: add support for  'include <x.obs>

from collections import OrderedDict

from typing import Optional, Dict, List, Text
from abc import ABCMeta

from modelscripts.base.metrics import Metrics
from modelscripts.megamodels.elements import SourceModelElement
from modelscripts.megamodels.metamodels import Metamodel
from modelscripts.megamodels.models import Model
from modelscripts.megamodels.dependencies.metamodels import (
    MetamodelDependency
)
from modelscripts.metamodels.classes import (
    ClassModel,
    METAMODEL as CLASS_METAMODEL
)
from modelscripts.metamodels.permissions import (
    UCPermissionModel,
    METAMODEL as UCPERMISSION_METAMODEL
)
from modelscripts.metamodels.permissions.sar import Subject
from modelscripts.metamodels.usecases import (
    Actor,
    System,
    UsecaseModel,
    METAMODEL as USECASE_METAMODEL
)
from modelscripts.metamodels.stories import (
    Story
)
from modelscripts.metamodels.stories.evaluations import (
    StoryEvaluation
)
META_CLASSES=(
    'ScenarioModel',
    'ActorInstance',
)

__all__=META_CLASSES

DEBUG=3

class ScenarioModel(Model, Subject):
    META_COMPOSITIONS=[
        'actorInstances',
        # 'stories',
    ]
    # TODO: add the inplace object model

    def __init__(self):
        #type: () -> None

        super(ScenarioModel, self).__init__()

        self._classModel='*not yet*'
        # Will be none or class model
        # see property

        self._usecaseModel='*not yet*'
        # see property

        self._permissionModel='*not yet*'
        # see property

        self.actorInstanceNamed=OrderedDict()
        #type: Dict[Text, ActorInstance]
        # set later

        self._contextNamed=OrderedDict()
        #type: Dict[Text, Context]

        self._scenarioNamed=OrderedDict()
        #type: Dict[Text, Scenario]


    @property
    def metamodel(self):
        #type: () -> Metamodel
        return METAMODEL

    @property
    def classModel(self):
        #type: ()-> Optional[ClassModel]
        if self._classModel == '*not yet*':
            self._classModel=self.theModel(
                CLASS_METAMODEL,
                acceptNone=True)
        return self._classModel

    @property
    def usecaseModel(self):
        #type: ()-> Optional[UsecaseModel]
        if self._usecaseModel == '*not yet*':
            self._usecaseModel=self.theModel(
                USECASE_METAMODEL,
                acceptNone=True)
        return self._usecaseModel

    @property
    def permissionModel(self):
        #type: ()-> Optional[ClassModel]
        if self._permissionModel == '*not yet*':
            self._permissionModel=self.theModel(
                UCPERMISSION_METAMODEL,
                acceptNone=True)
        return self._permissionModel

    @property
    def superSubjects(self):
        return []

    def context(self, name):
        if name in self._contextNamed:
            return self._contextNamed[name]
        else:
            return None

    @property
    def contexts(self):
        #type: () -> List[Context]
        return self._contextNamed.values()

    def scenario(self, name):
        if name in self._scenarioNamed:
            return self._scenarioNamed[name]
        else:
            return None

    @property
    def scenarios(self):
        #type: () -> List[Context]
        return self._scenarioNamed.values()

    @property
    def actorInstances(self):
        return self.actorInstanceNamed.values()

    @property
    def actorInstanceNames(self):
        return self.actorInstanceNamed.keys()

    @property
    def metrics(self):
        #type: () -> Metrics
        ms=super(ScenarioModel, self).metrics
        ms.addList((
            #TODO: add metrics
            ('actor instance', len(self.actorInstances)),
        ))
        return ms


class ActorInstance(SourceModelElement, Subject):
    def __init__(self, model, name, actor,
                 astNode=None, lineNo=None, description=None):
        super(ActorInstance, self).__init__(
            model=model,
            name=name,
            astNode=astNode,
            lineNo=lineNo,
            description=description)

        self.actor=actor
        # type: Actor
        model.actorInstanceNamed[self.name]=self

    @property
    def superSubjects(self):
        return [self.actor]


class StoryBlock(SourceModelElement):
    """
    Container of story. This abstract class is useful to
    deal with common characteristics of Context and Scenario
    at the same time, since both are basically StoryContainer.
    A story block contains:
    *   a story
    *   a story evaluation. This makes sense since there is only
        one evaluation for the context and for one main scenario.
    """
    __metaclass__ = ABCMeta

    def __init__(self, model, name, story,
                 storyEvaluation=None,
                 astNode=None, lineNo=None, description=None):
        super(StoryBlock, self).__init__(
            model=model,
            name=name,
            astNode=astNode,
            lineNo=lineNo,
            description=description)

        self.story=story
        #type: Story

        self.storyEvaluation=storyEvaluation
        #type: Optional[StoryEvaluation]


class Context(StoryBlock):
    def __init__(self, model, name, story,
                 storyEvaluation=None,
                 astNode=None, lineNo=None, description=None):
        super(Context, self).__init__(
            model=model,
            name=name,
            story=story,
            storyEvaluation=storyEvaluation,
            astNode=astNode,
            lineNo=lineNo,
            description=description)



class Scenario(StoryBlock):
    def __init__(self, model, name, story,
                 storyEvaluation=None,
                 astNode=None, lineNo=None, description=None):
        super(Scenario, self).__init__(
            model=model,
            name=name,
            story=story,
            storyEvaluation=storyEvaluation,
            astNode=astNode,
            lineNo=lineNo,
            description=description)





METAMODEL = Metamodel(
    id='sc',
    label='scenario',
    extension='.scs',
    modelClass=ScenarioModel,
    modelKinds=('', 'informal', 'preliminary', 'detailed')
)
MetamodelDependency(
    sourceId='sc',
    targetId='gl',
    optional=True,
    multiple=True,
)
MetamodelDependency(
    sourceId='sc',
    targetId='cl',
    optional=True,
    multiple=False,
)
MetamodelDependency(
    sourceId='sc',
    targetId='ob',
    optional=True,
    multiple=False,
)
MetamodelDependency(
    sourceId='sc',
    targetId='us',
    optional=True,
    multiple=False,
)
MetamodelDependency(
    sourceId='sc',
    targetId='pe',
    optional=True,
    multiple=False,
)