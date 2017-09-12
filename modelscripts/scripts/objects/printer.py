# coding=utf-8
from __future__ import unicode_literals, print_function, absolute_import, division

from modelscripts.base.printers import (
    AbstractPrinter
)

from modelscripts.metamodels.objects import (
    ObjectModel,
    Object,
    Link,
    LinkObject,
    metamodel
)



class ObjectModelPrinter(AbstractPrinter):

    def __init__(self, objectModel, displayLineNos=True):
        #type: (ObjectModel, bool) -> None
        super(ObjectModelPrinter, self).__init__(
            displayLineNos=displayLineNos)
        self.objectModel=objectModel

    def do(self):
        super(ObjectModelPrinter, self).do()
        self._ObjectModel(self.objectModel)
        return self.output

    def _ObjectModel(self, objectModel):
        self.outLine(
            'object model',
            lineNo=None, #objectModel.lineNo)  # TODO: change parser
            linesAfter=1  )

#TODO: add ObjectModelSourcePrinter

metamodel.registerModelPrinter(ObjectModelPrinter)
#TODO: register ObjectModelSourcePrinter
