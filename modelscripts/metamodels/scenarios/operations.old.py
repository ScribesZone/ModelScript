# # coding=utf-8
# """
# Meta elements for modeling operations
#
# The structure of this package is the following::
#
#     Operation
#     <|-- UpdateOperation
#         <|-- ObjectCreation
#         <|-- ObjectDeletion
#         <|-- AttributeAssignment
#         <|-- LinkCreation
#         <|-- LinkDeletion
#         <|-- LinkObjectCreation
#         <|-- LinkObjectDeletion
#     <|-- ConsultOperation
#         <|-- Check
#         <|-- Read
#
#
# """
# from abc import ABCMeta
#
# from typing import Optional, List, Text
#
# from modelscripts.metamodels.textblocks import TextBlock
# from modelscripts.metamodels.classes import (
#     Class,
#     Association,
#     AssociationClass,
#     Attribute,
# )
# # from modelscripts.metamodels.permissions.sar import Subject
# from modelscripts.metamodels.scenarios import Step
#
# META_CLASSES=[
#     'Operation',
#     'ReadOperation',
#     'UpdateOperation',
#     'ObjectCreation',
#     'ObjectDestruction',
#     'LinkCreation',
#     'LinkDestruction',
#     # TODO: LinkObject
#     # 'LinkObjectCreation',
#     # 'LinkObjectDeletion'
#     'AttributeAssignment',
#
#     # 'Query',
#     'Check'
# ]
# __all__=META_CLASSES
#
# #--------------------------------------------------------------
# #   Abstract classes
# #--------------------------------------------------------------
#
# class Operation(Step):
#     __metaclass__ = ABCMeta
#
#     META_COMPOSITIONS=[
#         'operationEvaluation',
#     ]
#
#     def __init__(self,
#         parent,
#         astNode=None, lineNo=None, description=None):
#         #type: (Step, Optional['ASTNode'], Optional[int], Optional[TextBlock]) -> None
#         super(Operation, self).__init__(
#             model=parent.model,
#             astNode=astNode, lineNo=lineNo,
#             description=description)
#
#         self.parentStep=parent
#         parent.steps.append(self)
#
#         # evaluation
#         self.operationEvaluation=None #filled if evaluated
#         #type: Optional['OperationEvaluation']
#
#
#
#
# class ReadOperation(Operation):
#     __metaclass__ = ABCMeta
#
#     def __init__(self,
#                  parent,
#                  astNode=None, lineNo=None,
#                  description=None):
#         #type: (Step, Optional['ASTNode'], Optional[int], Optional[TextBlock]) -> None
#         super(ReadOperation, self).__init__(
#             parent=parent,
#             astNode=astNode,
#             lineNo=lineNo,
#             description=description)
#
#
# class UpdateOperation(Operation):
#     __metaclass__ = ABCMeta
#
#
#     def __init__(self,
#                     parent,
#                     astNode=None, lineNo=None,
#                     description=None):
#         # type: (Step, Optional['ASTNode'], Optional[int], Optional[TextBlock]) -> None
#         super(UpdateOperation, self).__init__(
#             parent=parent,
#             astNode=astNode,
#             lineNo=lineNo,
#             description=description)
#
# #--------------------------------------------------------------
# #   Update operations
# #--------------------------------------------------------------
#
# class ObjectCreation(UpdateOperation):
#     """
#     """
#     def __init__(self,
#                  parent,
#                  objectName,
#                  class_,
#                  astNode=None, lineNo=None, description=None):
#         super(ObjectCreation, self).__init__(
#             parent=parent,
#             astNode=astNode,
#             lineNo=lineNo,
#             description=description)
#
#         self.objectName=objectName
#         #type: Text
#         self.class_=class_
#         #type: Class
#
# # TODO: should operation represent operation or evaluarion ?
#
# class AttributeAssignment(UpdateOperation):
#     def __init__(self,
#                  parent,
#                  objectName,
#                  attributeName,
#                  value,
#                  update=True,
#                  astNode=None, lineNo=None, description=None):
#         super(AttributeAssignment, self).__init__(
#             parent=parent,
#             astNode=astNode,
#             lineNo=lineNo,
#             description=description)
#
#
#         self.objectName=objectName
#         #type: Text
#
#         self.attributeName=attributeName
#         #type: Text
#
#         self.value=value
#         #type: 'BasicValue'
#
#         self.update=update
#         #type: 'Boolean'
#
#
# class ObjectDeletion(UpdateOperation):
#     """
#     Deletion of a regular object OR of a link object.
#     """
#     def __init__(self,
#                  parent,
#                  objectName,
#                  astNode=None, lineNo=None, description=None):
#         super(ObjectDeletion, self).__init__(
#             parent=parent,
#             astNode=astNode,
#             lineNo=lineNo,
#             description=description)
#         self.objectName=objectName
#
#
# class LinkCreation(UpdateOperation):
#     def __init__(self,
#                  parent,
#                  sourceObjectName,
#                  targetObjectName,
#                  association,
#                  astNode=None, lineNo=None, description=None):
#         super(LinkCreation, self).__init__(
#             parent=parent,
#             astNode=astNode,
#             lineNo=lineNo,
#             description=description)
#
#         self.sourceObjectName=sourceObjectName
#         #type:Text
#
#         self.targetObjectName=targetObjectName
#         #type:Text
#
#         self.association=association
#         # type: Association
#
#
# class LinkDeletion(UpdateOperation):
#     def __init__(self,
#                  parent,
#                  sourceObjectName,
#                  targetObjectName,
#                  association,
#                  astNode=None, lineNo=None, description=None):
#         super(LinkDeletion, self).__init__(
#             parent=parent,
#             astNode=astNode,
#             lineNo=lineNo,
#             description=description)
#
#         self.sourceObjectName=sourceObjectName
#         #type:Text
#
#         self.targetObjectName=targetObjectName
#         #type:Text
#
#         self.association=association
#         # type: Association
#
# # class LinkObjectCreation(UpdateOperation):
# #     def __init__(self, block,
# #                  variableName=None,
# #                  names=(),
# #                  id=None,
# #                  associationClass=None,
# #                  astNode=None, lineNo=None, description=None):
# #         super(LinkObjectCreation, self).__init__(
# #             block=block,
# #             name=variableName,
# #             astNode=astNode,
# #             lineNo=lineNo,
# #             description=description)
# #         # self.name can be None
# #         self.names = names
# #         self.id = id
# #
# #         self.associationClass = associationClass  # this is indeed an association class
# #         # type: AssociationClass
# #
#
#
#
#
# #--------------------------------------------------------------
# #   Read operations
# #--------------------------------------------------------------
#
# # class Query(ReadOperation):
# #     def __init__(self, block,
# #                  expression,
# #                  verbose=False,
# #                  code=None, lineNo=None, description=None, eolComment=None):
# #         super(Query, self).__init__(
# #             block=block,
# #             name=None,
# #             code=code,
# #             lineNo=
# #             lineNo,
# #             description=description, eolComment=eolComment)
# #
# #         self.expression = expression
# #         self.verbose = verbose
# #
# # class AssertQuery(Query):
# #     def __init__(self, block,
# #                  expression,
# #                  verbose=False,
# #                  code=None, lineNo=None, description=None, eolComment=None):
# #         super(AssertQuery, self).__init__(
# #             block=block,
# #             expression=expression,
# #             verbose=verbose,
# #             code=code, lineNo=lineNo,
# #             description=description, eolComment=eolComment)
# #
# #
# #
# class Check(ReadOperation):
#     def __init__(self,
#                  parent,
#                  astNode=None, lineNo=None, description=None):
#         super(Check, self).__init__(
#             parent=parent,
#             astNode=astNode,
#             lineNo=lineNo,
#             description=description)
