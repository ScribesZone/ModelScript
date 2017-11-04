# coding=utf-8
from __future__ import unicode_literals, print_function, absolute_import, division

from modelscribes.base.printers import (
    AbstractPrinter
)
from modelscribes.megamodels.dependencies.sources import (
    ImportBox
)

__all__=(
    'ImportBoxPrinter'
)

class ImportBoxPrinter(AbstractPrinter):

    def __init__(self, importBox, displayLineNos=True):
        #type: (ImportBox, bool) -> None
        super(ImportBoxPrinter, self).__init__(
            displayLineNos=displayLineNos)
        self.importBox=importBox

    def do(self):
        super(ImportBoxPrinter, self).do()
        self._importBox(self.importBox)
        return self.output

    def _importBox(self, importBox):
        self._modelDefinition(importBox)
        for import_ in importBox.imports:
            self._sourceImport(import_)


    def _modelDefinition(self, importBox):
        words=(
                importBox.modelKind,
                importBox.modelSource.metamodel.label,
                'model',
                importBox.modelName)
        self.outLine(
            ' '.join([ w for w in words if w ]),
            lineNo=None)


    def _sourceImport(self, import_):
        self.outLine(
            str(import_),
            lineNo=import_.importStmt.lineNo
        )

