from typing import Dict

from modelscripts.metamodels.objects import (
    ObjectModel,
    ShadowObjectModel)
from modelscripts.metamodels.objects.linkobjects import LinkObject
from modelscripts.metamodels.objects.links import PlainLink
from modelscripts.metamodels.objects.objects import (
    Object,
    PlainObject,
    Slot)


class ObjectModelCopier(object):

    def __init__(self, source):
        self.o=source
        #type: ObjectModel

        self.t=ShadowObjectModel(classModel=source._classModel)
        #type: ObjectModel

        self._object_map=dict()
        #type: Dict[Object, Object]
        # A mapping between object in the original model
        # and the corresponding object in the new model.
        # This is necessary to update links.
        # Note that 'object' refers to both plain object
        # and link object.

    def copy(self):
        self.t._classModel=self.o._classModel
        # No reason the make a copy as this is just a reference.

        self.t.storyEvaluation=self.o.storyEvaluation

        # copy all object and links
        #### order is important ######
        # The mapping _object_map is created during
        # _copy_plain_object and used during _copy_plain_link.
        # TODO:3 how to deal with creation of recursive linkobjects?
        #   Check what to do ?
        #   There is a problem with the evaluation order.
        #   At worse a link object will not be found
        for po in self.o.plainObjects:
            self._copy_plain_object(po)
        for l in self.o.linkObjects:
            self._copy_link_object(l)
        for l in self.o.plainLinks:
            self._copy_plain_link(l)
        return self.t

    def _copy_plain_object(self, plain_object):

        if plain_object.package is not None:
            raise NotImplementedError(
                'The usage of package is not supported yet')

        # The step does not change. The creation of the object
        # is defined at only one place (the step)
        new_step=plain_object.step

        new_object = \
            PlainObject(
                model=self.t,
                name=plain_object.name,
                class_=plain_object.class_,
                package=plain_object.package,   # See exception above
                step=new_step,
                lineNo=plain_object.lineNo,
                description=plain_object.description,
                astNode=plain_object.astNode)
        self._object_map[plain_object]=new_object
        for slot in plain_object.slots:
            self._copy_slot(slot, new_object)

    def _copy_plain_link(self, plain_link):
        if plain_link.package is not None:
            raise NotImplementedError(
                'The usage of package is not supported yet')

        # The step does not change. The creation of the link
        # is defined at only one place (the step)
        new_step=plain_link.step

        new_link= \
            PlainLink(
                model=self.t,
                name=plain_link.name,
                association=plain_link.association,
                sourceObject=self._object_map[plain_link.sourceObject],
                targetObject=self._object_map[plain_link.targetObject],
                package=plain_link.package,
                step=new_step,
                astNode=plain_link.astNode,
                lineNo=plain_link.lineNo,
                description=plain_link.description)

    def _copy_link_object(self, link_object):
        if link_object.package is not None:
            raise NotImplementedError(
                'The usage of package is not supported yet')
        # The step does not change. The creation of the link
        # is defined at only one place (the step)
        new_step=link_object.step

        new_link_object= \
            LinkObject(
                model=self.t,
                associationClass=link_object.associationClass,
                name=link_object.name,
                sourceObject=self._object_map[link_object.sourceObject],
                targetObject=self._object_map[link_object.targetObject],
                package=link_object.package,
                step=new_step,
                astNode=link_object.astNode,
                lineNo=link_object.lineNo,
                description=link_object.description)




    def _copy_slot(self, old_slot, new_object):
        new_slot=\
            Slot(
                object=new_object,
                attribute=old_slot.attribute,
                simpleValue=old_slot.simpleValue,
                step=old_slot.step,
                description=old_slot.description,
                lineNo=old_slot.lineNo,
                astNode=old_slot.astNode)