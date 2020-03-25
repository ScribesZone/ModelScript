# coding=utf-8


from typing import Optional

from modelscript.base.modelprinters import (
    ModelPrinter,
    ModelSourcePrinter,
    ModelPrinterConfig,
)
from modelscript.metamodels.glossaries import (
    GlossaryModel,
    METAMODEL
)
from modelscript.scripts.textblocks.printer import (
    TextBlockPrinter
)

__all__=(
    'GlossaryModelPrinter'
)

class GlossaryModelPrinter(ModelPrinter):

    def __init__(self,
                 theModel,
                 config=None):
        #type: (GlossaryModel, Optional[ModelPrinterConfig]) -> None
        super(GlossaryModelPrinter, self).__init__(
            theModel=theModel,
            config=config
        )
        self.theModel=theModel

    def doModelContent(self):
        super(GlossaryModelPrinter, self).doModelContent()
        self.doGlossaryModel(self.theModel)
        return self.output

    def doGlossaryModel(self, glossary):
        self.doModelTextBlock(glossary.description)
        for package in list(glossary.packageNamed.values()):
            self.doPackage(package)
        return self.output

    def doPackage(self, package):
        self.outLine(
            '%s %s' % (
                self.kwd('package'),
                package.name
            ),
            lineNo=package.lineNo,
            linesBefore=1)
        self.doModelTextBlock(package.description)
        for entry in list(package.entryNamed.values()):
            self.doEntry(entry)
        return self.output

    def doEntry(self, entry):
        self.outLine(
            '%s' % entry.term,
            lineNo=entry.lineNo,
            linesBefore=1
        )
        #TODO:3 ? ToCHeck: "add detailled information from entries"
        self.doModelTextBlock(entry.description)

        if len(entry.synonyms)>0:
            self.outLine(self.kwd('synonyms'))
            for synonym in entry.synonyms:
                self.outLine(synonym)

        if len(entry.inflections)>0:
            self.outLine(self.kwd('inflections'))
            for inflection in entry.inflections:
                self.outLine(inflection)

        if entry.label is not None:
            self.outLine(
                '%s: "%s"' % (self.kwd('label'), entry.label))

        if len(entry.translations)>0:
            self.outLine(self.kwd('translations'))
            for (language, label) in list(entry.translations.items()):
                self.outLine(
                    '%s: "%s"' % (language, label))
        return self.output

    def doDescription(self, textBlock):
        block_text=TextBlockPrinter(
            textBlock=textBlock,
            config=self.config).do()
        self.out(block_text)
        return self.output


METAMODEL.registerModelPrinter(GlossaryModelPrinter)
METAMODEL.registerSourcePrinter(ModelSourcePrinter)
