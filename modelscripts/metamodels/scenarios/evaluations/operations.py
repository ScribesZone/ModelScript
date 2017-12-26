# coding=utf-8
"""
Meta elements for modeling the evaluation of operations
"""
from abc import ABCMeta, abstractmethod
from collections import OrderedDict

from typing import Dict, Text, List, Optional

from modelscripts.megamodels.models import (
    ModelElement
)
from modelscripts.metamodels.classes import (
    Class,
    Association,
    AssociationClass,
    Role,
    Attribute,
)
from modelscripts.metamodels.classes.expressions import (
    Invariant
)
from modelscripts.metamodels.objects import (
    Object,
    Link,
    LinkObject,
    Slot
)
from modelscripts.metamodels.permissions import (
    CreateAction,
    # ReadAction,
    UpdateAction,
    DeleteAction,
    # ExecuteAction,
)
from modelscripts.metamodels.permissions.accesses import Access
from modelscripts.metamodels.permissions.sar import Subject
from modelscripts.metamodels.scenarios.operations import (
    Operation,
    ObjectCreation,
    ObjectDestruction,
    LinkCreation,
    LinkDestruction,
    LinkObjectCreation,
    AttributeAssignment,
    Query,
    AssertQuery,
    Check,
)

META_CLASSES=[
    'OperationEvaluation',
    'UpdateOperationEvaluation',
    'ObjectCreationEvaluation',
    'ObjectDestructionEvaluation',
    'LinkCreationEvaluation',
    'LinkDestructionEvaluation',
    'LinkObjectCreationEvaluation',
    'AttributeAssignmentEvaluation',
    'ReadOperationEvaluation',
    'CheckEvaluation',
    'InvariantEvaluation',
    'InvariantValidation',
    'InvariantViolation',
    'CardinalityEvaluation',
    'CardinalityViolation',
    'CardinalityViolationObject',
    'QueryEvaluation',
    'AssertQueryEvaluation'
]

__all__=(
    META_CLASSES+[
        'evaluateOperation',
    ]
)

def evaluateOperation(blockEvaluation, op):
    #type: ('BlockEvaluation', Operation) -> OperationEvaluation
    """
    Reuse or create an evaluation for the operation 'op'.
    Connect it to 'op' and blockEvaluation.
    If op.operationEvaluation already exists then
    reuses it as the evaluation is already there.
    This is the case for Queries and Check.
    """
    if op.operationEvaluation is not None:
        e=op.operationEvaluation
        # The operation evaluation is reused but make sure
        # it is connected to the BlockEvaluation
        # given as a parameter
        e.blockEvaluation = blockEvaluation
    else:
        if isinstance(op, ObjectCreation):
            e=ObjectCreationEvaluation(blockEvaluation, op)
        elif isinstance(op, ObjectDestruction):
            e=ObjectDestructionEvaluation(blockEvaluation, op)
        elif isinstance(op, LinkCreation):
            e=LinkCreationEvaluation(blockEvaluation, op)
        elif isinstance(op, LinkObjectCreation):
            e=LinkObjectCreationEvaluation(blockEvaluation, op)
        elif isinstance(op, AttributeAssignment):
            e=AttributeAssignmentEvaluation(blockEvaluation, op)
        elif isinstance(op, Query):
            return _NotImplementedQueryEvaluation(blockEvaluation, op)
        elif isinstance(op, Check):
            return _NotImplementedCheckEvaluation(blockEvaluation, op)
        else:
            raise NotImplementedError()
    # make sure that the block evaluation is correct
    # in case it as not
    return e

#--------------------------------------------------------------
#   Abstract classes
#--------------------------------------------------------------

