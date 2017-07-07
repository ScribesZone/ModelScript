# coding=utf-8

"""
Simple metamodel for object states. Contains definitions for:

- State,
- Object,
- Link,
- LinkObject.
"""
from typing import List, Optional
from collections import OrderedDict
from pyuseocl.metamodel.model import Class, Association, AssociationClass

class State(object):
    def __init__(self, name=None):
        self.name=name

        self.objects = []
        # type: List[Object]

        self.links = []
        # type: List[Link]

        self.linkObjects = []
        # type: List[LinkObject]


class StateElement(object):
    def __init__(self, state):
        self.state = state


class Object(StateElement):
    def __init__(self, state, class_, name=None):
        super(Object,self).__init__(state)
        state.objects.append(self)
        self.name = name
        # type: Optional[str]
        self.class_ = class_
        self.attributes = OrderedDict()

    def delete(self):
        raise NotImplementedError

    # def set(self, name, value):
    #     self.attributes[name] = value



class Link(StateElement):
    def __init__(self, state, association, objects):
        super(Link, self).__init__(state)
        state.links.append(self)
        self.association = association
        self.roles = objects

    def delete(self):
        self.state.links=[l for l in self.state.links if l != self]


class LinkObject(StateElement):
    def __init__(self, state, associationClass, objects, name=None) :
        super(LinkObject, self).__init__(state)

        state.linkObjects.append(self)

        self.name = name
        # list: Optional[str]

        self.associationClass = associationClass
        self.attributes = OrderedDict()
        self.roles = objects

    def set(self, name, value):
        self.attributes[name] = value

    def delete(self):
        self.state.links=[l for l in self.state.links if l != self]




