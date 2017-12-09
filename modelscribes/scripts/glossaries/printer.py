# coding=utf-8
from __future__ import unicode_literals, print_function, absolute_import, division
from typing import Optional

from modelscribes.scripts.base.printers import (
    ModelPrinter,
    ModelSourcePrinter,
    ModelPrinterConfig,
)
from modelscribes.scripts.textblocks.printer import (
    TextBlockModelPrinter
)
from modelscribes.metamodels.glossaries import (
    GlossaryModel,
    METAMODEL
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

        for domain in glossary.domainNamed.values():
            self.doDomain(domain)
        return self.output

    def doDomain(self, domain):
        self.outLine(
            '%s %s' % (
                self.kwd('domain'),
                domain.name
            ),
            lineNo=domain.lineNo,
            linesBefore=1)
        for entry in domain.entryNamed.values():
            self.doEntry(entry)
        return self.output

    def doEntry(self, entry):
        self.outLine(
            '    %s:' % (
                ' '.join([entry.mainTerm] + entry.alternativeTerms)),
            lineNo=entry.lineNo,
            linesBefore=1
        )
        self.doDescription(entry.description)

    def doDescription(self, textBlock):
        block_text=TextBlockModelPrinter(
            theModel=textBlock,
            config=self.config).doModelContent()
        self.out(block_text)
        return self.output


METAMODEL.registerModelPrinter(GlossaryModelPrinter)
METAMODEL.registerSourcePrinter(ModelSourcePrinter)
