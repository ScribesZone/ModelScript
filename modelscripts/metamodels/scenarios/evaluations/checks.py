# coding=utf-8
from typing import Text, Optional
from modelscripts.megamodels.checks import Checker
from modelscripts.base.issues import (
    Levels
)

from modelscripts.metamodels.scenarios.evaluations.operations import (
    _USEImplementedAssertQueryEvaluation
)

class QueryAssertChecker(Checker):

    def __init__(self, level, params=None):
        super(QueryAssertChecker, self).__init__(
            classes=[_USEImplementedAssertQueryEvaluation ],
            name='QueryAssertChecker',
            level=level,
            params=params
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

    def __init__(self, level, params=None):
        super(InvariantViolationChecker, self).__init__(
            classes=[InvariantViolation ],
            name='InvariantViolationChecker',
            level=level,
            params=params
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

    def __init__(self, level, params=None):
        super(CardinalityViolationCheckerObject, self).__init__(
            classes=[CardinalityViolationObject],
            name='CardinalityViolationCheckerObject',
            level=level,
            params=params
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