class OperationEvaluation(ModelElement, Subject):
    __metaclass__ = ABCMeta

    def __init__(self, blockEvaluation, op):
        # type: (Optional['BlockEvaluation'], Operation) -> OperationEvaluation
        """
        Abstract constructor to create a operation evaluation.
        It connects the operation evaluation to the block
        evaluation if specified. If not the block evaluation
        will be connected later. This is the case for
        Queries and Checks.
        Args:
            blockEvaluation:
            op:
        """
        self.blockEvaluation=blockEvaluation
        self.operation=op
        self.operation.operationEvaluation=self
        ModelElement.__init__(self, model=op.model)

        self.accesses=[] #type: Optional[List[Access]]
        # an operation can generate 0 or many access


    @abstractmethod
    def _eval(self):
        pass

    # @abstractmethod
    # def check(self):
    #     pass

    def _env(self):
        # convenience method
        return self.blockEvaluation._env()

    def _state(self):
        # convenience method
        return self.blockEvaluation._state()

    @property
    def _accessSet(self):
        # convenience method
        return self.blockEvaluation.accessSet

    @property
    def model(self):
        return self.operation.model



#################################################################
#  Update operations
#################################################################


class UpdateOperationEvaluation(OperationEvaluation):
    __metaclass__ = ABCMeta


    def __init__(self, blockEvaluation, op):
        super(UpdateOperationEvaluation, self).__init__(
            blockEvaluation, op)


class ObjectCreationEvaluation(UpdateOperationEvaluation):
    def __init__(self, blockEvaluation, op):
        #type: ('BlockEvaluation', ObjectCreation) -> None
        super(ObjectCreationEvaluation, self).__init__(
            blockEvaluation, op)

        self.createdObject=None  #type: Optional[Object]
        # filled by eval

        self.class_=op.class_  #type: Class

        self._eval()

    def _eval(self):
        op=self.operation #type: ObjectCreation
        self.createdObject=Object(
            self._state(),
            op.class_,
            name=op.name)
        self._env()[op.name]=self.createdObject
        self.accesses=[
            Access(
                op,
                CreateAction,
                self.class_,
                self._accessSet)]


class ObjectDestructionEvaluation(UpdateOperationEvaluation):
    """
    Destruction of a regular object OR of a link object.
    """
    def __init__(self, blockEvaluation, op,):
        #type: ('BlockEvaluation', ObjectDestruction) -> None
        super(ObjectDestructionEvaluation, self).__init__(
            blockEvaluation, op)

        #TODO: check why here we useclassifier while class_ for create
        self.classifier=None #type: Optional[Class]
        # filled by _eval

        self.deletedObject=None # filled by _eval
        self._eval()

    def _eval(self):
        # this can be the destruction of a regular object or of a link object
        op=self.operation #type: ObjectDestruction
        name=op.name
        self.deletedObject=self._env()[name] # TODO raise error if not defined
        self.classifier=self.deletedObject.classifier
        self.accesses=[
            Access(
                op,
                DeleteAction,
                self.classifier,
                self._accessSet)]
        self.deletedObject.delete()  # TODO: check what to do with obj/linkobj if there are links
        del self._env()[name]


class LinkCreationEvaluation(UpdateOperationEvaluation):
    def __init__(self, blockEvaluation, op):
        #type: ('BlockEvaluation', LinkCreation) -> None

        super(LinkCreationEvaluation, self).__init__(
            blockEvaluation, op
        )
        self.linkCreated=None #type: Optional[Link]
        #  filled by _eval

        self.linkedObjects=[] #type: List[Object]
        # filled by _eval

        self.association=op.association #type: Association

        self._eval()

    def _eval(self):
        op=self.operation #type: LinkCreation
        self.accesses=[
            Access(
                op,
                CreateAction,
                self.association,
                self._accessSet)]

        # TODO: raise errors if enough objects found
        self.linkedObjects=[self._env()[n] for n in op.names]
        self.linkCreated=Link(
            self._state(), op.association, self.linkedObjects)


class LinkDestructionEvaluation(UpdateOperationEvaluation):
    def __init__(self, blockEvaluation, op):
        #type: ('BlockEvaluation', LinkDestruction) -> None
        super(LinkDestructionEvaluation, self).__init__(
            blockEvaluation, op
        )
        self.deletedLink=None # filled by _eval

        self.association=op.association #type: Association

        self._eval()

    def _eval(self):
        op=self.operation #type: LinkDestruction
        self.accesses=[
            Access(
            op,
            DeleteAction,
            self.association,
            self._accessSet)]

    # def check(self):
    #     Issue()

        raise NotImplementedError()  # TODO: implement link destruction


