# coding=utf-8
"""
Meta elements for modeling operations

The structure of this package is the following::

    Step
    <|-- OperationStep
        <|-- UpdateStep
            <|-- ObjectCreationStep
            <|-- ObjectDeletionStep
            <|-- SlotStep
            <|-- LinkCreationStep
            <|-- LinkDeletionStep
            <|-- LinkObjectCreationStep
        <|-- ConsultStep
            <|-- CheckStep
            <|-- ReadStep

"""
from abc import ABCMeta

from typing import Optional, Text
from typing_extensions import Literal

from modelscript.metamodels.textblocks import TextBlock
from modelscript.metamodels.classes.classes import (
    PlainClass)
from modelscript.metamodels.classes.assocclasses import (
    AssociationClass)
from modelscript.metamodels.classes.associations import (
    PlainAssociation,
    Association)
from modelscript.metamodels.classes.types import SimpleValue
from modelscript.base.grammars import AST

from modelscript.metamodels.stories import Step, CompositeStep

META_CLASSES=[
    'OperationStep',
    'UpdateStep',
    'ObjectCreationStep',
    'ObjectDeletionStep',
    'SlotStep',
    'LinkCreationStep',
    'LinkDeletionStep',
    'LinkObjectCreationStep',
    'LinkObjectDeletionStep',
    'ConsultStep',
    'CheckStep',
    'ReadStep',
]
__all__=META_CLASSES


# --------------------------------------------------------------
#   Abstract classes
# --------------------------------------------------------------


class OperationStep(Step, metaclass=ABCMeta):
    def __init__(self,
                 parent: CompositeStep,
                 astNode: Optional['TextXNode'] = None,
                 lineNo: Optional[int] = None,
                 description: Optional[TextBlock] = None):
        super(OperationStep, self).__init__(
            model=parent.model,
            parent=parent,
            astNode=astNode,
            lineNo=lineNo,
            description=description)

    @property
    def hasOperations(self):
        return True


class UpdateOperationStep(OperationStep, metaclass=ABCMeta):

    isAction: bool

    def __init__(self,
                 parent: CompositeStep,
                 isAction: bool,
                 astNode: Optional['TextXNode'] = None,
                 lineNo: Optional[int] = None,
                 description: Optional[TextBlock] = None):
        super(UpdateOperationStep, self).__init__(
            parent=parent,
            astNode=astNode,
            lineNo=lineNo,
            description=description)

        self.isAction = isAction


class ConsultOperationStep(OperationStep, metaclass=ABCMeta):
    def __init__(self,
                 parent: CompositeStep,
                 astNode: Optional['TextXNode'] = None,
                 lineNo: Optional[int] = None,
                 description: Optional[TextBlock] = None):
        super(ConsultOperationStep, self).__init__(
            parent=parent,
            astNode=astNode,
            lineNo=lineNo,
            description=description)


# --------------------------------------------------------------
#   Update operations
# --------------------------------------------------------------


class ObjectCreationStep(UpdateOperationStep):
    """Creation of an object. The class is known.
    """

    objectName: str
    class_: PlainClass
    def __init__(self,
                 parent: CompositeStep,
                 isAction: bool,
                 objectName: str,
                 class_: PlainClass,
                 astNode: Optional['TextXNode'] = None,
                 lineNo: Optional[int] = None,
                 description: Optional[TextBlock] = None):
        super(ObjectCreationStep, self).__init__(
            parent=parent,
            isAction=isAction,
            astNode=astNode,
            lineNo=lineNo,
            description=description)

        assert isinstance(class_, PlainClass)

        self.objectName = objectName
        self.class_ = class_


class SlotStep(UpdateOperationStep):
    """Assignment like "o"."a"=v. The names of the object
    and the attribute are known but not the attribute/object.
    """

    objectName: str
    attributeName: str
    simpleValue: SimpleValue

    isUpdate: Optional[bool]
    """Indicates if this is an initialization or an isUpdate
    this indication could be given in the syntax (or not).
    """

    def __init__(self,
                 parent: CompositeStep,
                 isAction: bool,
                 objectName: str,
                 attributeName: str,
                 value: 'BasicValue',
                 isUpdate: Optional[bool] = None,
                 astNode: Optional['TextXNode'] = None,
                 lineNo: Optional[int] = None,
                 description: Optional[TextBlock] = None):
        super(SlotStep, self).__init__(
            parent=parent,
            isAction=isAction,
            astNode=astNode,
            lineNo=lineNo,
            description=description)

        self.objectName = objectName
        self.attributeName = attributeName
        self.simpleValue = value
        self.isUpdate = isUpdate


