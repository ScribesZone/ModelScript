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