class LinkObjectCreationEvaluation(UpdateOperationEvaluation):
    def __init__(self, blockEvaluation, op):
        #type: ('BlockEvaluation', LinkObjectCreation) -> None
        super(LinkObjectCreationEvaluation, self).__init__(
            blockEvaluation, op
        )
        self.linkedObjects=None #type: Optional[Link]
        # filled by _eval

        self.linkObjectCreated=None #type: Optional[LinkObject]
        # filled by _eval

        self.associationClass=op.associationClass #type: AssociationClass

        self._eval()

    def _eval(self):
        op=self.operation #type: LinkObjectCreation
        self.accesses=[
            Access(
                op,
                CreateAction,
                op.associationClass,
                self._accessSet)]
        # TODO: raise errors if enough objects found
        self.linkedObjects=[
            self._env()[n] for n in op.names]
        self.linkObjectCreated=LinkObject(
            self._state(),
            op.associationClass,
            self.linkedObjects,
            name=self.operation.name)
        self._env()[self.linkObjectCreated.name]=self.linkObjectCreated


class AttributeAssignmentEvaluation(UpdateOperationEvaluation):
    def __init__(self, blockEvaluation, op):
        #type: ('BlockEvaluation', AttributeAssignment) -> None
        super(AttributeAssignmentEvaluation, self).__init__(
            blockEvaluation, op)

        self.object=None #type: Optional[Object]
        #  filled by _eval

        self.attribute=None #type: Optional[Attribute]
        # filled by _eval

        self.slot=None #type: Optional[Slot]

        self._eval()

    def _eval(self):
        op=self.operation #type: AttributeAssignment
        if op.variableName not in self._env():
            raise ValueError(
                'Execution error %s: variable "%s" is undefined' % (
                    'at %i' % self.operation.lineNo
                            if self.operation.lineNo else '',
                    op.variableName
                ))
        self.object = self._env()[op.variableName]
        # self.object.slotNamed[op.attributeName]=(
        #     op.expression)

        c=self.object.classifier
        #FIXME: add support for inheritance
        self.attribute=c.attributeNamed[op.attributeName]
        self.object.assign(
            object=self.object,
            attribute=self.attribute,
            value=op.expression
        )
        self.accesses=[
            Access(
                op,
                UpdateAction,
                self.attribute,
                self._accessSet)]



#################################################################
# Read operations
##################################################################

class ReadOperationEvaluation(OperationEvaluation):
    __metaclass__ = ABCMeta

    def __init__(self, blockEvaluation, op):
        super(ReadOperationEvaluation, self).__init__(
            blockEvaluation, op)



#=================================================================
#   Check evaluation
#=================================================================

class CheckEvaluation(ReadOperationEvaluation):
    __metaclass__ = ABCMeta

    META_COMPOSITIONS=[
        'invariantEvaluations',
        'cardinalityEvaluations',
    ]

    @abstractmethod
    def __init__(self,
                 blockEvaluation,
                 op):
        #type: (Optional['BlockEvaluation'], Check) -> None
        super(CheckEvaluation, self).__init__(
            blockEvaluation, op
        )

        self.isNotImplemented=True

        self.invariantEvaluationByInvariant=OrderedDict()
        #type:Dict[Invariant,InvariantEvaluation]

        self.cardinalityEvaluationByRole = OrderedDict()
        # type:Dict[Role,CardinalityEvaluation]
        self._eval()

    @property
    def invariantEvaluations(self):
        return self.invariantEvaluationByInvariant.values()

    @property
    def cardinalityEvaluations(self):
        return self.cardinalityEvaluationByRole.values()

    def _eval(self):
        self.accesses = []

class _NotImplementedCheckEvaluation(CheckEvaluation):

    def __init__(self,
                 blockEvaluation,
                 op):
        #type: ('BlockEvaluation', Check) -> None
        super(_NotImplementedCheckEvaluation, self).__init__(blockEvaluation, op)
        self.isNotImplemented=True
        self._eval()

    def _eval(self):
        # Do nothing as USE parsing is already filling
        # the different fields
        self.accesses = []

