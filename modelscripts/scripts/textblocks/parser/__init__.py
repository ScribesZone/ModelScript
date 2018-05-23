# # coding=utf-8

from typing import Any, Optional

from modelscripts.metamodels.textblocks import (
    TextBlock,
    TextLine,
    PlainText,
    TextReference
)
#  import modelscripts.metamodels.textblocks in script due to cycle
from modelscripts.metamodels.glossaries import GlossaryModel

def astTextBlockToTextBlock(container, astTextBlock, glossary=None):
    #type: ('SourceModelElement', Optional['grammar.TextBlock'], Optional[GlossaryModel]) -> Optional[TextBlock]
    if astTextBlock is None:
        return None
    else:

        text_block=TextBlock(
            container=container,
            astTextBlock=astTextBlock,
            glossary=None)
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
                    raise NotImplementedError(
                        'Type %s not supported' % type_)

            # line_string=BracketedScript.extractDocLineText(ast_doc_line.text)
            # text_line=TextLine(
            #     text_block,
            #     astNode=ast_doc_line,
            #     stringLine=line_string)
        return text_block








# """
# Parser for text blocks.
#
# The class TextBlockSource contains the raw block of text, and
# after parsing it contains the model, a TextBlock.
# """
# from __future__ import unicode_literals, print_function, absolute_import, division
# from typing import Text, List, Optional, Any, Tuple
# import os
# import re
#
# DEBUG=3
#
# from modelscripts.metamodels.textblocks import (
#     TextBlock,
#     TextLine,
#     BrokenReference,
#     Occurrence,
#     PlainToken
# )
# from modelscripts.scripts.textblocks.parser.segments import (
#     segmentsAndErrors,
#     Segment,
#     StringSegment,
#     ReferenceSegment,
# )
#  TODO:
#
#
# class TextBlockSource(object):
#     """
#     Parser of a text block with potentially some references.
#     """
#     def __init__(self):
#         self.linePairs = []
#         #type: List[Tuple[Optional[int, Text]]
#         """
#         Text line (strings)
#         """
#
#         self.model = None
#         #type: Optional[TextBlock]
#         """
#         Text Block model.
#         Will be set by parseAndResolve.
#         """
#         # FIXME: check which kind of error should we put here
#         self.ignoredLines = []
#         self.errors = []
#         self.isValid=True
#
#     def addTextLine(self, textLine, lineNo=None):
#         #type: (Text, Optional[int]) -> None
#         self.linePairs.append((lineNo,textLine))
#
#     def parseToFillModel(self, container, glossary):
#         #type: (Any) -> None
#         """
#         Set the model  self.model
#         """
#
#         # def resolve(string, glossary):
#         #     entryOrNone = glossary.findEntry(string)
#         #     # self.entry=entryOrNone
#         #     # if self.entry is not None:
#         #     #     self.entry.references.append(self)
#         #     return entryOrNone
#
#         self.model=TextBlock()
#         self.model.glossary=glossary
#         self.model.container=container
#
#         for (line_no, line) in self.linePairs:
#             (segments, errors)=segmentsAndErrors(line)
#             line_model=TextLine(
#                 self.model,
#                 lineNo=line_no
#             )
#             #TODO: deal
#             for segment in segments:
#                 if isinstance(segment, ReferenceSegment):
#                     entry=glossary.findEntry(segment.string)
#                     if entry is None:
#                         x=BrokenReference(
#                             line=line_model,
#                             pos=segment.pos,
#                             string=segment.string
#                         )
#                     else:
#                         x=Occurrence(
#                             line=line_model,
#                             pos=segment.pos,
#                             string=segment.string,
#                             entry=entry,
#                         )
#                 else:
#                     x=PlainToken(
#                         line=line_model,
#                         pos=segment.pos,
#                         string=segment.string,
#                     )
#                 line_model.tokens.append(x)
#
#             self.model.lines.append(line_model)
#
#
