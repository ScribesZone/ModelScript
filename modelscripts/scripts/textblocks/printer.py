# coding=utf-8
from __future__ import unicode_literals, print_function, absolute_import, division
from typing import Optional

from modelscripts.base.printers import (
    AbstractPrinter,
    AbstractPrinterConfig,
    Styles
)

# from modelscripts.metamodels.textblocks import (
#     TextBlock,
#     PlainText,
#     TextReference
# )

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
        if len(self.textBlock.textLines)>=1:
            self.doTextBlock(self.textBlock)
        return self.output

    def doTextBlock(self, textBlock):
        for line in textBlock.textLines:
            self.doLine(line)
        return self.output

    def doLine(self, line):
        _= '    %s' % (
            Styles.comment.do('|', self.config.styled))
        for token in line.textTokens:
            self.doTextToken(token)
        self.outLine(_,lineNo=line.lineNo)
        return self.output

    def doTextToken(self, token):
        from modelscripts.metamodels.textblocks import (
            TextReference, PlainText
        )
        if isinstance(token, TextReference):
            r=token
            if r.isOccurrence:
                x = Styles.bold.do(
                    '`%s`!' % r.text,
                    styled=self.config.styled)
            elif r.isBroken:
                x = Styles.ko.do(
                    '`%s`?' % r.text,
                    styled=self.config.styled)
            else:
                x = Styles.comment.do(
                    '`%s`_' % r.text,
                    styled=self.config.styled)
        elif isinstance(token, PlainText):
            x = Styles.comment.do(
                token.text,
                styled=self.config.styled)
        else:
            raise NotImplementedError(
                'Printing %s is not implemented'
                % type(token))
        self.out(x)