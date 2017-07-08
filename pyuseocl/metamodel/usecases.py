# coding=utf-8

from typing import Union, Dict
import collections
from pyuseocl.source.sources import SourceElement

class System(SourceElement):
    def __init__(self,
        name, code=None, lineNo=None, docComment=None, eolComment=None):
        super(System, self).__init__(name, code, lineNo, docComment, eolComment)

        self.actorNamed = collections.OrderedDict()
        # type: Dict[str,Actor]

        self.usecaseNamed = collections.OrderedDict()
        # type: Dict[str,Usecase]


    @property
    def actors(self):
        return self.actorNamed.values()

    @property
    def usecases(self):
        return self.usecaseNamed.values()



class Actor(SourceElement):
    def __init__(self,
        system, name, kind='human',
        code=None, lineNo=None, docComment=None, eolComment=None):

        super(Actor, self).__init__(name, code, lineNo, docComment, eolComment)

        system.actorNamed[name]=self
        self.system = system

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


class Usecase(SourceElement):
    def __init__(self,
        system, name,
        code=None, lineNo=None, docComment=None, eolComment=None):

        super(Usecase, self).__init__(name, code, lineNo, docComment, eolComment)

        system.usecaseNamed[name]=self
        self.system = system

        self.actors=[]

    def addActor(self, actor):
        if actor in self.actors:
            return
        else:
            actor.usecases.append(self)
            self.actors.append(actor)