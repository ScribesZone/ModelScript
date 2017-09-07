# coding=utf-8
from __future__ import print_function
from typing import (
    Union, Dict, Text, Optional, List, Any,
)

from modelscripts.base.sources import SourceElement

class TextBlock(SourceElement):

    def __init__(self,
                 container=None,
                 lineNo=None,
                 lines=()):
        super(TextBlock, self).__init__(
            name=None,
            lineNo=lineNo
        )
        self.container=container
        # type: Any
        self.lines = list(lines)
        # type: List[Line]


class Line(SourceElement):

    def __init__(self, textBlock, lineNo=None, tokens=()):
        super(Line, self).__init__(
            name=None,
            lineNo=lineNo
        )

        self.textBlock = textBlock
        #type: TextBlock

        self.tokens = list(tokens)
        #type: List[Token]


class Token(object):

    def __init__(self, line, pos, string):
        #type: (Line, int, Text) -> None

        self.string=string
        #type: Text

        self.line=line
        #type: Line

        self.pos=pos
        #type: int


class Reference(Token):

    def __init__(self, line, pos, string, entry=None):
        #type: (Line, int, Text, Optional['Term']) -> None
        super(Reference, self).__init__(line, pos, string)

        self.entry=entry
        #type: Optional['Entry']

    def resolve(self, glossary):
        #type: ('Glossary')->Optional['Entry']
        """
        Return None if the term does not correspond to the entry.
        If it corresponds to an entry, then add it to its list
        of references.
        """

        if self.entry is not None:
            return self.entry
        else:
            entryOrNone=glossary.findEntry(self.string)
            self.entry=entryOrNone
            if self.entry is not None:
                self.entry.references.append(self)
            return entryOrNone