# coding=utf-8

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

    - 'ModelEvaluation' is the top-level result. This is an abstract class.
    - 'ModelValidation' is a 'ModelEvaluation' representing the fact that *ALL*
      invariants have been validated.
    - 'ModelViolation' is a 'ModelEvaluation' representing the fact that at
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

All these objects are created by the module 'evaluator'.
"""

from collections import OrderedDict
from abc import ABCMeta
import os.path



#------------------------------------------------------------------------------
#   Model level
#------------------------------------------------------------------------------

class ModelEvaluation(object):
    """
    Result of the evaluation of a USE OCL state against a USE OCL model.
    This is an abstract class. In practice this could either be a
    ModelValidation if the state is valid, that is there is absolutely
    no errors. If there is at least one error, then this will be
    a ModelViolation.
    A ModelEvaluation contains a map of InvariantEvaluation as well
    as a map of CardinalityEvaluation.
    """
    __metaclass__ = ABCMeta


    def __init__(self, model, state = None):
        self.model = model
        self.state = state

        """ str """
        self.stateShortName = os.path.splitext(os.path.basename(self.state))[0]
        self.isValidated = None  # abstract attribute. Filled by subclasses.

        self.invariantEvaluations = OrderedDict()
        """ dict[Invariant, InvariantEvaluation] """

        self.cardinalityViolations = OrderedDict()
        """ dict[Role, list[CardinalityViolation] ] """


    def getInvariantEvaluation(self,
                               classOrAssociationClassName, invariantName):
        inv = self.model.findInvariant(
                classOrAssociationClassName, invariantName )
        return self.invariantEvaluations[inv]


class ModelValidation(ModelEvaluation):
    """
    Result of the positive evaluation of a USE OCL state against a USE OCL
    model. Nothing particular to be stored as there is no error.
    """

    def __init__(self, model, state):
        ModelEvaluation.__init__(self, model, state)
        self.isValidated = True


    def __str__(self):
        return 'Model validated'

    def __repr__(self):
        return 'Valid(%s)' % self.stateShortName


class ModelViolation(ModelEvaluation):
    """
    Result of the negative evaluation of a USE OCL state against a USE OCL
    model. Store invariants violations and/or cardinality violations.
    """

    def __init__(self, model, state):
        ModelEvaluation.__init__(self, model, state)
        self.isValidated = True


    def __repr__(self):
        return 'Violation(%s,INV(%s),ROLE(%s))' % (
            self.stateShortName,
            ','.join(map(str, self.invariantEvaluations.values())),
            ','.join(map(str, self.cardinalityViolations.keys())))



#------------------------------------------------------------------------------
#   Invariant and Cardinality level
#------------------------------------------------------------------------------

class InvariantEvaluation(object):
    """ Result of the evaluation of an invariant. This is an abstract class.
    """
    __metaclass__ = ABCMeta

    def __init__(self, modelEvaluation, invariant):
        self.modelEvaluation = modelEvaluation
        self.invariant = invariant
        self.modelEvaluation.invariantEvaluations[invariant] = self
        self.isOK = None # set in subclasses. A bool.



class InvariantValidation(InvariantEvaluation):
    """
    Invariant validation.

    Looks like this in USE OCL::

        checking invariant (NUM) `CLASS::INVARIANT': OK.
    """

    def __init__(self, modelEvaluation, invariant):
        InvariantEvaluation.__init__(self, modelEvaluation, invariant)
        self.isOK = True


    def __repr__(self):
        return '%s=OK'% self.invariant.name



class InvariantViolation(InvariantEvaluation):
    """
    Invariant violation.

    Looks like this in USE OCL::

        checking invariant (NUM) `CLASS::INVARIANT': FAILED.
          -> false : Boolean
        Instances of CLASS violating the invariant:
          -> Set{@bedroom201,@bedroom202, ...} : Set(Bedroom)
    """
    def __init__(self, modelViolation, invariant, violatingObjects):
        InvariantEvaluation.__init__(self, modelViolation, invariant)
        self.violatingObjects = violatingObjects
        self.isOK = False


    def __repr__(self):
        return '%s=KO' % self.invariant.name



class CardinalityViolation(object):
    """
    Cardinality violation.

    Looks like this in USE OCL::

        Multiplicity constraint violation in association `ASSOC':
          Object `OBJECT' of class `CLASS' is connected to NUM objects of class `CLASS'
          at association end `END' but the multiplicity is specified as `NUM'.
    """
    def __init__(self, modelViolation, role,
                 violatingObject, cardinalityFound):
        self.modelViolation = modelViolation
        if role not in modelViolation.cardinalityViolations:
            modelViolation.cardinalityViolations[role] = []
        modelViolation.cardinalityViolations[role].append(self)

        self.role = role
        self.violatingObject = violatingObject
        self.cardinalityFound = cardinalityFound


del ABCMeta, OrderedDict