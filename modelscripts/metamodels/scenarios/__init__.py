# coding=utf-8
"""
Metamodel representing scenarios.

The structure of is the following::

    ScenarioModel
    ---> ClassModel
    ---> UseCaseModel
    ---> PermissionModel
    <>--* ActorInstance
    <>--* Context (contexts)
    <>--* Fragment (fragments)
    <>--1 Scenario (scenarios)


    ActorInstance
    ---- name
    ---- Actor

    StoryContainer
    ---> Story
    <|-- Context
    <|-- Fragment
    <|-- Scenario
    <|-- ObjectModelStoryContainer
"""

from collections import OrderedDict

from typing import Optional, Dict, List, Text, Union
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
from modelscripts.metamodels.objects import (
    ObjectModel,
    METAMODEL as OBJECT_METAMODEL
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
    Story,
    AbstractStoryCollection,
    AbstractStoryId
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
    """

    """
    META_COMPOSITIONS=[
        'actorInstances',
        # 'stories',
    ]

    def __init__(self):
        #type: () -> None

        super(ScenarioModel, self).__init__()

        self._classModel='*not yet*'
        #type: Optional[ClassModel]
        # Will be none or class model
        # see property

        self._usecaseModel='*not yet*'
        #type: Optional[UsecaseModel]
        # see property

        self._permissionModel='*not yet*'
        #type: Optional[UCPermissionModel]
        # see property

        self._objectModel='*not yet*'
        #type: Optional[ObjectModel]
        # see property

        self.actorInstanceNamed=OrderedDict()
        #type: Dict[Text, ActorInstance]
        # set later

        self.containerCollection=StoryContainerCollection(self)
        #type: StoryContainerCollection
        # The collection of all story container.




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
    def objectModel(self):
        #type: ()-> Optional[ObjectModel]
        if self._objectModel == '*not yet*':
            self._objectModel=self.theModel(
                OBJECT_METAMODEL,
                acceptNone=True)
        return self._objectModel

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

    @property
    def contexts(self):
        return self.containerCollection.storyContainers(
            kind='context')

    def context(self, name):
        return self.containerCollection.storyContainer(
            kind='context',
            name=name)

    @property
    def contextNames(self):
        return self.containerCollection.storyContainerNames(
            kind='context')


    @property
    def fragments(self):
        return self.containerCollection.storyContainers(
            kind='fragment')

    def fragment(self, name):
        return self.containerCollection.storyContainer(
            kind='fragment',
            name=name)

    @property
    def fragmentNames(self):
        return self.containerCollection.storyContainerNames(
            kind='fragment')


    @property
    def scenarios(self):
        return self.containerCollection.storyContainers(
            kind='scenario')

    def scenario(self, name):
        return self.containerCollection.storyContainer(
            kind='scenario',
            name=name)

    @property
    def scenarioNames(self):
        return self.containerCollection.storyContainerNames(
            kind='scenario')

    @property
    def actorInstances(self):
        return self.actorInstanceNamed.values()

    @property
    def actorInstanceNames(self):
        return self.actorInstanceNamed.keys()

    def addContainer(self, kind, name, container):
        self.containerCollection.add(kind, name, container)

    @property
    def metrics(self):
        #type: () -> Metrics
        ms=super(ScenarioModel, self).metrics
        ms.addList((
            ('actor instance', len(self.actorInstances)),
            ('context', len(self.contexts)),
            ('fragment', len(self.fragments)),
            ('scenario', len(self.scenarios)),
        ))
        # object model not included. Not sure if useful.
        containers=self.contexts+self.fragments+self.scenarios
        stories=[
            c.story for c in containers]
        ms.collect(stories)
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


STORY_KIND=['objectModel', 'context', 'scenario', 'fragment']


class StoryContainer(SourceModelElement, Subject):
    """
    Container of a story. This abstract class is useful to
    deal with common characteristics of Context, Fragment and
    Scenario at the same time. These are basically just story block.
    """
    __metaclass__ = ABCMeta

    def __init__(self,
                 model, name,
                 story,
                 storyEvaluation=None,
                 astNode=None, lineNo=None, description=None):
        super(StoryContainer, self).__init__(
            model=model,
            name=name,
            astNode=astNode,
            lineNo=lineNo,
            description=description)

        self.story=story
        #type: Story

        self.storyEvaluation=storyEvaluation
        #type: Optional[StoryEvaluation]

    @property
    def superSubjects(self):
        """ Direct parents """
        # type: () -> List[Subject]
        return [self.model]

    @property
    def subjectLabel(self):
        """
        Label of story.
        """
        return self.name

class Context(StoryContainer):
    """
    A named context. Part of a scenario model.
    """
    def __init__(self,
                 model, name,
                 story,
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


class Fragment(StoryContainer):
    """
    A named fragment. Part of a scenario model.
    Note that 'fragment" are called "story" in the concrete syntax.
    """

    def __init__(self,
                 model, name,
                 story,
                 storyEvaluation=None,
                 astNode=None, lineNo=None, description=None):
        super(Fragment, self).__init__(
            model=model,
            name=name,
            story=story,
            storyEvaluation=storyEvaluation,
            astNode=astNode,
            lineNo=lineNo,
            description=description)


class Scenario(StoryContainer):
    """
    A named scenario. Part of a scenario model.
    """

    def __init__(self,
                 model,
                 name, story,
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


class ObjectModelStoryContainer(StoryContainer):
    """
    A reference to the object model, seen as a story reference.
    This class does not comes from a AST element.
    (in fact it could be the import statement itself, but this
    requires a bit of investigation).
    """
    def __init__(self,
                 scenarioModel,
                 objectModel):
        #type: (ScenarioModel, ObjectModel) -> None
        # Not sure if this initialization is ok
        super(ObjectModelStoryContainer, self).__init__(
            model=scenarioModel,
            name='',
            story=objectModel.story,
            storyEvaluation=objectModel.storyEvaluation,
            astNode=None,
            lineNo=None,
            description=None)
        self.objectModel=objectModel
        #type: ObjectModel




class StoryId(AbstractStoryId):

    def __init__(self, kind, name):
        assert(kind in STORY_KIND)
        self.kind=kind
        #type: Text

        self.name=name
        #type: Text
        # '' for object model.
        # The name of the story container otherwise

    def __str__(self):
        return 'StoryId(%s,%s)' % (self.kind, self.name)

class StoryContainerCollection(AbstractStoryCollection):
    """
    Container for all story containers of a scenario model,
    story containers being:
    - the object model imported (kind='objectModel')
    - contexts defined in the model (kind='context')
    - fragments defined in the model (kind='fragment')
    - scenarios defined in the model (kind='scenario')
    This collection contains StoryContainer but serve
    also as an implemenation of AbstractStoryCollection
    by implementing story(storyId).
    """

    def __init__(self, model):
        self.model=model
        #type: ScenarioModel

        self.storyContainerByKindName=OrderedDict()
        #type: Dict[Text, Dict[Text, StoryContainer]]
        # Story containers indexed by story kind and then
        # by story name (the name of the story is the name
        # of the container.

    def add(self, kind, name, container):
        #type: (Text, Text, StoryContainer) -> None
        if kind not in self.storyContainerByKindName:
            self.storyContainerByKindName[kind]=OrderedDict()
        self.storyContainerByKindName[kind][name]=container

    def storyContainer(self, kind, name):
        #type: (Text, Text) -> Optional[StoryContainer]
        if kind not in self.storyContainerByKindName:
            return None
        else:
            story_by_name=self.storyContainerByKindName[kind]
            if name not in story_by_name:
                return None
            else:
                return story_by_name[name]

    def storyContainerNames(self, kind):
        if kind not in self.storyContainerByKindName:
            return []
        else:
            return self.storyContainerByKindName[kind].keys()

    def storyContainers(self, kind):
        if kind not in self.storyContainerByKindName:
            return []
        else:
            return self.storyContainerByKindName[kind].values()

    def story(self, storyId):
        #type: (StoryId) -> Optional[Story]
        """
        Implement the 'story(storyId) method so that this
        "container" collection behaves like a "story" collection.
        """
        container=self.storyContainer(
            storyId.kind,
            storyId.name)
        if container is None:
            return None
        else:
            return container.story


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