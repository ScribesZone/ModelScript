# coding=utf-8
"""
Metamodel a texts made of lines with possibily some references to
a entries in a glossary.

The structure of the meta elemens

    TextBlock
        <>--* Line
                <>--* Token
                        <|-- Reference
                                <|-- BrokenReference
                                <|-- Occurrence


"""
from __future__ import print_function
from typing import (
    Text, Optional, List, Any, Union
)
from abc import ABCMeta
from modelscripts.base.metrics import Metrics
from modelscripts.base.sources import SourceElement
from modelscripts.metamodels.glossaries import GlossaryModel
from modelscripts.scripts.textblocks.parser.segments import (
    segmentsAndErrors,

    ReferenceSegment,
)

__all__ = (
    'TextBlock',
    'Line',
    'Token',
    'PlainToken',
    'Reference',
    'BrokenReference',
    'Occurrence'
)


class TextBlock(SourceElement):
    _empty=None

    @classmethod
    def empty(cls):
        """
        Singleton empty text block to make sure
        that composite model will have a textblock
        instead of none.
        """
        if cls._empty is None:
            cls._empty=TextBlock()
        return cls._empty

    def __init__(self,
                 container=None,
                 glossary=None,
                 lines=()):
        super(TextBlock, self).__init__()

        self.container=container
        # type: Optional[Any]
        # Could be typically a ModelElement

        self.lines = list(lines)
        # type: List[Line]

        self.glossary=glossary
        # type: Optional[GlossaryModel]

        self.isResolved=False

    # def resolve(self):
    #     for line in self.lines:
    #         for token in line.tokens:
    #             if isinstance(token, Reference):
    #                 reference = token
    #
    #
    #             reference.resolve(self.glossary)

    # def metamodel(self):
    #     #type: () -> Metamodel
    #     raise NotImplementedError()

    def resolve(self):
        if self.glossary is not None:
            for l in self.lines:
                l.resolve()
            self.isResolved=True

    @property
    def metrics(self):
        #type: () -> Metrics
        ms=super(TextBlock, self).metrics
        ms.addList((
            ('line', len(self.lines)),
            ('token', sum(len(l.token) for l in self.lines) ),
            ('reference',
                sum(len(l.references) for l in self.lines)),
            ('brokenReference',
                sum(len(l.brokenReferences) for l in self.lines)),
            ('occurrences',
                sum(len(l.occurrences) for l in self.lines)),
        ))
        return ms

    def addNewLine(self, stringLine, lineNo=None):
        line=Line(
            textBlock=self,
            lineNo=lineNo,
            stringLine=stringLine
        )
        self.lines.append(line)





class Line(SourceElement):
    """
    Represents either a line to be parsed or a parsed line.
    In the first case there is only one token containing
    the whole line. In the second case the line contains
    various tokens, these tokens are either PlainToken
    or UnresolvedToken.
    """

    def __init__(self,
                 textBlock,
                 lineNo=None,
                 tokens=None,
                 stringLine=None):
        #type: (TextBlock, Optional[int], Optional[List[Token]], Optional[Text]) -> None
        """
        Create a Line either with a list of tokens or with a
        stringLine. Parameters tokens and stringLine are
        exclusive if none of them is provided then the line
        will have no token. If stringLine is given then
        the string is parsed and token are converted from
        that.
        """

        def _stringLineToLineTokens(stringLine, line):
            #type: (Text, Line) -> None
            """
            Segment the string line and create tokens in the
            given line.
            """
            (segments, errors) = segmentsAndErrors(stringLine)
            for segment in segments:
                if isinstance(segment, ReferenceSegment):
                    x = UnresolvedReference(
                        line=line,
                        pos=segment.pos,
                        string=segment.string
                    )
                else:
                    x = PlainToken(
                        line=line,
                        pos=segment.pos,
                        string=segment.string,
                    )
                line.tokens.append(x)

        assert tokens is None or stringLine is None
        super(Line, self).__init__(
            name=None,
            lineNo=lineNo
        )
        self.isResolved=False

        self.textBlock = textBlock
        #type: TextBlock

        self.tokens=[]
        # type: List[Token]
        # Value will be set below

        if tokens is not None:
            self.tokens=list(tokens)
        elif stringLine is not None:
            _stringLineToLineTokens(stringLine, self)
        else:
            pass

    def resolve(self):
        if self.textBlock.glossary is not None:
            for (i, token) in enumerate(self.tokens):
                if isinstance(token, UnresolvedReference):
                    # replace the UnresolvedReference by a new
                    # token, either BrokenReference or Occurrence
                    self.tokens[i]=token.resolve()


    def _selectByType(self, t):
        return [
            x for x in self.tokens
            if isinstance(x, t)
        ]

    @property
    def references(self):
        #type: () -> List[Reference]
        # noinspection PyTypeChecker
        return self._selectByType(Reference)

    # @property
    # def unresolvedReferences(self):
    #     #type: () -> List[UnresolvedReference]
    #     return self._selectByType(UnresolvedReference)

    @property
    def brokenReferences(self):
        #type: () -> List[BrokenReference]
        # noinspection PyTypeChecker
        return self._selectByType(BrokenReference)

    @property
    def occurrences(self):
        #type: () -> List[Occurrence]
        # noinspection PyTypeChecker
        return self._selectByType(Occurrence)


