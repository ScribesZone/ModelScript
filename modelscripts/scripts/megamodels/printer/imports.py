# coding=utf-8
from typing import Optional, Text

from modelscripts.base.printers import (
    AbstractPrinter,
    AbstractPrinterConfig)
from modelscripts.megamodels.dependencies.sources import (
    ImportBox,
    SourceImport)


class ImportBoxPrinter(AbstractPrinter):

    def __init__(self, importBox, config=None):
        #type: (ImportBox, Optional[AbstractPrinterConfig]) -> None
        super(ImportBoxPrinter, self).__init__(
            config=config)
        self.importBox=importBox


    # def getIssueBox(self):
    #     return IssueBox()  #TODO:- is that enough ?

    def do(self):
        # super(ImportBoxPrinter, self).do()
        self.doImportBox(self.importBox)
        return self.output

    def doImportBox(self, importBox):
        self.doModelDefinition(importBox)
        for import_ in importBox.imports:
            self.doSourceImport(import_)
        return self.output


    def doModelDefinition(self, importBox):
        model_kinds=[self.kwd(mk) for mk in importBox.modelKinds]
        words=(
            model_kinds,
            self.kwd(importBox.modelSource.metamodel.label),
            self.kwd('model'),
            importBox.modelName)
        self.outLine(
            ' '.join([w for w in words if w]),
            lineNo=None)
        return self.output


    def doSourceImport(self, import_):
        #type:(SourceImport) -> Text
        try:
            s=('%s %s %s %s %s' % (
                self.kwd('import'),
                self.kwd(import_.importStmt.metamodel.label),
                self.kwd('model'),
                self.kwd('from'),
                "'%s'" %
                    import_.importStmt.literalTargetFileName
            ))
        except Exception as e:
            s='**Error** in doSourceImport'
            print(e)
        else:
            print(s)
        self.outLine(
            s,
            lineNo=import_.importStmt.lineNo
        )
        return self.output
