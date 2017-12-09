# coding=utf-8
"""
Metamodel a texts made of lines with possibily some references to
a entries in a glossary.

The structure of the meta elemens

    TextBlockModel
        <>--* Line
                <>--* Token
                        <|-- Reference
                                <|-- BrokenReference
                                <|-- Occurrence


"""
from __future__ import print_function
from typing import (
    Text, Optional, List, Any,
)

from modelscribes.base.metrics import Metrics
from modelscribes.base.sources import SourceElement
from modelscribes.metamodels.glossaries import GlossaryModel
from modelscribes.megamodels.models import Model
from modelscribes.megamodels.metamodels import Metamodel
from modelscribes.megamodels.dependencies.metamodels import MetamodelDependency

class TextBlockModel(Model):
    _empty=None

    @classmethod
    def empty(cls):
        """
        Singleton empty text block to make sure
        that composite model will have a textblock
        instead of none.
        """
        if cls._empty is None:
            cls._empty=TextBlockModel()
        return cls._empty

    def __init__(self,
                 glossary=None,
                 container=None,
                 lines=()):
        super(TextBlockModel, self).__init__()
        self.container=container
        # type: Optional[Any]
        self.lines = list(lines)
        # type: List[Line]
        self.glossary=glossary
        # type: Optional[GlossaryModel]


    # def resolve(self):
    #     for line in self.lines:
    #         for token in line.tokens:
    #             if isinstance(token, Reference):
    #                 reference = token
    #
    #
    #             reference.resolve(self.glossary)

    def metamodel(self):
        #type: () -> Metamodel
        raise NotImplementedError()


    @property
    def metrics(self):
        #type: () -> Metrics
        ms=super(TextBlockModel, self).metrics
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

class Line(SourceElement):

    def __init__(self, textBlock, lineNo=None, tokens=()):
        super(Line, self).__init__(
            name=None,
            lineNo=lineNo
        )

        self.textBlock = textBlock
        #type: TextBlockModel

        self.tokens = list(tokens)
        #type: List[Token]

    @property
    def references(self):
        #type: () -> List[Reference]
        return [
            t for t in self.tokens
                if isinstance(t, Reference)
        ]

    @property
    def brokenReferences(self):
        #type: () -> List[BrokenReference]
        return [
            t for t in self.tokens
                if isinstance(t, BrokenReference)
        ]


    @property
    def occurrences(self):
        #type: () -> List[Occurrence]
        return [
            t for t in self.tokens
                if isinstance(t, Occurrence)
        ]



class Token(object):

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


class BrokenReference(Reference):

    def __init__(self, line, pos, string):
        #type: (Line, int, Text, Optional['Term']) -> None
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


METAMODEL = Metamodel(
    id='tx',
    label='text',
    extension='.txs',
    modelClass=TextBlockModel,
    modelKinds=()
)
MetamodelDependency(
    sourceId='tx',
    targetId='gl',
    optional=True,
    multiple=True,
)