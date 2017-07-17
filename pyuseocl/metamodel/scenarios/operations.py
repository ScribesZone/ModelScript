# coding=utf-8

from typing import Union, Optional, Dict, List, Text
from abc import ABCMeta, abstractmethod
from pyuseocl.source.sources import SourceElement

from pyuseocl.metamodel.classes import (
    Class,
    Association,
    AssociationClass,
    Attribute,
)
from pyuseocl.metamodel.objects import (
    Object, Link, LinkObject,
)
from pyuseocl.metamodel.accesses import (
    Access,
)

#--------------------------------------------------------------
#   Operations
#--------------------------------------------------------------

class StateOperation(SourceElement):
    __metaclass__ = ABCMeta

    def __init__(self,
        block, name=None,
        code=None, lineNo=None, docComment=None, eolComment=None):
        super(StateOperation, self).__init__(name, code, lineNo, docComment, eolComment)
        # self.scenario=scenario
        # self.scenario.operations.append(self)
        self.block=block
        self.block.operations.append(self)
        self.block.scenario.originalOrderOperations.append(self)

    @abstractmethod
    def execute(self, env, state):
        pass

class ObjectCreation(StateOperation):
    """
    """
    def __init__(self, block,
                 variableName, class_, id=None,
                 code=None, lineNo=None, docComment=None, eolComment=None):
        super(ObjectCreation, self).__init__(block, variableName, code, lineNo, docComment, eolComment)

        self.class_=class_
        # type: Class

        self.id=id
        # type: Optional[str]


    def execute(self, env, state):

        o=Object(state, self.class_,
                 name=self.name)
        env[self.name]=o
        Access('C', self.class_, self.block.accessSet)

class ObjectDestruction(StateOperation):
    """
    Destruction of a regular object OR of a link object.
    """
    def __init__(self, block,
                 variableName,
                 code=None, lineNo=None, docComment=None, eolComment=None):
        super(ObjectDestruction, self).__init__(block, variableName, code, lineNo, docComment, eolComment)

    def execute(self, env, state):
        # this can be the destruction of a rgular object or of a link object
        c=env[self.name].classifier
        Access('D', c, self.block.accessSet)
        env[self.name].delete()  # TODO: check what to do with obj/linkobj
        del env[self.name]

class LinkCreation(StateOperation):
    def __init__(self, block,
                 names, association, id=None,
                 code=None, lineNo=None, docComment=None, eolComment=None):
        super(LinkCreation, self).__init__(block, None, code, lineNo, docComment, eolComment)

        self.names=names #type:List[Text]

        self.association=association
        # type: Association

        self.id=id #type:Optional[Text]

    def execute(self, env, state):
        Access('C', self.association, self.block.accessSet)
        objects=[env[n] for n in self.names]
        Link(state, self.association, objects)


class LinkDestruction(StateOperation):
    def __init__(self, block,
                 names, association,
                 code=None, lineNo=None, docComment=None, eolComment=None):
        super(LinkDestruction, self).__init__(block, None, code, lineNo, docComment, eolComment)

        self.names=names

        self.association = association
        # type: Association

    def execute(self, env, state):
        Access('D', self.association, self.block.accessSet)
        state.links=[l for l in state.links if l != self]


class LinkObjectCreation(StateOperation):
    def __init__(self, block,
                 variableName=None, names=(), id=None, associationClass=None,
                 code=None, lineNo=None, docComment=None, eolComment=None):
        super(LinkObjectCreation, self).__init__(block, variableName, code, lineNo, docComment, eolComment)
        # self.name can be None
        self.names = names
        self.id = id,

        self.associationClass = associationClass  # this is indeed an association class
        # type: AssociationClass

    def execute(self, env, state):
        Access('C', self.associationClass, self.block.accessSet)

        objects=[env[n] for n in self.names]

        lo=LinkObject(state, self.associationClass, objects, name=self.name)
        env[lo.name]=lo


class AttributeAssignment(StateOperation):
    def __init__(self, block,
                 variableName,
                 attributeName,
                 expression,
                 code=None, lineNo=None, docComment=None, eolComment=None):
        super(AttributeAssignment, self).__init__(block, None, code, lineNo, docComment, eolComment)

        self.variableName = variableName
        self.attributeName = attributeName
        # type: Attribute

        self.expression = expression

    def execute(self, env, state):
        if self.variableName not in env:
            raise ValueError(
                'Execution error %s: variable "%s" is undefined' % (
                    'at %i' % self.lineNo if self.lineNo else '',
                    self.variableName
                ))
        o = env[self.variableName]
        o.slotNamed[self.attributeName]=self.expression
        Access('U',o.classifier, self.block.accessSet)

