# coding=utf-8
"""
Metamodel a texts made of textLines with possibily some references to
a entries in a glossary.

The structure of the meta elemens

    TextBlock
        <>--* TextLine
                <>--* TextToken
                        <|-- PlainText
                        <|-- Reference

"""
from __future__ import print_function
from typing import (
    Text, Optional, List, Any
)
from modelscripts.megamodels.elements import (
    SourceModelElement,
    ModelElement
)
from abc import ABCMeta, abstractmethod
from modelscripts.base.metrics import Metrics
from modelscripts.metamodels.glossaries import (
    GlossaryModel,
    Entry
)

__all__ = (
    'TextBlock',
    'TextLine',
    'TextToken',
    'PlainText',
    'TextReference',
)


class TextBlock(SourceModelElement):
    """ A text block embedded into a SourceModelElement """

    def __init__(self,
                 container,
                 glossary=None,
                 astTextBlock=None):
        #type: (SourceModelElement, Optional[GlossaryModel],Optional['grammar.TextBlock'] ) -> None
        print('RR'*20, container)
        print('RR'*20, type(container))
        print('RR'*20, container.model)
        super(TextBlock, self).__init__(
            model=container.model,
            astNode=astTextBlock)

        self.container=container
        # type: Optional[ModelElement]
        # Could be for instance a Usecase, Actor, but also
        # a model etc.
        if self.container is not None:
            print('NN'*20,type(container))
            assert isinstance(container, ModelElement)

        self.textLines=[]
        # type: List[TextLine]

        self.glossary=glossary
        # type: Optional[GlossaryModel]

        self.isResolved=False

    def resolve(self):
        if self.glossary is not None:
            for l in self.textLines:
                l.resolve()
            self.isResolved=True

    @property
    def metrics(self):
        #type: () -> Metrics
        ms=super(TextBlock, self).metrics
        ms.addList((
            ('line', len(self.textLines)),
            ('token', sum(len(l.token) for l in self.textLines)),
            ('reference',
                sum(len(l.references) for l in self.textLines)),
            ('brokenReference',
                sum(len(l.brokenReferences) for l in self.textLines)),
            ('occurrences',
                sum(len(l.occurrences) for l in self.textLines)),
        ))
        return ms

    def addTextLine(self, textLine):
        #type: (TextLine) -> None
        self.textLines.append(textLine)


# class TextBlock(SourceModelElement):
#     _empty=None
#
#     @classmethod
#     def empty(cls):
#         """
#         Singleton empty text block to make sure
#         that composite model will have a textblock
#         instead of none.
#         """
#         if cls._empty is None:
#             cls._empty=TextBlock()
#         return cls._empty
#
#     def __init__(self,
#                  container,
#                  glossary=None,
#                  astNode=None):
#         assert (container, 'model')
#         super(TextBlock, self).__init__(
#             model=container.model,
#             astNode=astNode)
#
#         self.container=container
#         # type: Optional[Any]
#         # Could be typically a ModelElement such as Usecase, Actor,
#         # Enumeration, etc.
#
#         self.lines=[]
#         # type: List[TextLine]
#
#         self.glossary=glossary
#         # type: Optional[GlossaryModel]
#
#         self.isResolved=False
#
#     # def resolve(self):
#     #     for line in self.lines:
#     #         for token in line.tokens:
#     #             if isinstance(token, Reference):
#     #                 reference = token
#     #
#     #
#     #             reference.resolve(self.glossary)
#
#     # def metamodel(self):
#     #     #type: () -> Metamodel
#     #     raise NotImplementedError()
#
#     def resolve(self):
#         if self.glossary is not None:
#             for l in self.lines:
#                 l.resolve()
#             self.isResolved=True
#
#     @property
#     def metrics(self):
#         #type: () -> Metrics
#         ms=super(TextBlock, self).metrics
#         ms.addList((
#             ('line', len(self.lines)),
#             ('token', sum(len(l.token) for l in self.lines) ),
#             ('reference',
#                 sum(len(l.references) for l in self.lines)),
#             ('brokenReference',
#                 sum(len(l.brokenReferences) for l in self.lines)),
#             ('occurrences',
#                 sum(len(l.occurrences) for l in self.lines)),
#         ))
#         return ms
#
#     # def addNewLine(self, stringLine, lineNo=None):
#     #     line=TextLine(
#     #         textBlock=self,
#     #         lineNo=lineNo,
#     #         stringLine=stringLine
#     #     )
#     #     self.lines.append(line)
#
#     def addTextLine(self, textLine):
#         #type: (TextLine) -> None
#         self.lines.append(textLine)