class ObjectDeletionStep(UpdateOperationStep):
    """Deletion of a regular object OR of a link object.
    Only the name of the object is known.
    No indication about the class/association class.
    """

    objectName: str

    def __init__(self,
                 parent: CompositeStep,
                 objectName: str,
                 astNode: Optional['TextXNode'] = None,
                 lineNo: Optional[int] = None,
                 description: Optional[TextBlock] = None):
        super(ObjectDeletionStep, self).__init__(
            parent=parent,
            isAction=True,
            astNode=astNode,
            lineNo=lineNo,
            description=description)

        self.objectName = objectName


class LinkCreationStep(UpdateOperationStep):
    """Creation of a link like "(o1, R, o2)" where R is a
    PlainAssociation. The name of the plain association is known.
    Names of objects are known but not the objects themselves.
    """

    sourceObjectName: str
    targetObjectName: str
    association: PlainAssociation

    def __init__(self,
                 parent: CompositeStep,
                 isAction: bool,
                 sourceObjectName: str,
                 targetObjectName: str,
                 association: PlainAssociation,
                 astNode: Optional['TextXNode'] = None,
                 lineNo: Optional[int] = None,
                 description: Optional[TextBlock] = None):

        super(LinkCreationStep, self).__init__(
            parent=parent,
            isAction=isAction,
            astNode=astNode,
            lineNo=lineNo,
            description=description)

        self.sourceObjectName = sourceObjectName
        self.targetObjectName = targetObjectName
        self.association = association


class LinkDeletionStep(UpdateOperationStep):
    """ Deletion of a link like "o1" R "o2": the name of association
    is known. Names of objects are known but not the objects.
    """

    sourceObjectName: str
    targetObjectName: str
    association: PlainAssociation


    def __init__(self,
                 parent: CompositeStep,
                 sourceObjectName: str,
                 targetObjectName: str,
                 association: PlainAssociation,
                 astNode: Optional['TextXNode'] = None,
                 lineNo: Optional[int] = None,
                 description: Optional[TextBlock] = None):
        super(LinkDeletionStep, self).__init__(
            parent=parent,
            isAction=True,
            astNode=astNode,
            lineNo=lineNo,
            description=description)

        self.sourceObjectName = sourceObjectName
        self.targetObjectName = targetObjectName
        self.association = association


class LinkObjectCreationStep(UpdateOperationStep):
    """Creation of a link object like "x : AC (o1, o2).
    The name AC of the association class is known.
    Names of objects are known but not the objects.
    """

    linkObjectName: str
    sourceObjectName: str
    targetObjectName: str
    associationClass: AssociationClass

    def __init__(self,
                 parent: CompositeStep,
                 isAction: bool,
                 linkObjectName: str,
                 sourceObjectName: str,
                 targetObjectName: str,
                 associationClass: AssociationClass,
                 astNode: Optional['TextXNode'] = None,
                 lineNo: Optional[int] = None,
                 description: Optional[TextBlock] = None):

        super(LinkObjectCreationStep, self).__init__(
            parent=parent,
            isAction=isAction,
            astNode=astNode,
            lineNo=lineNo,
            description=description)

        assert isinstance(associationClass, AssociationClass)
        self.linkObjectName = linkObjectName
        self.sourceObjectName =sourceObjectName
        self.targetObjectName = targetObjectName
        self.associationClass = associationClass


# --------------------------------------------------------------
#   Consult operations
# --------------------------------------------------------------


class CheckStep(ConsultOperationStep):

    number: int
    """The index of the CheckStep in the story.
    It is computed be StoryFiller.story().
    This number is used to give a unique label to each CheckStep.
    """

    position: Optional[Literal['before', 'after']]
    """ Indicates if the check statement is explicit (None)
    or implicit 'before' or 'after' a block. These implicit
    checks are automatically added by the parser.
    """

    def __init__(self,
                 parent,
                 number,
                 position=None,
                 astNode=None):
        super(CheckStep, self).__init__(
            parent=parent,
            astNode=astNode)

        self.number = number
        self.position = position

    @property
    def isImplicit(self):
        return self.position is not None

    @property
    def label(self):
        # property label might not be necessary
        return self.subjectLabel

    @property
    def subjectLabel(self):
        """
        Label like
        * "A.3.2" if the check is explicit
        * or "A.2.before_1" if the check is before step 1
        """
        parent_label = self.parent.subjectLabel
        nth_label = self.parent.steps.index(self)+1
        if self.isImplicit:
            return '%s.%s_%s' % (
                parent_label,
                self.position,
                nth_label)
        else:
            return '%s.%s' % (
                parent_label,
                nth_label)



class ReadStep(ConsultOperationStep):
    def __init__(self,
                 parent,
                 astNode=None, lineNo=None, description=None):
        super(ReadStep, self).__init__(
            parent=parent,
            astNode=astNode,
            lineNo=lineNo,
            description=description)

        # TODO:4 implement ReadStep
        pass
