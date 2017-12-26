# coding=utf-8
from typing import Text, Optional
from modelscripts.megamodels.checkers import Checker
from modelscripts.base.issues import (
    Levels
)

from modelscripts.metamodels.scenarios.evaluations.operations import (
    _USEImplementedAssertQueryEvaluation
)

class QueryAssertChecker(Checker):

    def __init__(self,**params):
        super(QueryAssertChecker, self).__init__(
            metaclasses=[_USEImplementedAssertQueryEvaluation],
            **params
        )


    def doCheck(self, e):
        #type: ('_USEImplementedAssertQueryEvaluation') -> Optional[Text]
        if e.status != 'OK':
            return (
                'Assert is %s (%s : %s)' % (
                    e.status,
                    e.resultValue,
                    e.resultType
            ))
        else:
            return None

QueryAssertChecker(
    level=Levels.Error
)


#-------------------------------------------------------------
from modelscripts.metamodels.scenarios.evaluations.operations import (
    InvariantViolation
)

class InvariantViolationChecker(Checker):

    def __init__(self, **params):
        super(InvariantViolationChecker, self).__init__(
            metaclasses=[InvariantViolation ],
            **params
        )


    def doCheck(self, iv):
        #type: ('InvariantViolation') -> Optional[Text]
            return (
                'Invariant %s is violated' % (
                    iv.invariant.invariantLabel,
            ))

InvariantViolationChecker(
    level=Levels.Error
)

#-------------------------------------------------------------

from modelscripts.metamodels.scenarios.evaluations.operations import (
    CardinalityViolationObject
)

class CardinalityViolationCheckerObject(Checker):

    def __init__(self, **params):
        super(CardinalityViolationCheckerObject, self).__init__(
            metaclasses=[CardinalityViolationObject],
            **params
        )


    def doCheck(self, vo):
        #type: ('CardinalityViolationObject') -> Optional[Text]
            r=vo.cardinalityViolation.role
            return (
                'Cardinality of role %s.%s[%s]  is violated' % (
                    r.association.name,
                    r.name,
                    r.cardinalityLabel
            ))

CardinalityViolationCheckerObject(
    level=Levels.Error
)