class TextLine(SourceModelElement):

    def __init__(self,
                 textBlock,
                 astTextLine=None
                 ):
        #type: (TextBlock, Optional['grammar.TextLine'] ) -> None

        super(TextLine, self).__init__(
            model=textBlock.model,
            name=None,
            astNode=astTextLine
        )
        self.isResolved=False

        self.textBlock = textBlock
        #type: TextBlock

        self.textTokens=[]
        # type: List[TextToken]
        # Value will be set below

        self.textBlock.addTextLine(self)

    def resolve(self):
        if self.textBlock.glossary is not None:
            for textToken in self.textTokens:
                textToken.resolve()
            self.isResolved=True

    def _selectByType(self, t):
        return [
            x for x in self.textTokens
            if isinstance(x, t)
        ]

    @property
    def plainTexts(self):
        #type: () -> List[TextReference]
        # noinspection PyTypeChecker
        return self._selectByType(PlainText)

    @property
    def textReferences(self):
        #type: () -> List[TextReference]
        # noinspection PyTypeChecker
        return self._selectByType(TextReference)

    @property
    def brokenReferences(self):
        #type: () -> List[TextReference]
        # noinspection PyTypeChecker
        return [
            r for r in self.textReferences
            if r.isBroken
        ]

    @property
    def occurrences(self):
        #type: () -> List[TextReference]
        # noinspection PyTypeChecker
        return [
            r for r in self.textReferences
            if r.isOccurrence
        ]

    def addTextToken(self, token):
        #type: (TextToken) -> None
        return self.textTokens.append(token)


# class TextLine(SourceElement):
#     """
#     Represents either a line to be parsed or a parsed line.
#     In the first case there is only one token containing
#     the whole line. In the second case the line contains
#     various tokens, these tokens are either PlainToken
#     or UnresolvedToken.
#     """
#
#     def __init__(self,
#                  textBlock,
#                  tokens=None,
#                  #stringLine=None,
#                  # lineNo=None, replaced by ASTNode,
#                  astNode=None  # in practice grammar.DocLine
#                  ):
#         #type: (TextBlock, Optional[List[Token]], Optional[Text], 'ASTNode' ) -> None
#         """
#         Create a TextLine from two alteratives:
#         - a list of tokens,
#         - a plain string.
#         These alternatives are exclusives. If none of these 2 parameters
#         are provide the line will have no token.
#         If the tokens are provided they are left untoouched.
#         If stringLine is given then the string is parsed and token are
#         converted from that.
#         """
#
#         def _add_string_to_tokens(string_to_parse, text_line):
#             #type: (Text, TextLine) -> None
#             """
#             Segment the string line and create tokens in the
#             given line.
#             """
#             (segments, errors) = segmentsAndErrors(string_to_parse)
#             for segment in segments:
#                 if isinstance(segment, ReferenceSegment):
#                     x = UnresolvedReference(
#                         line=text_line,
#                         pos=segment.pos,
#                         string=segment.string
#                     )
#                 else:
#                     x = PlainToken(
#                         line=text_line,
#                         pos=segment.pos,
#                         string=segment.string,
#                     )
#                 text_line.tokens.append(x)
#
#         assert tokens is None or stringLine is None
#         super(TextLine, self).__init__(
#             name=None,
#             astNode=astNode
#             # lineNo=lineNo
#         )
#         self.isResolved=False
#
#         self.textBlock = textBlock
#         #type: TextBlock
#
#         self.tokens=[]
#         # type: List[Token]
#         # Value will be set below
#
#         if tokens is not None:
#             self.tokens=list(tokens)
#         elif stringLine is not None:
#             _add_string_to_tokens(stringLine, self)
#         else:
#             pass
#
#     def resolve(self):
#         if self.textBlock.glossary is not None:
#             for (i, token) in enumerate(self.tokens):
#                 if isinstance(token, UnresolvedReference):
#                     # replace the UnresolvedReference by a new
#                     # token, either BrokenReference or Occurrence
#                     self.tokens[i]=token.resolve()
#
#
#     def _selectByType(self, t):
#         return [
#             x for x in self.tokens
#             if isinstance(x, t)
#         ]
#
#     @property
#     def references(self):
#         #type: () -> List[Reference]
#         # noinspection PyTypeChecker
#         return self._selectByType(Reference)
#
#     # @property
#     # def unresolvedReferences(self):
#     #     #type: () -> List[UnresolvedReference]
#     #     return self._selectByType(UnresolvedReference)
#
#     @property
#     def brokenReferences(self):
#         #type: () -> List[BrokenReference]
#         # noinspection PyTypeChecker
#         return self._selectByType(BrokenReference)
#
#     @property
#     def occurrences(self):
#         #type: () -> List[Occurrence]
#         # noinspection PyTypeChecker
#         return self._selectByType(Occurrence)


