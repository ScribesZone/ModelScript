# # coding=utf-8
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
#     Line,
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
#             line_model=Line(
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
