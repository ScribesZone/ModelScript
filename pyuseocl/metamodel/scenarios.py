# coding=utf-8
import collections
from typing import Union, Optional, Dict, List
from pyuseocl.source.sources import SourceElement
from pyuseocl.metamodel.usecases import Actor, System
from pyuseocl.metamodel.model import Class, Association, AssociationClass, Attribute


from pyuseocl.metamodel.objects import (
    State, Object, Link, LinkObject,
)


class Scenario(object):
    def __init__(self, name, system, classModel, file=None):
        self.name = name
        self.file = file
        self.system=system
        self.classModel=classModel

        self.actorInstanceNamed = collections.OrderedDict()
        #: Dict[str,ActorInstance]

        self.operations=[]
        # type: List[ModelOperation]

    def execute(self):
        state = State()
        env = collections.OrderedDict()
        for op in self.operations:
            op.execute(env, state)


class ActorInstance(SourceElement):
    def __init__(self, scenario, name, actor,
                 code=None, lineNo=None, docComment=None, eolComment=None):
        super(ActorInstance, self).__init__(name, code, lineNo, docComment, eolComment)
        self.scenario=scenario

        # type: Scenario
        self.name=name

        self.actor=actor
        # type: Actor


# class Block(object):
#     pass
#
#
# class UseCaseExecution(Block):
#     def __init__(self,
#              actorInstance, actor, usecase,
#         ):
#         self.actorInstance=actorInstance
#         # type: str|ActorInstance



class ModelOperation(SourceElement):
    def __init__(self,
                 name, code=None, lineNo=None, docComment=None, eolComment=None):
        super(ModelOperation, self).__init__(name, code, lineNo, docComment, eolComment)


class ObjectCreation(ModelOperation):
    def __init__(self,
                 variableName, class_, id=None,
                 code=None, lineNo=None, docComment=None, eolComment=None):
        super(ObjectCreation, self).__init__(variableName, code, lineNo, docComment, eolComment)

        self.class_=class_
        # type: Class

        self.id=id
        # type: Optional[str]

    def execute(self, env, state):
        o=Object(state, self.class_, name=self.id if self.id else self.name+'_')
        env.objects[self.name]=o

class ObjectDestruction(ModelOperation):
    def __init__(self,
                 variableName,
                 code=None, lineNo=None, docComment=None, eolComment=None):
        super(ObjectDestruction, self).__init__(variableName, code, lineNo, docComment, eolComment)

    def execute(self, env, state):
        env.objects[self.name].delete()
        del env.objects[self.name]

class LinkCreation(ModelOperation):
    def __init__(self,
                 names, association, id=None,
                 code=None, lineNo=None, docComment=None, eolComment=None):
        super(LinkCreation, self).__init__(None, code, lineNo, docComment, eolComment)

        self.names=names

        self.association=association
        # type: Association

        self.id=id

    def execute(self, env, state):
        objects=[env.objects[n] for n in self.names]
        Link(state, self.association, objects)

class LinkDestruction(ModelOperation):
    def __init__(self,
                 name1, name2, association,
                 code=None, lineNo=None, docComment=None, eolComment=None):
        super(LinkDestruction, self).__init__(None, code, lineNo, docComment, eolComment)

        self.name1 = name1
        self.name2 = name2

        self.association = association
        # type: Association

    def execute(self, env, state):
        state.links=[l for l in state.links if l != self]

class AttributeAssignement(ModelOperation):
    def __init__(self,
                 variableName, attribute, expression,
                 code=None, lineNo=None, docComment=None, eolComment=None):
        super(AttributeAssignement, self).__init__(None, code, lineNo, docComment, eolComment)

        self.variableName = variableName
        self.attribute = attribute
        # type: Attribute

        self.expression = expression

    def execute(self, env, state):
        raise NotImplementedError


