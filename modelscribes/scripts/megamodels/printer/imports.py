# coding=utf-8
from typing import Optional, Text

from modelscribes.base.printers import (
    AbstractPrinter,
    AbstractPrinterConfig
)
from modelscribes.megamodels.sources import (
    ImportBox,
    SourceImport
)


class ImportBoxPrinter(AbstractPrinter):

    def __init__(self, importBox, config=None):
        #type: (ImportBox, Optional[AbstractPrinterConfig]) -> None
        super(ImportBoxPrinter, self).__init__(
            config=config)
        self.importBox=importBox


    # def getIssueBox(self):
    #     return IssueBox()  #TODO: is that enough ?

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
        model_kind=('' if not importBox.modelKind
                    else self.kwd(importBox.modelKind))
        words=(
            model_kind,
            self.kwd(importBox.modelSource.metamodel.label),
            self.kwd('model'),
            importBox.modelName)
        self.outLine(
            ' '.join([w for w in words if w]),
            lineNo=None)
        return self.output


    def doSourceImport(self, import_):
        #type: (SourceImport) -> Text
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
            print(e)
        else:
            print(s)
        self.outLine(
            s,
            lineNo=import_.importStmt.lineNo
        )
        return self.output

