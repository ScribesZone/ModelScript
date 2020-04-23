# coding=utf-8

from typing import Optional, Text

from modelscript.base.printers import (
    AbstractPrinter,
    AbstractPrinterConfig)
from modelscript.megamodels.dependencies.sources import (
    ImportBox,
    SourceImport)
from modelscript.scripts.textblocks.printer import (
    TextBlockPrinter)

class ImportBoxPrinter(AbstractPrinter):

    def __init__(self,
                 importBox: ImportBox,
                 config: Optional[AbstractPrinterConfig] = None)\
            -> None:
        super(ImportBoxPrinter, self).__init__(
            config=config)
        self.importBox = importBox


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
        model_kinds = [self.kwd(mk) for mk in importBox.modelKinds]
        words = (
            model_kinds,
            self.kwd(importBox.modelSource.metamodel.label),
            self.kwd('model'),
            importBox.modelName)
        self.outLine(
            ' '.join([w for w in words if w]),
            lineNo=None)
        model_doc = importBox.modelSource.model.description
        if model_doc is not None:
            block_text = TextBlockPrinter(
                textBlock=model_doc,
                indent=1,
                config=self.config).do()
            self.out(block_text)
        return self.output


    def doSourceImport(self, import_: SourceImport) -> str:
        try:
            s = ('%s %s %s %s %s' % (
                self.kwd('import'),
                self.kwd(import_.importStmt.metamodel.label),
                self.kwd('model'),
                self.kwd('from'),
                "'%s'" %
                    import_.importStmt.literalTargetFileName
            ))
        except Exception as e:
            s = '**Error** in doSourceImport'
            print(e)
        else:
            print(s)
        self.outLine(
            s
        )
        return self.output
