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

from modelscripts.metamodels.textblocks import TextBlock
from modelscripts.metamodels.classes import (
    Class,
    Association,

)
from modelscripts.base.grammars import AST

from modelscripts.metamodels.stories import Step

META_CLASSES=[
    'OperationStep',
    'UpdateStep',
    'ObjectCreationStep',
    'ObjectDeletionStep',
    'SlotStep',
    'LinkCreationStep',
    'LinkDeletionStep',
    # TODO: Link Object
    'ConsultStep',
    'CheckStep',
    'ReadStep',
]
__all__=META_CLASSES

#--------------------------------------------------------------
#   Abstract classes
#--------------------------------------------------------------

class OperationStep(Step):
    __metaclass__ = ABCMeta

    def __init__(self,
        parent,
        astNode=None,
        lineNo=None,
        description=None):
        #type: (Step, Optional['ASTNode'], Optional[int], Optional[TextBlock]) -> None
        super(OperationStep, self).__init__(
            model=parent.model,
            parent=parent,
            astNode=astNode,
            lineNo=lineNo,
            description=description)


class UpdateOperationStep(OperationStep):
    __metaclass__ = ABCMeta


    def __init__(self,
                    parent, isAction, 
                    astNode=None, lineNo=None,
                    description=None):
        # type: (Step, bool, Optional['ASTNode'], Optional[int], Optional[TextBlock]) -> None
        super(UpdateOperationStep, self).__init__(
            parent=parent,
            astNode=astNode,
            lineNo=lineNo,
            description=description)

        self.isAction=isAction
        #type: bool


class ConsultOperationStep(OperationStep):
    __metaclass__ = ABCMeta


    def __init__(self,
                    parent,
                    astNode=None, lineNo=None,
                    description=None):
        # type: (Step, bool, Optional['ASTNode'], Optional[int], Optional[TextBlock]) -> None
        super(ConsultOperationStep, self).__init__(
            parent=parent,
            astNode=astNode,
            lineNo=lineNo,
            description=description)


#--------------------------------------------------------------
#   Update operations
#--------------------------------------------------------------

class ObjectCreationStep(UpdateOperationStep):
    """
    Creation of an object. The class is known.
    """
    def __init__(self,
                 parent, isAction,
                 objectName, class_,
                 astNode=None, lineNo=None, description=None):
        # type: (Step, bool, Text, Class,  Optional['ASTNode'], Optional[int], Optional[TextBlock]) -> None
        super(ObjectCreationStep, self).__init__(
            parent=parent,
            isAction=isAction,
            astNode=astNode,
            lineNo=lineNo,
            description=description)

        self.objectName=objectName
        #type: Text

        self.class_=class_
        #type: Class


class SlotStep(UpdateOperationStep):
    """
    Assignment like "o"."a"=v. The names of the object
    and the attribute are known but not the attribute/object.
    """
    def __init__(self,
                 parent, isAction,
                 objectName, attributeName, value,
                 isUpdate=None,
                 astNode=None, lineNo=None, description=None):
        # type: (Step, bool, Text, Text, 'BasicValue', Optional[bool], Optional['ASTNode'], Optional[int], Optional[TextBlock]) -> None
        super(SlotStep, self).__init__(
            parent=parent,
            isAction=isAction,
            astNode=astNode,
            lineNo=lineNo,
            description=description)

        self.objectName=objectName
        #type: Text

        self.attributeName=attributeName
        #type: Text

        self.value=value
        #type: 'BasicValue'

        self.isUpdate=isUpdate
        #type: Optional[bool]
        # Indicates if this is an initialization or an isUpdate
        # this indication could be given in the syntax (or not).


class ObjectDeletionStep(UpdateOperationStep):
    """
    Deletion of a regular object OR of a link object.
    Only the name of the object is known. No indication about
    the class/association class.
    """
    def __init__(self,
                 parent,
                 objectName,
                 astNode=None, lineNo=None, description=None):
        # type: (Step, Text, Optional[bool], Optional['ASTNode'], Optional[int], Optional[TextBlock]) -> None
        super(ObjectDeletionStep, self).__init__(
            parent=parent,
            isAction=True,
            astNode=astNode,
            lineNo=lineNo,
            description=description)

        self.objectName=objectName
        #type: Text


class LinkCreationStep(UpdateOperationStep):
    """
    Creation of a link like "o1" R "o2": the name of association
    is known. Names of objects are known but not the objects.
    """
    def __init__(self,
                 parent, isAction,
                 sourceObjectName, targetObjectName, association,
                 astNode=None, lineNo=None, description=None):
        # type: (Step, bool, Text, Text, Association, Optional['ASTNode'], Optional[int], Optional[TextBlock]) -> None

        super(LinkCreationStep, self).__init__(
            parent=parent,
            isAction=isAction,
            astNode=astNode,
            lineNo=lineNo,
            description=description)

        self.sourceObjectName=sourceObjectName
        #type:Text

        self.targetObjectName=targetObjectName
        #type:Text

        self.association=association
        # type: Association


class LinkDeletionStep(UpdateOperationStep):
    """
    Deletion of a link like "o1" R "o2": the name of association
    is known. Names of objects are known but not the objects.
    """
    def __init__(self,
                 parent,
                 sourceObjectName, targetObjectName, association,
                 astNode=None, lineNo=None, description=None):
        # type: (Step, Text, Text, Association, Optional['ASTNode'], Optional[int], Optional[TextBlock]) -> None
        super(LinkDeletionStep, self).__init__(
            parent=parent,
            isAction=True,
            astNode=astNode,
            lineNo=lineNo,
            description=description)

        self.sourceObjectName=sourceObjectName
        #type:Text

        self.targetObjectName=targetObjectName
        #type:Text

        self.association=association
        # type: Association

# class LinkObjectCreation(UpdateOperation):
#     def __init__(self, block,
#                  variableName=None,
#                  names=(),
#                  id=None,
#                  associationClass=None,
#                  astNode=None, lineNo=None, description=None):
#         super(LinkObjectCreation, self).__init__(
#             block=block,
#             name=variableName,
#             astNode=astNode,
#             lineNo=lineNo,
#             description=description)
#         # self.name can be None
#         self.names = names
#         self.id = id
#
#         self.associationClass = associationClass  # this is indeed an association class
#         # type: AssociationClass
#


#--------------------------------------------------------------
#   Consult operations
#--------------------------------------------------------------

class CheckStep(ConsultOperationStep):

    def __init__(self,
                 parent, astNode=None, position=None):
        super(CheckStep, self).__init__(
            parent=parent,
            astNode=astNode)

        self.position=position
        #type: Optional['before','after']
        """ 
        Indicates if the check statement is explicit (None)
        or implicit 'before' or 'after' a block. These implicit
        checks step are automatically added by the parser.
        """


class ReadStep(ConsultOperationStep):
    def __init__(self,
                 parent,
                 astNode=None, lineNo=None, description=None):
        super(ReadStep, self).__init__(
            parent=parent,
            astNode=astNode,
            lineNo=lineNo,
            description=description)

        # TODO: implement ReadStep
        pass