class _USEImplementedCheckEvaluation(CheckEvaluation):
    def __init__(self,
                 blockEvaluation,
                 op):
        #type: (Optional['BlockEvaluation'], Check) -> None
        super(_USEImplementedCheckEvaluation, self).__init__(blockEvaluation, op)
        self.isNotImplemented=False
        self.accesses = []
        self._eval()

    def _eval(self):
        # Do nothing as USE parsing is already filling
        # the different fields
        self.accesses = []


# class _CheckEvaluationProxy(object):
#     def __init__(self, block,
#                  verbose=False,
#                  showFaultyObjects=False,
#                  checkEvaluation=None,
#                  all=True,
#                  code=None, lineNo=None, docComment=None, eolComment=None):
#         super(_CheckEvaluationProxy, self).__init__(block, None, code, lineNo, docComment, eolComment)
#
#         self.verbose = verbose
#         self.showFaultyObjects = showFaultyObjects
#         self.all=all
#
#         self.checkEvaluation=checkEvaluation
#         # Filled if the scenario is evaluated


#------------------------------------------------------------------------------
#   Invariant evaluation
#------------------------------------------------------------------------------

class InvariantEvaluation(ModelElement):
    """
    Abstract class representing the result of the evaluation
    of an invariant.
   """
    __metaclass__ = ABCMeta

    def __init__(self,
                 checkEvaluation,
                 invariant,
                 result=True):
        #type: (CheckEvaluation, Invariant, bool) -> None
        ModelElement.__init__(self, invariant.model)
        self.checkEvaluation = checkEvaluation
        self.invariant = invariant
        self.checkEvaluation.invariantEvaluationByInvariant[invariant] = self
        self.result = result #type: bool
        self._eval()

    def _eval(self):
        # currently we have no mean to extract ReadAction
        self.accesses = []


class InvariantValidation(InvariantEvaluation):
    """
    Evaluation of invariant returning True.

    For instance, it looks like this in USE OCL in syntax::

        checking invariant (NUM) `CLASS::INVARIANT': OK.
    """

    def __init__(self,
                 checkEvaluation,
                 invariant):
        #type: (CheckEvaluation, Invariant) -> None
        InvariantEvaluation.__init__(self,
                                     checkEvaluation,
                                     invariant,
                                     True)

    def __repr__(self):
        return '%s=True'% self.invariant.name


class InvariantViolation(InvariantEvaluation):
    """
    Evaluation of invariant returning False + detail about
    the violation.

    For instance, it looks like this in USE OCL syntax::

        checking invariant (NUM) `CLASS::INVARIANT': FAILED.
          -> false : Boolean
        Instances of CLASS violating the invariant:
          -> Set{@bedroom201,@bedroom202, ...} : Set(Bedroom)
    """
    def __init__(self,
                 checkEvaluation,
                 invariant,
                 resultValue='false',
                 resultType='Boolean',
                 violatingObjects=(),
                 violatingObjectType='',
                 subexpressions=()):
        #type: (CheckEvaluation, Invariant, Text, Text, List[Text], Text, List[Text]) -> None
        InvariantEvaluation.__init__(self, checkEvaluation, invariant, False)
        # the attributes below can be filled incrementally
        self.violatingObjects=violatingObjects # List[Text]
        self.violatingObjectType=violatingObjectType # Text
        self.resultValue=resultValue # Text
        self.resultType=resultType # Text
        self.subexpressions=list(subexpressions)  # List[Text]

    def __repr__(self):
        return '%s=False' % self.invariant.name



#------------------------------------------------------------------------------
#   Cardinality evaluation
#------------------------------------------------------------------------------


class CardinalityEvaluation(ModelElement):
    """
    Result of a cardinality evaluation.
    This is an abstract class.
    In the case of USE OCL only cardinality violations are described
    so there is so far only one subclass.
    """
    __metaclass__ = ABCMeta

    def __init__(self, checkEvaluation, role):
        #type: (CheckEvaluation, Role) -> None

        ModelElement.__init__(self, model=role.model)

        self.checkEvaluation=checkEvaluation
        #type: CheckEvaluation

        # in fact an association class is an association
        self.role=role   # could be None but filled later


