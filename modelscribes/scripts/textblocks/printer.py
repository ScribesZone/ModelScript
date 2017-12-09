# coding=utf-8
from __future__ import unicode_literals, print_function, absolute_import, division
from typing import Optional

from modelscribes.scripts.base.printers import (
    ModelPrinter,
    ModelPrinterConfig,
    ModelSourcePrinter,
    Styles
)
from modelscribes.metamodels.textblocks import (
    METAMODEL
)
from modelscribes.metamodels.textblocks import (
    TextBlockModel,
    BrokenReference,
    Occurrence
)

__all__=(
    'TextBlockModelPrinter'
)

class TextBlockModelPrinter(ModelPrinter):

    def __init__(self,
                 theModel,
                 config=None):
        #type: (TextBlockModel, Optional[ModelPrinterConfig]) -> None
        super(TextBlockModelPrinter, self).__init__(
            theModel=theModel,
            config=config
        )

    def doModelContent(self):
        super(TextBlockModelPrinter, self).doModelContent()
        self.doTextBlockModel(self.theModel)
        return self.output

    def doTextBlockModel(self, textBlock):
        for line in textBlock.lines:
            self.doLine(line)
        return self.output

    def doLine(self, line):
        _= '        | '
        for token in line.tokens:
            if isinstance(token, Occurrence):
                x= Styles.bold.do(
                    '`%s`!' % token.string,
                    styled=self.config.styled)
            elif isinstance(token, BrokenReference):
                x= Styles.ko.do(
                    '`%s`?' % token.string,
                    styled=self.config.styled)
            else:
                x=token . string
            _+=x
        self.outLine(_,lineNo=line.lineNo)
        return self.output


METAMODEL.registerModelPrinter(TextBlockModelPrinter)
METAMODEL.registerSourcePrinter(ModelSourcePrinter)