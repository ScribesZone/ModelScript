# coding=utf-8

"""
Simple metamodel for object states. Contains definitions for:

    ObjectModel
    <>--* Object
        <>--* Slot
    <>--* Link
    <>--* LinkObject

    StateElement
    <|-- Object
    <|-- Link

    Link, Object
    <|-- LinkObject
"""


from collections import OrderedDict

from typing import List, Optional, Dict
from modelscripts.base.metrics import Metrics
from modelscripts.megamodels.metamodels import Metamodel
from modelscripts.megamodels.models import Model
from modelscripts.megamodels.dependencies.metamodels import (
    MetamodelDependency
)

__all__=(
    'ObjectModel',
    'StateElement',
    'Object',
    'Slot',
    'Link',
    'LinkObject',
)

class ObjectModel(Model):
    def __init__(self):
        super(ObjectModel, self).__init__()
        self.objects = []
        # type: List[Object]

        self.links = []
        # type: List[Link]

        self.linkObjects = []
        # type: List[LinkObject]

    @property
    def metrics(self):
        #type: () -> Metrics
        ms=super(ObjectModel, self).metrics
        ms.addList((
            ('object', len(self.objects)),
            ('link', len(self.links)),
            ('linkObject', len(self.linkObjects)),
            ('slot',sum(
                len(o.slots)
                for o in self.objects)),
        ))
        return ms

    @property
    def metamodel(self):
        #type: () -> Metamodel
        return METAMODEL

class StateElement(object):
      pass



class Object(StateElement):

    def __init__(self, classifier, name):

        StateElement.__init__(self)
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

        # Slot of the object sorted by attribute name
        self.slotNamed = OrderedDict()
        # type: Dict[str, Slot]

    def assign(self, object, attribute, value):
        #TODO: check that the attribute pertains to the class
        #       or to a superclass
        self.slotNamed[attribute.name]=Slot(
            object=object,
            attribute=attribute,
            value=value
        )

    @property
    def slots(self):
        return list(self.slotNamed.values())

    def delete(self):
        #TODO:  implement delete operation on objects

        raise NotImplementedError('Delete operation on objects is not implemented')


class Slot(StateElement):

    def __init__(self, object, attribute, value):
        super(Slot, self).__init__(object.state)
        self.object=object
        self.attribute=attribute
        self.value=value


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
        #TODO:  implement delete operation on link objects
        raise NotImplementedError('Delete operation on link object is not implemented')

METAMODEL = Metamodel(
    id='ob',
    label='object',
    extension='.obs',
    modelClass=ObjectModel
)
MetamodelDependency(
    sourceId='ob',
    targetId='gl',
    optional=True,
    multiple=True,
)
MetamodelDependency(
    sourceId='ob',
    targetId='ob',
    optional=True,
    multiple=True,
)
MetamodelDependency(
    sourceId='ob',
    targetId='cl',
    optional=True,
    multiple=True,
)