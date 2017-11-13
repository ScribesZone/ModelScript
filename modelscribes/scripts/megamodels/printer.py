# coding=utf-8
from __future__ import unicode_literals, print_function, absolute_import, division

from modelscribes.base.printers import (
    AbstractPrinter
)
from modelscribes.megamodels.dependencies.sources import (
    ImportBox
)
from modelscribes.megamodels.megamodels import (
    Megamodel
)

__all__=(
    'ImportBoxPrinter',
    'MegamodelPrinter'
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


class MegamodelPrinter(AbstractPrinter):
    def __init__(self):
        #type: () -> ()
        super(MegamodelPrinter, self).__init__(
            displayLineNos=None
        )

    def do(self):
        super(MegamodelPrinter, self).do()
        self._megamodel()
        return self.output

    def _megamodel(self):
        self.outLine('%'*80)
        self.metamodelRegistery()
        self.modelRegistery()
        self.sourceRegistery()
        self.outLine('%'*80)
        self.outLine('')


    def metamodelRegistery(self):
        self.outLine('-'*30+' metamodels '+'-'*30)
        self.outLine(
            ', '.join([mm.id for mm in Megamodel.metamodels()] ))
        for mmd in Megamodel.metamodelDependencies():
            self.outLine('%s -> %s' % (
                mmd.source.id,
                mmd.target.id))

    def modelRegistery(self):
        self.outLine('-'*32+' models '+'-'*32)
        self.outLine(
            ', '.join([
                    m.label for m in Megamodel.models()] ))
        for md in Megamodel.modelDependencies():
            self.outLine('%s -> %s' % (
                md.source.label,
                md.target.label))

    def sourceRegistery(self):
        self.outLine('-' * 32 + ' sources ' + '-' * 31)
        self.outLine(
            ', '.join([
                s.label for s in Megamodel.sources()]))
        for sd in Megamodel.sourceDependencies():
            self.outLine('%s -> %s' % (
                sd.source.label,
                sd.target.label))


