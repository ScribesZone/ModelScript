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
        name, kind='human', code=None, lineNo=None, docComment=None, eolComment=None):
        super(Actor, self).__init__(name, code, lineNo, docComment, eolComment)
        self.kind=kind

class Usecase(SourceElement):
    def __init__(self,
        name, code=None, lineNo=None, docComment=None, eolComment=None):
        super(Usecase, self).__init__(name, code, lineNo, docComment, eolComment)
