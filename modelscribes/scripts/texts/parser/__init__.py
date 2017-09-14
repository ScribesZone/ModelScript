# coding=utf-8
from __future__ import unicode_literals, print_function, absolute_import, division
from typing import Text, List, Optional, Union, Tuple
import os
import re

DEBUG=3

from modelscribes.metamodels.texts import (
    TextBlock,
    Line,
    Token,
    Reference,
)
from modelscribes.scripts.texts.parser.segments import (
    segmentsAndErrors,
    Segment,
    StringSegment,
    ReferenceSegment,
)



class TextSourceFragment(object):
    def __init__(self, string, startLineNo=None):
        #type: (Text, Optional[int]) -> None

        # if not os.path.isfile(textFileName):
        #     raise Exception('File "%s" not found' % textFileName)
        # self.fileName = textFileName
        # noinspection PyTypeChecker
        self.startLineNo=startLineNo
        self.sourceLines = (
            line.rstrip()
            for line in string.split('\n'))
        # self.directory = os.path.dirname(textFileName)
        self.isValid = None
        self.errors = []
        self.lines = None
        self.ignoredLines = []
        self.textBlock = TextBlock(lineNo=startLineNo)
        self._parse()
        self.isValid=True # Todo, check errors, etc.

    def _parse(self):

        for (line_index, line) in enumerate(self.sourceLines):
            original_line = line
            line_no = line_index +(
                1 if self.startLineNo is None else self.startLineNo)
            (segments,errors)=segmentsAndErrors(line)
            text_line=Line(
                self.textBlock,
                lineNo=line_no
            )
            for segment in segments:
                if isinstance(segment,ReferenceSegment):
                    x=Reference(
                        line=text_line,
                        pos=segment.pos,
                        string=segment.string,
                        entry=None,  # not resolved yet
                    )
                else:
                    x=Token(
                        line=text_line,
                        pos=segment.pos,
                        string=segment.string,
                    )
                text_line.tokens.append(x)

            self.textBlock.lines.append(text_line)

    def printStatus(self):
        """
        Print the status of the file:

        * the list of errors if the file is invalid,
        * a short summary of entities (classes, attributes, etc.) otherwise
        """

        if self.isValid:
            print(self.textBlock)
        else:
            print('%s error(s) in the text model'  % len(self.errors))
            for e in self.errors:
                print(e)