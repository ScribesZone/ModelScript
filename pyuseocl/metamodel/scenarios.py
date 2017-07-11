# coding=utf-8
import collections
from typing import Union, Optional, Dict, List
from pyuseocl.source.sources import SourceElement
from pyuseocl.metamodel.usecases import Actor, System
from pyuseocl.metamodel.classes import Class, Association, AssociationClass, Attribute


from pyuseocl.metamodel.objects import (
    State, Object, Link, LinkObject,
)


class Scenario(object):
    def __init__(self, classModel, name, system,  file=None):
        self.name = name
        self.file = file
        self.system=system
        self.classModel=classModel

        self.actorInstanceNamed = collections.OrderedDict()
        #: Dict[str,ActorInstance]

        self.operations=[]
        # type: List[StateOperation]

    def execute(self):
        state = State()
        env = collections.OrderedDict()
        for op in self.operations:
            op.execute(env, state)
        return state


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



class StateOperation(SourceElement):
    def __init__(self, scenario,
                 name=None, code=None, lineNo=None, docComment=None, eolComment=None):
        super(StateOperation, self).__init__(name, code, lineNo, docComment, eolComment)
        self.scenario=scenario
        self.scenario.operations.append(self)



class ObjectCreation(StateOperation):
    """
    """
    def __init__(self, scenario,
                 variableName, class_, id=None,
                 code=None, lineNo=None, docComment=None, eolComment=None):
        super(ObjectCreation, self).__init__(scenario, variableName, code, lineNo, docComment, eolComment)

        self.class_=class_
        # type: Class

        self.id=id
        # type: Optional[str]


    def execute(self, env, state):

        o=Object(state, self.class_,
                 name=self.name)
        env[self.name]=o

class ObjectDestruction(StateOperation):
    """
    Destruction of a regular object OR of a link object.
    """
    def __init__(self, scenario,
                 variableName,
                 code=None, lineNo=None, docComment=None, eolComment=None):
        super(ObjectDestruction, self).__init__(scenario, variableName, code, lineNo, docComment, eolComment)

    def execute(self, env, state):
        # this can be the destruction of a rgular object or of a link object
        env[self.name].delete()  # TODO: check what to do with obj/linkobj
        del env[self.name]

class LinkCreation(StateOperation):
    def __init__(self, scenario,
                 names, association, id=None,
                 code=None, lineNo=None, docComment=None, eolComment=None):
        super(LinkCreation, self).__init__(scenario, None, code, lineNo, docComment, eolComment)

        self.names=names

        self.association=association
        # type: Association

        self.id=id

    def execute(self, env, state):
        objects=[env[n] for n in self.names]
        Link(state, self.association, objects)


class LinkDestruction(StateOperation):
    def __init__(self, scenario,
                 names, association,
                 code=None, lineNo=None, docComment=None, eolComment=None):
        super(LinkDestruction, self).__init__(scenario, None, code, lineNo, docComment, eolComment)

        self.names=names

        self.association = association
        # type: Association

    def execute(self, env, state):
        state.links=[l for l in state.links if l != self]


class LinkObjectCreation(StateOperation):
    def __init__(self, scenario,
                 variableName=None, names=(), id=None, associationClass=None,
                 code=None, lineNo=None, docComment=None, eolComment=None):
        super(LinkObjectCreation, self).__init__(scenario, variableName, code, lineNo, docComment, eolComment)
        # self.name can be None
        self.names = names
        self.id = id,

        self.associationClass = associationClass  # this is indeed an association class
        # type: AssociationClass

    def execute(self, env, state):
        objects=[env[n] for n in self.names]

        LinkObject(state, self.associationClass, objects, name=self.name)


class AttributeAssignment(StateOperation):
    def __init__(self, scenario,
                 variableName,
                 attributeName,
                 expression,
                 code=None, lineNo=None, docComment=None, eolComment=None):
        super(AttributeAssignment, self).__init__(scenario, None, code, lineNo, docComment, eolComment)

        self.variableName = variableName
        self.attributeName = attributeName
        # type: Attribute

        self.expression = expression

    def execute(self, env, state):
        o = env[self.variableName]
        o.slotNamed[self.attributeName]=self.expression


