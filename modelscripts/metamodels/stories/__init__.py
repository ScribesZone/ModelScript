# coding=utf-8
"""
Code of the Scenario metamodel.

The global structure of this metamodel is as following::

    Story
        <>--* Step O
        ----1 Model

    Step
    <|-- CompositeStep
        <|-- Story
        <|-- VerbStep
        <|-- TextStep
    <|-- IncludeStep
    <|-- OperationStep ... (defined in Operations)
        <|-- ...

    IncludeStep
        ---> 1 AbstractStoryId

    AbstractStoryCollection


The hierarchy of step is recursive but Story is the only root.
"""


from typing import Optional, List, Text, Union
from abc import ABCMeta, abstractproperty, abstractmethod
from modelscripts.megamodels.elements import SourceModelElement
from modelscripts.metamodels.permissions.sar import Subject


META_CLASSES=(
    'Story',
    'Step',
    'CompositeStep'
    'TextStep',
    'VerbStep',
    'IncludeStep',
    'AbstractStoryId',
    'AbstractStoryCollection',
    'EmptyStoryCollection'
)

__all__=META_CLASSES

DEBUG=3


class Step(SourceModelElement, Subject):
    """
    Abstract class for all steps.
    This class deal with
    (1) the hierarchy through "parent" management.
    (2) accesses with "superSubjects" / "subjectLabel"
    (3) hasOperations to indicates if (a) the step is an
        operation or if (b) there is an operation in its
        substeps (if any).
    """
    __metaclass__ = ABCMeta

    def __init__(self,
                 model,
                 parent,
                 astNode=None,
                 lineNo=None,
                 description=None):
        super(Step, self).__init__(
            model=model,
            name=None,
            astNode=astNode,
            lineNo=lineNo,
            description=description)

        self.parent=parent
        #type: Optional[Step]

        if parent is not None:
            self.parent.steps.append(self)

    # @abstractproperty
    # def hasOperations(self):
    #     raise NotImplementedError('hasOperations')

    @property
    def superSubjects(self):
        """ Direct parents """
        # type: () -> List[Subject]
        return [self.parent]

    @property
    def subjectLabel(self):
        """ Label of step. Using something like "story.3.2.5" """
        parent_label=self.parent.subjectLabel
        nth_label=self.parent.steps.index(self)+1
        return '%s.%s' % (parent_label, nth_label)


class CompositeStep(Step):
    """
    Composite steps have substeps and therefore a "steps"
    attribute.
    Only composites have (nested) steps but all steps have
    a parent (see Steps).
    The parent of step is None for Stories.
    """
    __metaclass__ = ABCMeta

    def __init__(self,
                 model,
                 parent,
                 astNode=None,
                 lineNo=None,
                 description=None):
        super(CompositeStep, self).__init__(
            model=model,
            parent=parent,
            astNode=astNode,
            lineNo=lineNo,
            description=description)

        self.steps=[]
        #type: List[Step]
    #
    # @property
    # def hasOperations(self):
    #     for substep in self.steps:
    #         if substep.hasOperations:
    #             return True
    #     else:
    #         return False


class Story(CompositeStep):
    """
    A story, that is, a root of a Step hierarchy.
    Note that multiple stories can exists in the
    context of AbstractStoryCollection.
    Since they are rool, all stories have parent
    is None.
    NOTE: while a Story is a root, this is not
    the case for StoryEvaluation since these can
    be included. See StoryEvaluation for more
    details.
    """

    def __init__(self,
                 model,
                 astNode=None,
                 lineNo=None,
                 description=None):
        # """
        # Create the story.
        # The "model" might be unknown at this time, but it can
        # be set later. Subclasses of Step will compute "model"
        # at initialization time (e.g. "self.model = parent.model").
        # As long as the attribute "model" is defined for the root
        # (the Story), this is ok.
        # """
        super(Story, self).__init__(
            model=model,
            parent=None,
            astNode=astNode,
            lineNo=lineNo,
            description=description)

    @property
    def superSubjects(self):
        return [self.model]

    @property
    def subjectLabel(self):
        return 'story'


class TextStep(CompositeStep):
    """
    Annotated text block. That is, a text block with some steps.
    """

    def __init__(self,
                 parent,
                 textBlock,
                 astNode=None,
                 lineNo=None,
                 description=None):
        super(TextStep, self).__init__(
            model=parent.model,
            parent=parent,
            astNode=astNode,
            lineNo=lineNo,
            description=description)

        self.textBlock=textBlock


class VerbStep(CompositeStep):
    """
    A step with a subject and verb, plus steps in the block.
    """
    def __init__(self,
                 parent,
                 subjectName,
                 verbName,
                 astNode=None,
                 lineNo=None,
                 description=None):
        super(VerbStep, self).__init__(
            model=parent.model,
            parent=parent,
            astNode=astNode,
            lineNo=lineNo,
            description=description)

        self.subjectName=subjectName
        self.verbName=verbName


class AbstractStoryId(object):
    """
    Identifier of a story. Concrete classes must
    be defined in metamodel reusing "stories".
    (Abstract)StoryIds are used by IncludeStep
    to identify which story should be included.
    This class is also used by AbstractStoryCollection.
    """
    __metaclass__ = ABCMeta

    pass


class IncludeStep(Step):
    """
    A step corresponding to the inclusion of a story.
    Only the kind/name of the story is stored. That story
    associated with this name depends on the environment
    given to the evaluator.
    """
    def __init__(self,
                 parent,
                 storyId,
                 words=(),
                 astNode=None,
                 lineNo=None,
                 description=None):
        #type: (Step, AbstractStoryId, Optional['ASTIncludeStep'], Optional[int], Optional['TextBlock']) -> None
        super(IncludeStep, self).__init__(
            model=parent.model,
            parent=parent,
            astNode=astNode,
            lineNo=lineNo,
            description=description)

        self.storyId=storyId
        #type: AbstractStoryId
        # The story id. This corresponds to the logical/internal
        # representation.

        self.words=words
        #type: List[Text]
        # The external, concrete syntax.
        # This could be used for printing or error message.


class AbstractStoryCollection(object):
    """
    Abstract class describing collections of stories indexed
    by AbstractStoryId.
    In practice and currently there is only one AbstractStoryCollection.
    The "stories" package does not provided any concrete implementation.
    There is no syntactic elements in the "stories" package to
    represent this collection. So this is in the metamodel but not in
    the syntax.
    The "scenarios" package fill this gap, providing
    a concrete implementation for AbstractStoryCollection.
    """
    @abstractmethod
    def story(self, storyId):
        #type: (AbstractStoryId) -> Optional[Story]
        """
        Return for a given story id, the corresponding story.
        If there is no such story available for this story then
        return None.
        """
        raise NotImplementedError('story() not implemented')


class EmptyStoryCollection(AbstractStoryCollection):

    def story(self, storyId):
        return None