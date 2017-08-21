# coding=utf-8

"""
Meta elements for modeling results of a scenario evaluation.

The structure of the metamodel is::

    ScenarioEvaluation
    <>-- CheckEvaluation   (soil command "check")
        <>-- CardinalityEvaluation
             <|-- CardinalityViolation
        <>-- InvariantEvaluation
             <|-- InvariantValidation
             <|-- InvariantViolation
    <>-- QueryEvaluation   (soil command "??")
"""
from __future__ import print_function, division
from typing import Text, List, Dict, Optional
from collections import OrderedDict
from abc import ABCMeta
from modelscripts.metamodels.classes.expressions import Invariant

from modelscripts.metamodels.classes import Role
from modelscripts.metamodels.scenarios import ScenarioModel
from modelscripts.metamodels.scenarios.operations import (
    Check,
    Query,
)



# TODO: Change comment, remove dead code, etc.
#       This should lead to a general metamodel (conformance ?)


"""
Model the result of the evaluation of a USE OCL state (a soil file) against
a USE OCL model. This module represents the output of the evaluation
while the module 'evaluator' actually perform the computation from
a state (a '.soil') and a model (a '.use')) using a ``check`` command.
Simply put this module represents the information contained in the output of
this command which might look like::

        checking invariant (NUM) `CLASS::INVARIANT': OK.

        checking invariant (NUM) `CLASS::INVARIANT': FAILED.
          -> false : Boolean
        Instances of CLASS violating the invariant:
          -> Set{@bedroom201,@bedroom202, ...} : Set(Bedroom)

The evaluation is modeled at two levels of granularity.

- At the *model* level there are 3 classes:

    - 'ScenarioEvaluation' is the top-level result. This is an abstract class.
    - 'ClassModelValidation' is a 'ScenarioEvaluation' representing the fact that *ALL*
      invariants have been validated.
    - 'ClassModelViolation' is a 'ScenarioEvaluation' representing the fact that at
      least one invariant has not been validated.

- At the *feature* level (e.g. 'invariant' or a 'cardinality') there are
  also 3 classes:

    - 'InvariantEvaluation' is an abstract class representing the outcome of
      the evaluation of an invariant against a state.
    - 'InvariantValidation' is a 'InvariantEvaluation' representing the fact
      that the invariant has been validated.
    - 'InvariantViolation' is a 'InvariantEvaluation' representing the fact
      that the invariant has been violated.
    - 'CardinalityViolation' represents the fact that a cardinality has been
      violated.

      XXX

All these objects are created by the module 'evaluator'.
"""



#------------------------------------------------------------------------------
#   Class Model level
#------------------------------------------------------------------------------


class ScenarioEvaluation(object):
    """
    Result of the evaluation of a scenario in the context of
    a class model. Contains results of the evaluation::

    * query results
    * invariant results
    * cardinality results

    """


    def __init__(self, scenario):
        #type: (ScenarioModel) -> None
        self.scenario = scenario  #type: ScenarioModel

        self.checkEvaluations = []
        #type: List[CheckEvaluation]

        self.queryEvaluations = []
        #type: List[QueryEvaluation]


    # def getInvariantEvaluation(self,
    #                            classOrAssociationClassName, invariantName):
    #     inv = self.model.findInvariant(
    #             classOrAssociationClassName, invariantName )
    #     return self.invariantEvaluations[inv]
    #
    #
    #







#------------------------------------------------------------------------------
#   Check evaluation
#------------------------------------------------------------------------------



class CheckEvaluation(object):

    def __init__(self, scenarioEvaluation, check):
        #type: (ScenarioEvaluation, Check) -> None
        self.check=check
        self.check.checkEvaluation=self

        self.scenarioEvaluation=scenarioEvaluation
        self.scenarioEvaluation.checkEvaluations.append(self)

        self.invariantEvaluations=OrderedDict()
        #type:Dict[Invariant,InvariantEvaluation]


        self.cardinalityEvaluations = OrderedDict()
        # type:Dict[Role,CardinalityEvaluation]





#------------------------------------------------------------------------------
#   Invariant evaluation
#------------------------------------------------------------------------------



class InvariantEvaluation(object):
    """
    Result of the evaluation of an invariant.
    This is an abstract class.
    """
    __metaclass__ = ABCMeta

    def __init__(self,
                 checkEvaluation,
                 invariant,
                 result=True):
        #type: (CheckEvaluation, Invariant, bool) -> None
        self.checkEvaluation = checkEvaluation
        self.invariant = invariant
        self.checkEvaluation.invariantEvaluations[invariant] = self
        self.result = result #type: bool



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

