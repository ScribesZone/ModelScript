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
from abc import ABCMeta
from typing import (
    Text, Optional, List, Any
)
from modelscripts.megamodels.elements import (
    SourceModelElement,
    ModelElement
)
from abc import ABCMeta, abstractmethod
from modelscripts.base.metrics import Metrics

__all__ = (
    'WithTextBlocks'
    'TextBlock',
    'TextLine',
    'TextToken',
    'PlainText',
    'TextReference',
)

DEBUG=1

class WithTextBlocks(object):

    @property
    def glossaryList(self):
        #TODO: check how to get access to Megamodel globally
        from modelscripts.megamodels import Megamodel
        GLOSSARY_METAMODEL = Megamodel.theMetamodel('gl')
        return self.usedModels(
            targetMetamodel=GLOSSARY_METAMODEL)

    @property
    def textBlocksMetrics(self):
        #type: () -> Metrics
        ms=Metrics()
        for tb in self.textBlocks:
            ms.addMetrics(tb.metrics)
        return ms

    @property
    def textBlocks(self):
        _=[]
        return _

GlossaryModel='GlossaryModel'
Entry='Entry'






class TextBlock(SourceModelElement):
    """ A text block embedded into a SourceModelElement """

    def __init__(self,
                 container,
                 astTextBlock=None):
        #type: (SourceModelElement, Optional[GlossaryModel],Optional['grammar.TextBlock'] ) -> None

        super(TextBlock, self).__init__(
            model=container.model,
            astNode=astTextBlock)

        self.container=container
        # Could be for instance a Usecase, Actor, but also
        # a model etc. At the end the model containing with this
        # model element must have an attribute  glossaryModelUsed
        # (this model being a GlossaryDependent)
        if self.container is not None:
            assert isinstance(container, ModelElement)

        self.textLines=[]
        # type: List[TextLine]

        self.isResolved=False

    def addTextLine(self, textLine):
        #type: (TextLine) -> None
        self.textLines.append(textLine)

    def resolve(self):
        for l in self.textLines:
            l.resolve()
        self.isResolved=True

    # TODO: add metrics to the model with the code below
    @property
    def metrics(self):
        #type: () -> Metrics
        ms=Metrics()
        ms.addList((
            ('text block', 1),
            ('text line', len(self.textLines)),
            ('text token',
                sum(len(l.textTokens) for l in self.textLines)),
            ('text reference',
                sum(len(l.textReferences) for l in self.textLines)),
            ('broken text reference',
                sum(len(l.brokenReferences)
                    for l in self.textLines)),
            ('text occurrences',
                sum(len(l.occurrences)
                    for l in self.textLines)),
        ))
        return ms

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

    def resolve(self):
        self.isResolved=True


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
        if DEBUG>=2:
            print('TXT: Searching term "%s"' % self.text)
        for glossary in self.model.glossaryList:
            if DEBUG >= 2:
                print('TXT: Searching in %s' % glossary)
            entry_or_none=glossary.findEntry(self.text)
            if entry_or_none is not None:
                if DEBUG >= 2:
                    print('TXT: found' % glossary)
                self._isBroken=False
                self.entry=entry_or_none
                self.entry.occurrences.append(self)
                self.isResolved=True
                break
        else:
            self._isBroken = True
        self.isResolved = True





