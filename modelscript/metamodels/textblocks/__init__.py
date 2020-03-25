# coding=utf-8
"""
Metamodel a TextBlocks made of TextLines possibly some References
to Entries in Glossaries.

The structure of the meta elements ::

    TextBlock
        <>--* TextLine
                <>--* TextToken
                        <|-- PlainText
                        <|-- Reference

"""

from abc import ABCMeta
from typing import (
    Text, Optional, List, Any)
from abc import ABCMeta, abstractmethod
from modelscript.base.metrics import Metrics
from modelscript.megamodels.elements import (
    SourceModelElement,
    ModelElement)

__all__ = (
    'WithTextBlocks',
    'TextBlock',
    'TextLine',
    'TextToken',
    'PlainText',
    'TextReference',
)

DEBUG=1

ISSUES={
    'TERM_NOT_FOUND': 'txt.TermNotFound',
}

def icode(ilabel):
    return ISSUES[ilabel]

class WithTextBlocks(object):
    """
    Mixin for Models. Used to extend the "Model" class.
    As a result all models can contain some texte block.
    """

    def __init__(self):
        self._textBlocks=[]

    @property
    def glossaryList(self):
        """
        The list of glossaries contected to the model.
        """
        # TODO:- improve the framework to simplify the code below
        #   When using an importBox one can write this
        #       return self.importBox.models('gl')
        #   Unfortunately this is for sources only
        #   The same should be available for models
        from modelscript.megamodels import Megamodel
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
        """
        The list of all text blocks in the model.
        """
        return self._textBlocks

    def addTextBlock(self, textBlock):
        """
        called by the TextBlock constructor to add
        each text block to the model it is contained in.
        """
        self._textBlocks.append(textBlock)

    def resolveTextBlocks(self):
        if len(self.glossaryList)!=0:
            for block in self.textBlocks:
                block.resolve()

GlossaryModel='GlossaryModel'
Entry='Entry'


class TextBlock(SourceModelElement):
    """
    A TextBlock included into a SourceModelElement.
    A TextBlock is made of a list of TextLine
    """

    def __init__(self,
                 container,
                 astTextBlock=None):
        #type: (SourceModelElement, Optional['grammar.TextBlock'] ) -> None

        SourceModelElement.__init__(
            self,
            model=container.model,
            name=None,
            astNode=astTextBlock)

        self.container=container
        # Could be for instance a Usecase, Actor, but also
        # a model, etc.
        assert(self.container is not None)
        if self.container is not None:
            assert isinstance(container, ModelElement)
            self.container.model.addTextBlock(self)

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
    """
    TextLine containing TextTokens. Each textLines is part
    of a TextBlock.
    """

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


class TextToken(SourceModelElement, metaclass=ABCMeta):
    """
    A TextToken is part of a TextLine. Either
    a PlainText or a Reference.
    """

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


class TextReference(TextToken, metaclass=ABCMeta):
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
                    print('TXT: found in %s' % glossary)
                self._isBroken=False
                self.entry=entry_or_none
                self.entry.occurrences.append(self)
                self.isResolved=True
                break
        else:
            if DEBUG >= 2:
                print('TXT: not found')
            self._isBroken = True
            from modelscript.base.grammars import (
                ASTNodeSourceIssue)
            from modelscript.base.issues import (
                Levels)
            ASTNodeSourceIssue(
                code=icode('TERM_NOT_FOUND'),
                astNode=self.astNode,
                level=Levels.Warning,
                message=(
                        'Undefined term `%s`.' % self.text))

        self.isResolved = True