class CardinalityViolation(CardinalityEvaluation):
    """
    Cardinality violation for a given role. Various objects can
    violate the cardinality. These objects are represented by
    a CardinalityViolationObjects

    Looks like this in USE OCL::

        Multiplicity constraint violation in association `ASSOC':
          Object `OBJECT' of class `CLASS' is connected to NUM objects of class `CLASS'
          at association end `END' but the multiplicity is specified as `NUM'.
    """
    META_COMPOSITIONS=[
        'violatingObjects',
    ]
    def __init__(self, checkEvaluation, role):
        #type: (CheckEvaluation, Role) -> None
        super(CardinalityViolation, self).__init__(checkEvaluation, role)

        self.role=role
        assert(role not in self.checkEvaluation.cardinalityEvaluationByRole)
        self.checkEvaluation.cardinalityEvaluationByRole[role]=self
        self.violatingObjects=[]


class CardinalityViolationObject(ModelElement):

    def __init__(self,
                 cardinalityViolation,
                 violatingObject,
                 actualCardinality):
        #type: (CardinalityViolation, Text, int) -> None

        ModelElement.__init__(self,
                              cardinalityViolation.model)

        self.cardinalityViolation=cardinalityViolation
        self.cardinalityViolation.violatingObjects.append(self)

        self.violatingObject=violatingObject #type: Text
        self.actualCardinality=actualCardinality #type: int



#=================================================================
#  Query evaluation
#=================================================================


class QueryEvaluation(ReadOperationEvaluation):
    """
    Result of the evaluation of a query.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self,
                 blockEvaluation,
                 op):
        #type: (Optional['BlockEvaluation'], Query) -> None
        super(QueryEvaluation,self).__init__(blockEvaluation, op)

        self.isNotImplemented=True #type: bool

        self.resultValue=None #type: Optional[Text]
        #defined if implemented

        self.resultType=None #type: Optional[Text]
        #defined if implemented

        self.subexpressions=[] #type: Optional[List[Text]]
        #defined if implemented

        self.accesses = []


class AssertQueryEvaluation(QueryEvaluation):
    """
    Result of AssertQuery evaluation.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self,
                 blockEvaluation,
                 op):
        #type: (Optional['BlockEvaluation'], AssertQuery) -> None
        QueryEvaluation.__init__(self, blockEvaluation, op)

    @property
    def status(self):
        if self.resultType!='Boolean':
            return 'Failure'
        elif self.resultValue=='false':
            return 'KO'
        elif self.resultValue=='true':
            return 'OK'
        else:
            raise NotImplementedError(
                'Unexpected value from evaluation: %s' %
                self.resultValue)


class _NotImplementedQueryEvaluation(QueryEvaluation):
    def __init__(self,
                 blockEvaluation,
                 op):
        #type: ('BlockEvaluation', Query) -> None
        super(_NotImplementedQueryEvaluation,self).__init__(blockEvaluation, op)
        self.isNotImplemented=True

    def _eval(self):
        # Nothing can be done
        pass


class _USEImplementedQueryEvaluation(QueryEvaluation):
    def __init__(self,
                 blockEvaluation,
                 op):
        #type: (Optional['BlockEvaluation'], Query) -> None
        super(_USEImplementedQueryEvaluation,self).__init__(blockEvaluation, op)
        self.isNotImplemented=False

    def _eval(self):
        # Do nothing as USE parsing is already filling
        # the different fields
        pass


class _USEImplementedAssertQueryEvaluation(AssertQueryEvaluation):
    def __init__(self,
                 blockEvaluation,
                 op):
        # type: (Optional['BlockEvaluation'], AssertQuery) -> None
        super(_USEImplementedAssertQueryEvaluation, self).__init__(blockEvaluation, op)
        self.isNotImplemented = False

    def _eval(self):
        # Do nothing as USE parsing is already filling
        # the different fields
        pass



# # This implementation comes from regulat operation evaluation
#
# class QueryEvaluationProxy(ReadOperationEvaluation):
#     def __init__(self, block,
#                  expression,
#                  verbose=False,
#                  queryEvaluation=None,
#                  code=None, lineNo=None, docComment=None, eolComment=None):
#         super(Query, self).__init__(block, None, code, lineNo, docComment, eolComment)
#
#         self.expression = expression
#         self.verbose = verbose
#
#         self.queryEvaluation = queryEvaluation
#         # Filled if the scenario is evaluated
