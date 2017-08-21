# coding=utf-8
from __future__ import unicode_literals, print_function, absolute_import, division
from typing import Text, Union, Optional, Dict, List

from modelscripts.source.printer import (
    AbstractPrinter
)

from modelscripts.metamodels.objects import (
    ObjectModel,
    Object,
    Link,
    LinkObject,
)



class Printer(AbstractPrinter):

    def __init__(self, objectModel, displayLineNos=True):
        #type: (ObjectModel, bool) -> None
        super(Printer,self).__init__(
            displayLineNos=displayLineNos)
        self.objectModel=objectModel

    def do(self):
        super(Printer,self).do()
        self._ObjectModel(self.objectModel)
        return self.output

    def _ObjectModel(self, objectModel):
        self.outLine(
            'object model',
            lineNo=None, #objectModel.lineNo)  # TODO: change parser
            linesAfter=1  )