# coding=utf-8

from typing import Optional

from modelscript.base.printers import (
    AbstractPrinter,
    AbstractPrinterConfig,
    Styles
)

from modelscript.base.exceptions import (
    UnexpectedCase)

__all__=(
    'TextBlockPrinter'
)

TextBlock = 'TextBlock'

class TextBlockPrinter(AbstractPrinter):

    def __init__(self,
                 textBlock: TextBlock,
                 indent: int = 0,
                 config: Optional[AbstractPrinterConfig] = None):
        super(TextBlockPrinter, self).__init__(
            config=config
        )
        self.textBlock = textBlock
        self.indent = indent

    def do(self):
        if len(self.textBlock.textLines) >= 1:
            self.doTextBlock(self.textBlock)
        return self.output

    def doTextBlock(self, textBlock):
        for line in textBlock.textLines:
            # self.out('XX')
            self.doLine(line)
            # self.out('YY')

        return self.output

    def doLine(self, line):
        _ = '%s' % (
            Styles.comment.do('|', self.config.styled))
        self.out(_, indent=self.indent)
        for token in line.textTokens:
            self.doTextToken(token)
        self.endLine()
        return self.output

    def doTextToken(self, token):
        from modelscript.metamodels.textblocks import (
            TextReference, PlainText
        )
        if isinstance(token, TextReference):
            r = token
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
            raise UnexpectedCase(  # raise:OK
                'Printing %s is not implemented'
                % type(token))
        self.out(x)
        return self.output
