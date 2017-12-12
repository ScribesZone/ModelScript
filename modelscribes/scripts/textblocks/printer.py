# coding=utf-8
from __future__ import unicode_literals, print_function, absolute_import, division
from typing import Optional

from modelscribes.base.printers import (
    AbstractPrinter,
    AbstractPrinterConfig,
    Styles
)

from modelscribes.metamodels.textblocks import (
    TextBlock,
    BrokenReference,
    Occurrence
)

__all__=(
    'TextBlockPrinter'
)

class TextBlockPrinter(AbstractPrinter):

    def __init__(self,
                 textBlock,
                 config=None):
        #type: (TextBlock, Optional[AbstractPrinterConfig]) -> None
        super(TextBlockPrinter, self).__init__(
            config=config
        )
        self.textBlock=textBlock

    def do(self):
        if len(self.textBlock.lines)>=1:
            self.doTextBlock(self.textBlock)
        return self.output

    def doTextBlock(self, textBlock):
        for line in textBlock.lines:
            self.doLine(line)
        return self.output

    def doLine(self, line):
        _= '    %s' % (
            Styles.comment.do('|', self.config.styled))
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
                x=Styles.comment.do(
                    token.string,
                    styled=self.config.styled)
            _+=x
        self.outLine(_,lineNo=line.lineNo)
        return self.output