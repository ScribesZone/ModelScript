# coding=utf-8
from typing import Text, Optional
from modelscripts.megamodels.checkers import (
    Checker,
    CheckOutput
)
from modelscripts.base.issues import (
    Levels
)

from modelscripts.metamodels.scenarios.evaluations.operations import (
    _USEImplementedQueryEvaluation
)

class QueryEvaluationChecker(Checker):

    def __init__(self,**params):
        super(QueryEvaluationChecker, self).__init__(
            metaclasses=[_USEImplementedQueryEvaluation],
            **params
        )


    def doCheck(self, qe):
        #type: ('_USEImplementedQueryEvaluation') -> Optional[CheckOutput]
        lines=['Query returns %s : %s' % (
                        qe.resultValue,
                        qe.resultType)]
        if qe.operation.verbose:
            lines.append('Details of query evaluation')
            lines.extend(['    '+se for se in qe.subexpressions])
        return CheckOutput(
            message='\n'.join(lines),
            locationElement=qe.operation)

QueryEvaluationChecker(
    level=Levels.Info
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
        #type: ('_USEImplementedAssertQueryEvaluation') -> Optional[CheckOutput]
        if e.status != 'OK':
            lines=['Assert is %s (returns %s : %s)' % (
                        e.status,
                        e.resultValue,
                        e.resultType)]
            lines.append('Details of assert evaluation')
            lines.extend(['    '+se for se in e.subexpressions])
            return CheckOutput(
                message='\n'.join(lines),
                locationElement=e.operation)

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
        #type: ('InvariantViolation') -> Optional[CheckOutput]
        lines=[
            'Invariant %s returns %s %s' % (
                iv.invariant.invariantLabel,
                iv.resultValue,
                ': '+iv.resultType if iv.resultType!="Boolean" else '' )]
        for vo in iv.violatingObjects:
            lines.append(
                '    object "%s" violates the invariant.' % (
                    vo
                ))
        lines.append('Detailled evaluation of the invariant.')
        for e in iv.subexpressions:
            lines.append('    '+e)
        return CheckOutput(
            message='\n'.join(lines))

InvariantViolationChecker(
    level=Levels.Error
)

#-------------------------------------------------------------

from modelscripts.metamodels.scenarios.evaluations.operations import (
    CardinalityViolation
)

class CardinalityViolationChecker(Checker):

    def __init__(self, **params):
        super(CardinalityViolationChecker, self).__init__(
            metaclasses=[CardinalityViolation],
            **params
        )


    def doCheck(self, v):
        #type: ('CardinalityViolation') -> Optional[CheckOutput]
        r=v.role
        lines=[
            'Cardinality of role %s.%s[%s] is violated:' % (
                r.association.name,
                r.name,
                r.cardinalityLabel
        )]
        for vo in v.violatingObjects:
            lines.append(
            '    object "%s" has %i "%s"' % (
                vo.violatingObject,
                vo.actualCardinality,
                r.name
            ))
        return CheckOutput(
            message='\n'.join(lines))

CardinalityViolationChecker(
    level=Levels.Error
)
