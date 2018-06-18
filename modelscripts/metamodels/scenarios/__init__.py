# coding=utf-8
"""
Code of the Scenario metamodel.

The global structure of this metamodel is as following::

    ScenarioModel
    <>--* ActorInstance
    <>--1 Story
          <>--* Step
                <>--* Step
    Step
    <|-- Story
    <|-- AnnotatedTextBlockStep
    <|-- UsecaseInstanceStep
    <|-- Operation

Althougth the hierarchy of step is recursive the
actual structure is only two-level deep :

    Story
    <>--* UsecaseInstanceStep
        <>--* AnnotatedTextBlockStep
        <>--* Operation
    <>--* AnnotatedTextBlockStep
        <>--* Operation
    <>--* Operation
"""

# TODO: add support for  'include <x.obs>

import collections

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
)
from modelscripts.metamodels.permissions import (
    UCPermissionModel)
from modelscripts.metamodels.permissions.sar import Subject
from modelscripts.metamodels.usecases import (
    Actor,
    System,
    UsecaseModel,
)

META_CLASSES=(
    'ScenarioModel',
    'ActorInstance',
    'Step',
    'Story',
    'AnnotatedTextBlockStep',
    'UsecaseInstanceStep'
)

__all__=META_CLASSES

DEBUG=3

class ScenarioModel(Model, Subject):
    META_COMPOSITIONS=[
        'actorInstances',
        'story',
    ]
    # TODO: add the inplace object model

    def __init__(self):
        #type: () -> None

        super(ScenarioModel, self).__init__()

        self.usecaseModel=None
        #type: Optional[UsecaseModel]
        # set later

        self.classModel=None
        #type: Optional[ClassModel]
        # set later

        self.permissionModel=None
        #type: Optional[UCPermissionModel]
        # set later

        #TODO: add the inplace object model

        self.actorInstanceNamed = collections.OrderedDict()
        #type: Dict[Text, ActorInstance]
        # set later

        self.story=None
        #type: Optional[Story]
        # set later. Will never be None. At worse it will contain no step.

    @property
    def metamodel(self):
        #type: () -> Metamodel
        return METAMODEL

    @property
    def superSubjects(self):
        return []

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


class Step(SourceModelElement, Subject):
    """
    All elements in a story, including itself.
    Steps forms a hierarchy of steps, although it is not
    recursive but two levels.
    """
    __metaclass__ = ABCMeta


    def __init__(self,
                 model,
                 astNode=None,
                 lineNo=None,
                 description=None):
        super(Step, self).__init__(
            model=model,
            name=None,
            astNode=astNode,
            lineNo=lineNo,
            description=description)

        self.parentStep=None
        #type: Optional[Step]

        self.steps=[]
        #type: List[Step]

    @property
    def superSubjects(self):
        """ Direct parents """
        # type: () -> List[Subject]
        return [self.parentStep]

    @property
    def subjectLabel(self):
        parent_label=self.parentStep.subjectLabel
        nth_label=self.parentStep.steps.index(self)
        return '%s.%s' % (parent_label, nth_label)


class Story(Step):

    def __init__(self,
                 model,
                 astNode=None,
                 lineNo=None,
                 description=None):
        super(Story, self).__init__(
            model=model,
            astNode=astNode,
            lineNo=lineNo,
            description=description)

        self.parentStep=None

        model.story=self

    @property
    def superSubjects(self):
        return [self.model]

    @property
    def subjectLabel(self):
        return 'story'


class AnnotatedTextBlockStep(Step):

    def __init__(self,
                 parent,
                 textBlock,
                 astNode=None,
                 lineNo=None,
                 description=None):
        super(AnnotatedTextBlockStep, self).__init__(
            model=parent.model,
            astNode=astNode,
            lineNo=lineNo,
            description=description)

        self.textBlock=textBlock

        self.parentStep=parent
        parent.steps.append(self)


class UsecaseInstanceStep(Step):
    def __init__(self,
                 parent,
                 actorInstance,
                 usecase,
                 astNode=None,
                 lineNo=None,
                 description=None):
        super(UsecaseInstanceStep, self).__init__(
            model=parent.model,
            astNode=astNode,
            lineNo=lineNo,
            description=description)

        self.actorInstance=actorInstance
        self.usecase=usecase

        self.parentStep = parent
        parent.steps.append(self)


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