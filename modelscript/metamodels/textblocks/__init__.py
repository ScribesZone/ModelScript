# coding=utf-8
"""Metamodel component for TextBlocks made of TextLines possibly
making references to entries in glossaries.

This metamodel component is used to store the documentation all kinds
of entities, of models, classes, usecases, and so on.

TextBlock does not constitute a language per itself. TextBlock
is made of (1) a metamodel component and (2) a script component.
These components are to be embedded in all other languages.

Note that the TextBlock metamodel component is separated from the
glossary metamodel (which is a full-fledge language). The TextBlock
component can appear anywhere, in any metamodels. As
a particular case TextBlocks can appear in glossary models as well.
On the other way around TextBlocks use references to glossaries.

This TextBlock metamodel and the corresponding syntax play a unique role
in the modelscript framework in the sense that TextBlocks are made
available in all other languages.
By contrast to other metamodels, such as the glossary metamodel for
instance, the TextBlocks defined here are embedded in the languages
themselves. With regular imports a symbol is just referenced in
the importing language. Here the TextBlock syntactic definitions are parts
of target grammar and the metamodel.

The structure of the meta elements ::

    Model (WithTextBlocks)
      <>--* TextBlock
            <>--* TextLine
                    <>--* TextToken
                            <|-- PlainText
                            <|-- Reference

Note that in this diagram TextBlock are stored all together at the top
level directly under the model. This global registry of TextBlocks allows
operations such as glossary-based resolution, all at once. From
a syntactic point of view TextBlock are under all kinds of model elements
for instance attribute, association, etc. This hierarchy is not the
one used here.
"""