class Token(object):
    __metaclass__ = ABCMeta

    def __init__(self, line, pos, string):
        #type: (Line, int, Text) -> None

        self.string=string
        #type: Text

        self.line=line
        #type: Line

        self.pos=pos
        #type: int


class PlainToken(Token):

    def __init__(self, line, pos, string):
        #type: (Line, int, Text) -> None
        super(PlainToken, self).__init__(
            line=line, pos=pos, string=string)


class Reference(Token):
    __metaclass__ = ABCMeta

    def __init__(self, line, pos, string):
        #type: (Line, int, Text) -> None
        super(Reference, self).__init__(line, pos, string)

    @property
    def isBroken(self):
        return False

    # def resolve(self, glossary):
    #     #type: ('Glossary')->Optional['Entry']
    #     """
    #     Return None if the term does not correspond to the entry.
    #     If it corresponds to an entry, then add it to its list
    #     of references.
    #     """
    #
    #     if self.entry is not None:
    #         return self.entry
    #     else:
    #         entryOrNone=glossary.findEntry(self.string)
    #         self.entry=entryOrNone
    #         if self.entry is not None:
    #             self.entry.references.append(self)
    #         return entryOrNone


class UnresolvedReference(Reference):
    def __init__(self, line, pos, string):
        #type: (Line, int, Text) -> None
        super(UnresolvedReference, self).__init__(
            line, pos, string)

    def resolve(self):
        #type: () -> Union[BrokenReference, Occurrence]
        """
        Resolve the token with the glossary defined
        in the text block. Return a new token:
        - a BrokenReference if no entry is found
        - an Occurrence if an entry is not found
        If no glossary was provided then the token
        is left untouched.
        """
        g = self.line.textBlock.glossary
        if g is not None:
            entry_or_none=g.findEntry(self.string)
            if entry_or_none is None:
                new_entry=BrokenReference(
                    line=self.line,
                    pos=self.pos,
                    string=self.string)
            else:
                new_entry=Occurrence(
                    line=self.line,
                    pos=self.pos,
                    string=self.string,
                    entry=entry_or_none)
        else:
            new_entry=self
        return new_entry


class BrokenReference(Reference):

    def __init__(self, line, pos, string):
        #type: (Line, int, Text) -> None
        super(BrokenReference, self).__init__(line, pos, string)

    @property
    def isBroken(self):
        return True


class Occurrence(Reference):

    def __init__(self, line, pos, string, entry):
        #type: (Line, int, Text, Optional['Term']) -> None
        super(Occurrence, self).__init__(line, pos, string)

        self.entry=entry
        # Add the occurrence to the reference to the entry
        self.entry.occurrences.append(self)


    @property
    def isBroken(self):
        return False


# METAMODEL = Metamodel(
#     id='tx',
#     label='text',
#     extension='.txs',
#     modelClass=TextBlock,
#     modelKinds=()
# )
# MetamodelDependency(
#     sourceId='tx',
#     targetId='gl',
#     optional=True,
#     multiple=True,
# )