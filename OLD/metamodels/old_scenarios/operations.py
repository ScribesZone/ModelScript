# coding=utf-8
"""
Meta elements for modeling operations

The structure of this package is the following::

    Operation
    <|-- ReadOperation
        <|-- Query (soil command '?' and '??')
        <|-- Check (soil command 'check')
    <|-- UpdateOperation
        <|-- ObjectCreation (soil commands '!new' and '!create'
        <|-- ObjectDestruction (soil command )
        <|-- LinkCreation (soil command '! insert')
        <|-- LinkDestruction (soil command )
        <|-- LinkObjectCreation (soil command '! new between')
        <|-- AttributeAssignment (soil command '! :=' )



"""
from abc import ABCMeta

from typing import Optional, List, Text

from modelscripts.megamodels.elements import SourceModelElement
from modelscripts.metamodels.classes import (
    Class,
    Association,
)
from modelscripts.metamodels.classes.assocclasses import AssociationClass
from modelscripts.metamodels.classes.classes import Attribute
from modelscripts.metamodels.permissions.sar import Subject

META_CLASSES=[
    'Operation',
    'ReadOperation',
    'UpdateOperation',
    'ObjectCreation',
    'ObjectDestruction',
    'LinkCreation',
    'LinkDestruction',
    'LinkObjectCreation',
    'AttributeAssignment',
    'Query',
    'Check'
]
__all__=META_CLASSES

#--------------------------------------------------------------
#   Abstract classes
#--------------------------------------------------------------

class Operation(SourceModelElement, Subject):
    __metaclass__ = ABCMeta

    META_COMPOSITIONS=[
        'operationEvaluation',
    ]

    def __init__(self,
        block,
        name=None,
        astNode=None, lineNo=None, description=None):
        SourceModelElement.__init__(self,
            model=block.model,
            name=name,
            astNode=astNode, lineNo=lineNo,
            description=description)
        self.block=block
        self.block.operations.append(self)

        # evaluation
        self.operationEvaluation=None #filled if evaluated
        #type: Optional['OperationEvaluation']

    @property
    def superSubjects(self):
        return [self.block]

    @property
    def subjectLabel(self):
        return 'operation'


class ReadOperation(Operation):
    __metaclass__ = ABCMeta

    def __init__(self,
                 block,
                 name=None,
                 astNode=None, lineNo=None,
                 description=None):
        super(ReadOperation, self).__init__(
            block=block,
            name=name,
            astNode=astNode,
            lineNo=lineNo,
            description=description)


class UpdateOperation(Operation):
    __metaclass__ = ABCMeta


    def __init__(self,
        block, name=None,
        astNode=None, lineNo=None, description=None):
        super(UpdateOperation, self).__init__(
            block=block,
            name=name,
            astNode=astNode,
            lineNo=lineNo,
            description=description)

#--------------------------------------------------------------
#   Update operations
#--------------------------------------------------------------

class ObjectCreation(UpdateOperation):
    """
    """
    def __init__(self, block,
                 variableName, class_, id=None,
                 astNode=None, lineNo=None, description=None):
        super(ObjectCreation, self).__init__(
            block=block,
            name=variableName,
            astNode=astNode,
            lineNo=lineNo,
            description=description)

        self.class_=class_
        # type: Class

        self.id=id
        # type: Optional[str]


class ObjectDestruction(UpdateOperation):
    """
    Destruction of a regular object OR of a link object.
    """
    def __init__(self, block,
                 variableName,
                 astNode=None, lineNo=None, description=None):
        super(ObjectDestruction, self).__init__(
            block=block,
            name=variableName,
            astNode=astNode,
            lineNo=lineNo,
            description=description)


class LinkCreation(UpdateOperation):
    def __init__(self, block,
                 names, association, id=None,
                 astNpde=None, lineNo=None, description=None):
        super(LinkCreation, self).__init__(
            block=block,
            name=None,
            astNode=astNpde,
            lineNo=lineNo,
            description=description)

        self.names=names #type:List[Text]

        self.association=association
        # type: Association

        self.id=id #type:Optional[Text]


class LinkDestruction(UpdateOperation):
    def __init__(self, block,
                 names, association,
                 astNode=None, lineNo=None, description=None):
        super(LinkDestruction, self).__init__(
            block=block,
            name=None,
            astNode=astNode,
            lineNo=lineNo,
            description=description)

        self.names=names

        self.association = association
        # type: Association


class LinkObjectCreation(UpdateOperation):
    def __init__(self, block,
                 variableName=None,
                 names=(),
                 id=None,
                 associationClass=None,
                 astNode=None, lineNo=None, description=None):
        super(LinkObjectCreation, self).__init__(
            block=block,
            name=variableName,
            astNode=astNode,
            lineNo=lineNo,
            description=description)
        # self.name can be None
        self.names = names
        self.id = id

        self.associationClass = associationClass  # this is indeed an association class
        # type: AssociationClass


class AttributeAssignment(UpdateOperation):
    def __init__(self, block,
                 variableName,
                 attributeName,
                 expression,
                 astNode=None, lineNo=None, description=None):
        super(AttributeAssignment, self).__init__(
            block=block,
            name=None,
            astNode=astNode,
            lineNo=lineNo,
            description=description)
        self.variableName = variableName
        #TODO: check the type below
        self.attributeName = attributeName
        # type: Attribute

        self.expression = expression


#--------------------------------------------------------------
#   Read operations
#--------------------------------------------------------------

# class Query(ReadOperation):
#     def __init__(self, block,
#                  expression,
#                  verbose=False,
#                  code=None, lineNo=None, description=None, eolComment=None):
#         super(Query, self).__init__(
#             block=block,
#             name=None,
#             code=code,
#             lineNo=
#             lineNo,
#             description=description, eolComment=eolComment)
#
#         self.expression = expression
#         self.verbose = verbose
#
# class AssertQuery(Query):
#     def __init__(self, block,
#                  expression,
#                  verbose=False,
#                  code=None, lineNo=None, description=None, eolComment=None):
#         super(AssertQuery, self).__init__(
#             block=block,
#             expression=expression,
#             verbose=verbose,
#             code=code, lineNo=lineNo,
#             description=description, eolComment=eolComment)
#
#
#
# class Check(ReadOperation):
#     def __init__(self, block,
#                  verbose=False,
#                  showFaultyObjects=False,
#                  all=True,
#                  code=None, lineNo=None, description=None, eolComment=None):
#         super(Check, self).__init__(block, None, code, lineNo, description, eolComment)
#
#         self.verbose = verbose
#         self.showFaultyObjects = showFaultyObjects
#         self.all=all