from typing import Text, Optional, List, Any, Union, cast
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
    """ Facet (mixin) for the class Model.
    Each model store at the top level, flat level, the set of all
    TextBlock that it contains, whatever the model element it is
    attached to. That means that the documentation of the model itself,
    will stored with the documentation of a class, the documentation
    of an attribute, etc. All TextBlock are gathered in the same place.
    The nesting documentation inside of nested model elements is
    ignored. The availability of all TextBlocks, irrespective of their
    position inside the model, is enough to deal with TextBlock/Glossary
    resolution.
    """

    _textBlocks: List['TextBlock']
    """List of all text blocks in the model."""

    def __init__(self):
        self._textBlocks = []

    @property
    def glossaryList(self):
        """The list of glossaries connected to the model.
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
    def textBlocksMetrics(self) -> Metrics:
        """Metrics for all text blocks in the model"""
        ms = Metrics()
        for tb in self.textBlocks:
            ms.addMetrics(tb.metrics)
        return ms

    @property
    def textBlocks(self):
        """The list of all TextBlocks in the model.
        """
        return self._textBlocks

    def addTextBlock(self, textBlock):
        """Add a TextBlock to the list
        Called by the TextBlock constructor to add
        each text block to the model it is contained in.
        """
        self._textBlocks.append(textBlock)

    def resolveTextBlocks(self):
        """Resolve all TextBlocks"""
        if len(self.glossaryList) != 0:
            for block in self.textBlocks:
                block.resolve()


GlossaryModel = 'GlossaryModel'
Entry = 'Entry'


class TextBlock(SourceModelElement):
    """A TextBlock included in a ModelElement.
    A TextBlock is made of a list of TextLines.
    """

    container: ModelElement
    """Model element containing directly the TextBlock.
    For instance if an attribute contains a documentation,
    then the attribute will contain the TextBlock.
    """

    textLines: List['TextLine']
    """List of TextLines that make the TextBlock.
    """

    isResolved: bool
    """Whether the TextBlock has been resolved with the glossary 
    or not.
    """

    def __init__(self,
                 container: ModelElement,
                 astTextBlock: 'grammar.TextBlock')\
            -> None:
        """
        Create a new TextBlock and register it to list of TextBlock
        in the model. The TextBlock is registered at the top level
        but there is no back link for the container.

        About the container back link.
        ------------------------------
        Note that there is no back link set from the container
        to the TextBlock. There is no definitive
        rule that say in which attribute the TextBlock is stored.
        Additionally a ModelElement can contain various TextBlock.
        That said, in practice most of the time the TextBlock is
        stored in the "description" field of the ModelElement.

        Args:
            container: the syntactic container of the TextBlock.
                For instance this could be an attribute if the TextBlock
                is the attribute documentation.
            astTextBlock:  an AST Node. The syntactic representation
                of the TextBlock.
        """

        SourceModelElement.__init__(
            self,
            model=container.model,
            name=None,
            astNode=astTextBlock)

        assert(container is not None)
        assert(astTextBlock is not None)
        assert(isinstance(container, ModelElement))

        # The container of the TextBlock can be any SourceModelElement,
        # such as for instance a Usecase, Actor, but can also be a Model
        # for those TextBlock at the model top level.
        self.container = container

        # Register the TextBlock to the model top level list
        self.container.model.addTextBlock(self)

        # Text lines will be added later
        self.textLines = []

        # TextBlock is not yet resolved.
        self.isResolved = False

    def addTextLine(self, textLine: 'TextLine') -> None:
        self.textLines.append(textLine)

    def resolve(self):
        """Resolve the TextBlock."""
        for l in self.textLines:
            l.resolve()
        self.isResolved = True

    @property
    def metrics(self) -> Metrics:
        ms = Metrics()
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
    """TextLine containing TextTokens. Each textLines is part
    of a TextBlock.
    """

    isResolved: bool
    textBlock: TextBlock
    textTokens: List['TextToken']

    def __init__(self,
                 textBlock: TextBlock,
                 astTextLine: Optional['grammar.TextLine'] = None
                 ) -> None:
        super(TextLine, self).__init__(
            model=textBlock.model,
            name=None,
            astNode=astTextLine
        )
        self.isResolved = False

        self.textBlock = textBlock

        self.textTokens = []
        # Value will be set below

        self.textBlock.addTextLine(self)

    def resolve(self):
        for textToken in self.textTokens:
            textToken.resolve()
        self.isResolved = True

    def _selectByType(self, t):
        return [
            x for x in self.textTokens
            if isinstance(x, t)
        ]

    @property
    def plainTexts(self) -> List['PlainText']:
        return cast(List['PlainText'], self._selectByType(PlainText))

    @property
    def textReferences(self) -> List['TextReference']:
        return cast(List['TextReference'],
                    self._selectByType(TextReference))

    @property
    def brokenReferences(self) -> List['TextReference']:
        return [
            r for r in self.textReferences
            if r.isBroken
        ]

    @property
    def occurrences(self) -> List['TextReference']:
        return [
            r for r in self.textReferences
            if r.isOccurrence
        ]

    def addTextToken(self, token: 'TextToken') -> None:
        return self.textTokens.append(token)


class TextToken(SourceModelElement, metaclass=ABCMeta):
    """A TextToken is part of a TextLine. Either
    a PlainText or a Reference.
    """

    text: str
    """The text represenation of the token."""

    textLine: TextLine
    isResolved: bool


    def __init__(self,
                 textLine: TextLine,
                 text: str,
                 astTextToken: Optional['grammar.TextToken'] = None) \
            -> None:

        super(TextToken, self).__init__(
            model=textLine.model,
            name=None,
            astNode=astTextToken
        )
        self.isResolved = False
        self.text = text
        self.textLine = textLine
        self.textLine.addTextToken(self)

    @abstractmethod
    def resolve(self):
        pass


class PlainText(TextToken):

    def __init__(self,
                 textLine: TextLine,
                 text: str,
                 astPlainText: Optional['grammar.PlainText'] = None)\
            -> None:

        super(PlainText, self).__init__(
            textLine, text, astPlainText)

    def resolve(self):
        self.isResolved = True


class TextReference(TextToken):

    _isBroken: Optional[bool]
    entry: Optional[Entry]

    def __init__(self,
                 textLine: TextLine,
                 text: str,
                 astTextReference:
                    Optional['grammar.TextReference'] = None) \
            -> None:
        super(TextReference, self).__init__(
            textLine, text, astTextReference)

        self._isBroken = None
        self.entry = None

    @property
    def isOccurrence(self):
        return self.isResolved and not self._isBroken

    @property
    def isBroken(self):
        return self.isResolved and self._isBroken

    def resolve(self):
        if DEBUG >= 2:
            print('TXT: Searching term "%s"' % self.text)
        for glossary in self.model.glossaryList:
            if DEBUG >= 2:
                print('TXT: Searching in %s' % glossary)
            entry_or_none = glossary.findEntry(self.text)
            if entry_or_none is not None:
                if DEBUG >= 2:
                    print('TXT: found in %s' % glossary)
                self._isBroken = False
                self.entry = entry_or_none
                self.entry.occurrences.append(self)
                self.isResolved = True
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
