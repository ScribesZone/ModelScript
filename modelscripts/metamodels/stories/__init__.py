# coding=utf-8
"""
Code of the Scenario metamodel.

The global structure of this metamodel is as following::

    Story
        <>--* Step
            <>-- * Step O

    Step
    <|-- CompositeStep
        <|-- Story
        <|-- VerbStep
        <|-- TextStep
    <|-- OperationStep

The hierarchy of step is recursive but Story is the only root.

"""


from typing import Optional, List
from abc import ABCMeta
from modelscripts.megamodels.elements import SourceModelElement
from modelscripts.metamodels.permissions.sar import Subject


META_CLASSES=(
    'Story',
    'Step',
    'CompositeStep'
    'TextStep',
    'VerbStep',
)

__all__=META_CLASSES

DEBUG=3


class Step(SourceModelElement, Subject):
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

    @property
    def superSubjects(self):
        """ Direct parents """
        # type: () -> List[Subject]
        return [self.parent]

    @property
    def subjectLabel(self):
        parent_label=self.parent.subjectLabel
        nth_label=self.parent.steps.index(self)+1
        return '%s.%s' % (parent_label, nth_label)


class CompositeStep(Step):
    """
    Composite steps have substeps and therefore a steps attribute.
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


class Story(CompositeStep):

    def __init__(self,
                 model,
                 astNode=None,
                 lineNo=None,
                 description=None):
        # """
        # Create the story. The model might be unknown at this
        # time, but it can be set later. Subclasses of step
        # will compute model dynamically so any update is ok.
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


