# coding=utf-8
from __future__ import unicode_literals, print_function, absolute_import, \
    division

from typing import Optional

from modelscripts.base.modelprinters import (
    ModelPrinter,
    ModelSourcePrinter,
    ModelPrinterConfig,
)
from modelscripts.metamodels.objects import (
    ObjectModel,
    METAMODEL
)
from modelscripts.megamodels.models import (
    Placeholder
)


class ObjectModelPrinter(ModelPrinter):

    def __init__(self,
                 theModel,
                 config=None):
        #type: (ObjectModel, Optional[ModelPrinterConfig]) -> None
        super(ObjectModelPrinter, self).__init__(
            theModel=theModel,
            config=config
        )

    def doModelContent(self):
        super(ObjectModelPrinter, self).doModelContent()
        self.doObjectModel(self.theModel)
        return self.output

    def doObjectModel(self, objectModel):
        for o in objectModel.objects:
            self.doObject(o)
        for l in objectModel.links:
            self.doLink(l)
        return self.output


    def doObject(self, o):
        class_name=(
            str(o.class_)
                if isinstance(o.class_, Placeholder)
            else o.class_.name)
        self.outLine('%s %s %s' % (
                 o.name,
                 self.kwd(':'),
                 class_name))
        for s in o.slots:
            self.doSlot(s)

        return self.output

    def doSlot(self, slot):
        print('TT'*10, )
        attribute_name=(
            str(slot.attribute) if isinstance(slot.attribute, Placeholder)
            else slot.attribute.name)
        if self.config.verbose:
            self.outLine('%s %s %s %s %s' % (
                    slot.object.name,
                    self.kwd('.'),
                    attribute_name,
                    self.kwd('='),
                    str(slot.value)),
                indent=0)
        else:
            self.outLine('%s %s %s' % (
                    attribute_name,
                    self.kwd('is'),
                    str(slot.value)),
                indent=1)
        return self.output

    def doLink(self, l):
        association_name=(
            str(l.association)
                if isinstance(l.association, Placeholder)
            else l.association.name)
        self.outLine('%s %s %s' % (
                     l.roles[0].name,
                     association_name,
                     l.roles[1].name))
        return self.output

        # FIXME:1 add object links


METAMODEL.registerModelPrinter(ObjectModelPrinter)
METAMODEL.registerSourcePrinter(ModelSourcePrinter)
