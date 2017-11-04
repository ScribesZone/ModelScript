# coding=utf-8
from __future__ import print_function

import collections

from typing import Dict, Text

from modelscribes.base.sources import SourceElement
from modelscribes.megamodels.metamodels import Metamodel
from modelscribes.megamodels.dependencies.metamodels import (
    MetamodelDependency
)

from modelscribes.megamodels.models import Model
from modelscribes.metamodels.permissions.sar import Subject


class UsecaseModel(Model):
    def __init__(self):
        super(UsecaseModel, self).__init__()
        self.system=None # Filled later

        self.actorNamed = collections.OrderedDict()
        # type: Dict[Text, Actor]

    @property
    def metamodel(self):
        #type: () -> Metamodel
        return METAMODEL

    @property
    def actors(self):
        return self.actorNamed.values()


class System(SourceElement):
    def __init__(self,
                 usecaseModel, name,
                 code=None, lineNo=None,
                 docComment=None, eolComment=None):
        super(System, self).__init__(
            name=name,
            code=code,
            lineNo=lineNo,
            docComment=docComment, eolComment=eolComment)
        self.usecaseModel = usecaseModel
        self.usecaseModel.system=self

        self.usecaseNamed = collections.OrderedDict()
        # type: Dict[str,Usecase]

    @property
    def usecases(self):
        return self.usecaseNamed.values()


class Actor(SourceElement, Subject):
    def __init__(self,
                 usModel, name, kind='human',
                 code=None, lineNo=None,
                 docComment=None, eolComment=None):
        super(Actor, self).__init__(name, code, lineNo, docComment, eolComment)

        self.usecaseModel = usModel
        self.usecaseModel.actorNamed[name]=self
        self.kind=kind # system|human
        self.superActors=[]
        self.subActors=[]
        self.usecases=[]

    def addUsecase(self, usecase):
        if usecase in self.usecases:
            return
        else:
            usecase.actors.append(self)
            self.usecases.append(usecase)

    def addSuperActor(self, actor):
        if actor in self.superActors:
            return
        else:
            actor.subActors.append(self)
            self.superActors.append(actor)


class Usecase(SourceElement, Subject):
    def __init__(self,
                 system, name,
        code=None, lineNo=None, docComment=None, eolComment=None):

        super(Usecase, self).__init__(
            name, code, lineNo, docComment, eolComment)

        self.system = system
        self.system.usecaseNamed[name]=self
        self.actors=[]

    @property
    def superSubjects(self):
        return self.actors

    def addActor(self, actor):
        if actor in self.actors:
            return
        else:
            actor.usecases.append(self)
            self.actors.append(actor)



METAMODEL = Metamodel(
    id='us',
    label='usecase',
    extension='.uss',
    modelClass=UsecaseModel,
    modelKinds=('', 'preliminary', 'detailled')
)
MetamodelDependency(
    sourceId='us',
    targetId='gl',
    optional=True,
    multiple=True,
)