class CardinalityEvaluation(object):
    """
    Result of a cardinality evaluation.
    This is an abstract class.
    In the case of USE OCL only cardinality violations are described
    so there is so far only one subclass.
    """
    __metaclass__ = ABCMeta

    def __init__(self, checkEvaluation, role):
        #type: (CheckEvaluation, Role) -> None

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
    def __init__(self, checkEvaluation, role):
        #type: (CheckEvaluation, Role) -> None
        super(CardinalityViolation, self).__init__(checkEvaluation, role)

        self.role=role
        assert(role not in self.checkEvaluation.cardinalityEvaluations)
        self.checkEvaluation.cardinalityEvaluations[role]=self
        self.violatingObjects=[]

class CardinalityViolationObject(object):

    def __init__(self, cardinalityViolation, violatingObject, actualCardinality):
        #type: (CardinalityViolation, Text, int) -> None

        self.cardinalityViolation=cardinalityViolation
        self.cardinalityViolation.violatingObjects.append(self)

        self.violatingObject=violatingObject #type: Text
        self.actualCardinality=actualCardinality #type: int



#------------------------------------------------------------------------------
#   Query evaluation
#------------------------------------------------------------------------------


class QueryEvaluation(object):
    """
    Result of the evaluation of a query.
    """
    def __init__(self, scenarioEvaluation, query, resultValue='', resultType='', subexpressions=()):
        #type: (ScenarioEvaluation, Query, Text, Text, List[Text]) -> None
        self.query=query
        self.query.queryEvaluation=self

        self.scenarioEvaluation=scenarioEvaluation
        self.scenarioEvaluation.queryEvaluations.append(self)
        self.resultValue=resultValue  # Filled later
        self.resultType=resultType # Filled later
        self.subexpressions=list(subexpressions)






# class ScenarioEvaluation(object):
#     """
#     Result of the evaluation of a USE OCL state against a USE OCL model.
#     This is an abstract class. In practice this could either be a
#     ClassModelValidation if the state is valid, that is there is absolutely
#     no errors. If there is at least one error, then this will be
#     a ClassModelViolation.
#     A ScenarioEvaluation contains a map of InvariantEvaluation as well
#     as a map of CardinalityEvaluation.
#     """
#     __metaclass__ = ABCMeta
#
#
#     def __init__(self, model, state = None):
#         self.model = model
#         self.state = state
#
#         """ str """
#         self.stateShortName = os.path.splitext(os.path.basename(self.state))[0]
#         self.isValidated = None  # abstract attribute. Filled by subclasses.
#
#         self.invariantEvaluations = OrderedDict()
#         """ dict[Invariant, InvariantEvaluation] """
#
#         self.cardinalityViolations = OrderedDict()
#         """ dict[Role, list[CardinalityViolation] ] """
#
#
#     def getInvariantEvaluation(self,
#                                classOrAssociationClassName, invariantName):
#         inv = self.model.findInvariant(
#                 classOrAssociationClassName, invariantName )
#         return self.invariantEvaluations[inv]
#
#
# class ClassModelValidation(ScenarioEvaluation):
#     """
#     Result of the positive evaluation of a USE OCL state against a USE OCL
#     model. Nothing particular to be stored as there is no error.
#     """
#
#     def __init__(self, model, state):
#         ScenarioEvaluation.__init__(self, model, state)
#         self.isValidated = True
#
#
#     def __str__(self):
#         return 'Model validated'
#
#     def __repr__(self):
#         return 'Valid(%s)' % self.stateShortName
#
#
# class ClassModelViolation(ScenarioEvaluation):
#     """
#     Result of the negative evaluation of a USE OCL state against a USE OCL
#     model. Store invariants violations and/or cardinality violations.
#     """
#
#     def __init__(self, model, state):
#         ScenarioEvaluation.__init__(self, model, state)
#         self.isValidated = True
#
#
#     def __repr__(self):
#         return 'Violation(%s,INV(%s),ROLE(%s))' % (
#             self.stateShortName,
#             ','.join(map(str, self.invariantEvaluations.values())),
#             ','.join(map(str, self.cardinalityViolations.keys())))
#
