# # coding=utf-8

from typing import Any, Optional

from modelscripts.base.exceptions import (
    UnexpectedCase)
from modelscripts.metamodels.textblocks import (
    TextBlock,
    TextLine,
    PlainText,
    TextReference)
#  import modelscripts.metamodels.textblocks in script due to cycle
from modelscripts.metamodels.glossaries import GlossaryModel

def astTextBlockToTextBlock(container, astTextBlock, glossary=None):
    #type: ('SourceModelElement', Optional['grammar.TextBlock'], Optional[GlossaryModel]) -> Optional[TextBlock]
    if astTextBlock is None:
        return None
    else:

        text_block=TextBlock(
            container=container,
            astTextBlock=astTextBlock)
        for ast_text_line in astTextBlock.textLines:
            text_line=TextLine(text_block, ast_text_line)
            for ast_text_token in ast_text_line.textTokens:
                type_ =ast_text_token.__class__.__name__
                if type_=='PlainText':
                    PlainText(
                        textLine=text_line,
                        text=ast_text_token.text,
                        astPlainText=ast_text_token)
                elif type_=='TextReference':
                    TextReference(
                        textLine=text_line,
                        text=ast_text_token.text,
                        astTextReference=ast_text_token)
                else:
                    raise UnexpectedCase( #raise:OK
                        'Type %s not supported' % type_)

        #TODO:2 add a reference to this text block into the model
        # here container.model is the model we need
        # add something like:
        #      container.model.textBlocks.append(text_block)
        return text_block

GRAMMAR='''
'''