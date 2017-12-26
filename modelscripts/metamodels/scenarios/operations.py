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
    AssociationClass,
    Attribute,
)
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
        code=None, lineNo=None, docComment=None, eolComment=None):
        SourceModelElement.__init__(self,
            model=block.model,
            name=name,
            code=code, lineNo=lineNo,
            docComment=docComment, eolComment=eolComment)
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
                 block, name=None,
                 code=None, lineNo=None, docComment=None, eolComment=None):
        super(ReadOperation, self).__init__(block, name, code, lineNo, docComment, eolComment)


class UpdateOperation(Operation):
    __metaclass__ = ABCMeta


    def __init__(self,
        block, name=None,
        code=None, lineNo=None, docComment=None, eolComment=None):
        super(UpdateOperation, self).__init__(block, name, code, lineNo, docComment, eolComment)


#--------------------------------------------------------------
#   Update operations
#--------------------------------------------------------------

class ObjectCreation(UpdateOperation):
    """
    """
    def __init__(self, block,
                 variableName, class_, id=None,
                 code=None, lineNo=None, docComment=None, eolComment=None):
        super(ObjectCreation, self).__init__(block, variableName, code, lineNo, docComment, eolComment)

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
                 code=None, lineNo=None, docComment=None, eolComment=None):
        super(ObjectDestruction, self).__init__(block, variableName, code, lineNo, docComment, eolComment)


class LinkCreation(UpdateOperation):
    def __init__(self, block,
                 names, association, id=None,
                 code=None, lineNo=None, docComment=None, eolComment=None):
        super(LinkCreation, self).__init__(block, None, code, lineNo, docComment, eolComment)

        self.names=names #type:List[Text]

        self.association=association
        # type: Association

        self.id=id #type:Optional[Text]


class LinkDestruction(UpdateOperation):
    def __init__(self, block,
                 names, association,
                 code=None, lineNo=None, docComment=None, eolComment=None):
        super(LinkDestruction, self).__init__(block, None, code, lineNo, docComment, eolComment)

        self.names=names

        self.association = association
        # type: Association


class LinkObjectCreation(UpdateOperation):
    def __init__(self, block,
                 variableName=None, names=(), id=None, associationClass=None,
                 code=None, lineNo=None, docComment=None, eolComment=None):
        super(LinkObjectCreation, self).__init__(block, variableName, code, lineNo, docComment, eolComment)
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
                 code=None, lineNo=None, docComment=None, eolComment=None):
        super(AttributeAssignment, self).__init__(block, None, code, lineNo, docComment, eolComment)

        self.variableName = variableName
        self.attributeName = attributeName
        # type: Attribute

        self.expression = expression


#--------------------------------------------------------------
#   Read operations
#--------------------------------------------------------------

class Query(ReadOperation):
    def __init__(self, block,
                 expression,
                 verbose=False,
                 code=None, lineNo=None, docComment=None, eolComment=None):
        super(Query, self).__init__(
            block=block,
            name=None,
            code=code,
            lineNo=
            lineNo,
            docComment=docComment, eolComment=eolComment)

        self.expression = expression
        self.verbose = verbose

class AssertQuery(Query):
    def __init__(self, block,
                 expression,
                 verbose=False,
                 code=None, lineNo=None, docComment=None, eolComment=None):
        super(AssertQuery, self).__init__(
            block=block,
            expression=expression,
            verbose=verbose,
            code=code, lineNo=lineNo,
            docComment=docComment, eolComment=eolComment)



class Check(ReadOperation):
    def __init__(self, block,
                 verbose=False,
                 showFaultyObjects=False,
                 all=True,
                 code=None, lineNo=None, docComment=None, eolComment=None):
        super(Check, self).__init__(block, None, code, lineNo, docComment, eolComment)

        self.verbose = verbose
        self.showFaultyObjects = showFaultyObjects
        self.all=all
