# coding=utf-8

"""
Simple metamodel for object states. Contains definitions for:

    ObjectModel
    <>--* Object
    <>--* Link
    <>--* LinkObject

    StateElement
    <|-- Object
    <|-- Link

    Link, Object
    <|-- LinkObject
"""


from typing import List, Optional, Dict
from collections import OrderedDict
from modelscripts.utils import Model
from modelscripts.metamodels.classes import (
    Class,
    Attribute,
    Association,
    AssociationClass,
)

class ObjectModel(Model):
    def __init__(self, source=None, name=None):
        super(ObjectModel, self).__init__(source=source)

        self.name=name

        self.objects = []
        # type: List[Object]

        self.links = []
        # type: List[Link]

        self.linkObjects = []
        # type: List[LinkObject]

    def status(self):
        return (
            '%i objects\n%i links\n%i link objects' % (
            len(self.objects),
            len(self.links),
            len(self.linkObjects)
        ))

class StateElement(object):
    def __init__(self, state):
        self.state = state



class Object(StateElement):

    _last_indexes=dict()
    # type: Dict[str,int]
    # last index for a given class name
    # This allow to have id likes _Person1, _Employee2

    def __init__(self, state, classifier, name=None):

        # FIXME: mix between id and name
        # There should be 3 concepts. Consider := R('lila')
        # - the variable name is currently refered as 'name'
        #   in parsing and here. Not necessarily define or
        #   can be ambuguious because of multiple assignement
        # - the label just like 'lila'. it can be defined or not
        #   this is what is displayed in the object diagram
        #   CURRENT we display the name. Which is wrong
        # - the uid always defined. it is used to produce graph
        #    is computed as below. Currenty the notion of
        #   label is not implemented or clearly defined.
        # To fix this, changes in 'scenario.py',
        # 'objects/parser.py', this file and the puml generator
        def _get_uid():
            if self.name is not None:
                return self.name
            else:
                cn = self.classifier.name
                if cn not in self._last_indexes:
                    self._last_indexes[cn] = 1
                else:
                    self._last_indexes[cn] += 1
                return ('_%s%i' % (
                    cn,
                    self._last_indexes[cn]
                ))

        StateElement.__init__(self, state)
        state.objects.append(self)

        # type: Optional[str]


        self.classifier = classifier
        #: this is a Class but can be AssociationClass for subtype

        self.name = name
        # type: Optional[str]
        #: name is the display name of the object

        self.uid = _get_uid()
        # type: str
        #: a unique id like  'reslili'  or '_Residence2'

        # The solution below avoid to create a Slot class
        # Here atribute names are directly
        self.slotNamed = OrderedDict()
        # type: Dict[str,Attribute]

    def delete(self):
        raise NotImplementedError



class Link(StateElement):
    def __init__(self, state, classifier, objects):
        super(Link, self).__init__(state)
        state.links.append(self)
        self.classifier = classifier
        self.roles = objects

    def delete(self):
        self.state.links=[l for l in self.state.links if l != self]


class LinkObject(Object, Link):
    def __init__(self, state, classifier, objects, name=None) :
        Object.__init__(
            self,
            state=state,
            classifier=classifier,
            name=name,
        )
        # remove it from the list of objects just changed
        state.objects = [o for o in state.objects if o!=self]
        Link.__init__(
            self,
            state=state,
            classifier=classifier,
            objects=objects,
        )
        # remove it from the list of objects just changed
        state.links = [l for l in state.links if l!=self]

        state.linkObjects.append(self)

    def delete(self):
        raise NotImplementedError