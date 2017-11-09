# coding=utf-8
from __future__ import unicode_literals, print_function, absolute_import, division

from modelscribes.base.printers import (
    AbstractPrinter,
    SourcePrinter
)

from modelscribes.metamodels.objects import (
    ObjectModel,
    Object,
    Link,
    LinkObject,
    METAMODEL
)



class ObjectModelPrinter(AbstractPrinter):

    def __init__(self, theModel, displayLineNos=True):
        #type: (ObjectModel, bool) -> None
        super(ObjectModelPrinter, self).__init__(
            displayLineNos=displayLineNos)
        self.objectModel=theModel

    def do(self):
        super(ObjectModelPrinter, self).do()
        self._ObjectModel(self.objectModel)
        self._objects()
        self._links()
        return self.output

    def _ObjectModel(self, objectModel):
        self.outLine(
            'object model',
            lineNo=None, #objectModel.lineNo)  # TODO: change parser
            linesAfter=1  )

    def _objects(self):
        for o in self.objectModel.objects:
            self.outLine('    %s is a %s' % (
                         o.name,
                         o.classifier.name))

    def _links(self):
        for l in self.objectModel.links:
            self.outLine('    %s %s %s' % (
                         l.roles[0].name,
                         l.classifier.name,
                         l.roles[1].name))

    # FIXME:1 add object links

class ObjectSourcePrinter(SourcePrinter):
    def __init__(self,
                 theSource,
                 summary=False,
                 displayLineNos=True,
                 ):
        super(ObjectSourcePrinter, self).__init__(
            theSource=theSource,
            summary=False,
            displayLineNos=True)

    def do(self):
        self.output=''
        if self.theSource.model is not None:
            p=ObjectModelPrinter(
                theModel=self.theSource.model,
                displayLineNos=self.displayLineNos
            ).do()
            self.out(p)
        else:
            self._issues()
        return self.output

METAMODEL.registerSourcePrinter(ObjectSourcePrinter)
METAMODEL.registerModelPrinter(ObjectModelPrinter)