class TextToken(SourceModelElement):
    __metaclass__ = ABCMeta

    def __init__(self,
                 textLine,
                 text,
                 astTextToken=None):
        #type: (TextLine, Text, Optional['grammar.TextToken'] ) -> None

        super(TextToken, self).__init__(
            model=textLine.model,
            name=None,
            astNode=astTextToken
        )
        self.isResolved=False

        self.text=text
        #type: Text

        self.textLine=textLine
        #type: TextLine

        self.textLine.addTextToken(self)

    @abstractmethod
    def resolve(self):
        pass



class PlainText(TextToken):

    def __init__(self,
                 textLine,
                 text,
                 astPlainText=None):
        #type: (TextLine, Text, Optional['grammar.PlainText'] ) -> None
        super(PlainText, self).__init__(
            textLine, text, astPlainText)
        self.isResolved=True

    def resolve(self):
        pass


class TextReference(TextToken):
    __metaclass__ = ABCMeta

    def __init__(self,
                 textLine,
                 text,
                 astTextReference=None):
        #type: (TextLine, Text, Optional['grammar.TextReference']) -> None
        super(TextReference, self).__init__(
            textLine, text, astTextReference)

        self._isBroken=None
        #type: Optional['Boolean']

        self.entry=None
        #type: Optional[Entry]
        # Add the occurrence to the reference to the entry

    @property
    def isOccurrence(self):
        return self.isResolved and not self._isBroken

    @property
    def isBroken(self):
        return self.isResolved and self._isBroken

    def resolve(self):
        g = self.textLine.textBlock.glossary
        if g is not None:
            entry_or_none=g.findEntry(self.text)
            if entry_or_none is None:
                self._isBroken=True
            else:
                self._isBroken=False
                self.entry=entry_or_none
                self.entry.occurrences.append(self)


                #
# class UnresolvedReference(Reference):
#     def __init__(self,
#                  textLine,
#                  text,
#                  astReferenceNode=None):
#         #type: (TextLine, Text, Optional['grammar.Reference']) -> None
#         super(UnresolvedReference, self).__init__(
#             textLine, text, astReferenceNode)
#
#     def resolve(self):
#         #type: () -> Union[BrokenReference, Occurrence]
#         """
#         Resolve the token with the glossary defined
#         in the text block. Return a new token:
#         - a BrokenReference if no entry is found
#         - an Occurrence if an entry is not found
#         The calling method is in charge to replace
#         this very text token by the result of this method.
#         If no glossary was provided then the token
#         is left untouched.
#         """
#         g = self.textLine.textBlock.glossary
#         if g is not None:
#             entry_or_none=g.findEntry(self.text)
#             if entry_or_none is None:
#                 new_entry=BrokenReference(
#                     line=self.line,
#                     pos=self.pos,
#                     string=self.string)
#             else:
#                 new_entry=Occurrence(
#                     line=self.line,
#                     pos=self.pos,
#                     string=self.string,
#                     entry=entry_or_none)
#         else:
#             new_entry=self
#         return new_entry
#
#
# class BrokenReference(Reference):
#
#     def __init__(self, line, pos, string):
#         #type: (TextLine, int, Text) -> None
#         super(BrokenReference, self).__init__(line, pos, string)
#
#     @property
#     def isBroken(self):
#         return True
#
#
# class Occurrence(Reference):
#
#     def __init__(self, line, pos, string, entry):
#         #type: (TextLine, int, Text, Optional['Term']) -> None
#         super(Occurrence, self).__init__(line, pos, string)
#
#         self.entry=entry
#         # Add the occurrence to the reference to the entry
#         self.entry.occurrences.append(self)
#
#
#     @property
#     def isBroken(self):
#         return False


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