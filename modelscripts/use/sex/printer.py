# coding=utf-8


__all__ = [
    'SexPrinter', 'SoilPrinter'
]


import logging

from typing import Union, Text

from modelscripts.metamodels.scenarios import (
    ScenarioModel,
    operations,
    blocks
)
from modelscripts.metamodels.scenarios.evaluations import (
    ScenarioEvaluation,
    CardinalityViolation,
    InvariantValidation,
)
from modelscripts.source.printer import (
    AbstractPrinter
)

# logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('test.' + __name__)

def indent(prefix,s):
    return '\n'.join([ prefix+l for l in s.split('\n') ])


class PolymorphicPrinter(AbstractPrinter):

    def __init__(self,
                 scenarioOrScenarioEvaluation,
                 modelHeader='scenario model',
                 displayLineNos=True):
        #type: (Union[ScenarioModel, ScenarioEvaluation], Text, bool) -> None
        super(PolymorphicPrinter, self).__init__(
            displayLineNos=displayLineNos
        )
        self.modelHeader=modelHeader

        if isinstance(scenarioOrScenarioEvaluation, ScenarioModel):
            self.scenario=scenarioOrScenarioEvaluation
            self.scenarioEvaluation=None
        elif isinstance(scenarioOrScenarioEvaluation, ScenarioEvaluation):
            self.scenario=scenarioOrScenarioEvaluation.scenario
            self.scenarioEvaluation=scenarioOrScenarioEvaluation
        else:
            raise NotImplementedError()
        if self.scenarioEvaluation is None:
            self.kind='soil'
        else:
            self.kind='sex'
        self.output = ''

    def do(self):
        print('AAAAAAAAAAAAAAAAAAAA')
        super(PolymorphicPrinter, self).do()
        self._scenario(self.scenario)
        return self.output

    # def docComment(self, source_element, indent):
    #     c = source_element.docComment   # multiple lines
    #     if c is not None:
    #         for line in c:
    #             self.out(indent+'--'+line+'\n')
    #
    # def eolComment(self, source_element):
    #     c = source_element.eolComment
    #     if c is not None:
    #         self.out(' --'+c)
    #     self.out('\n')


    def _scenario(self, scenario, originalOrder=False):
        print('BBBBBB')
        self.outLine('XXXX')

        if scenario.name is not None:
            self.outLine(
                '-- @%s %s' % (self.modelHeader, scenario.name),
                scenario.lineNo)
        self.outLine('XXXX %i'%len(scenario.actorInstanceNamed))

        for ai in scenario.actorInstanceNamed.values():
            self._actorInstance(ai)

        if originalOrder:
            for op in scenario.originalOrderOperations:
                self._operation(op)
        else:
            for b in scenario.contextBlocks:
                self._block(b)
            for b in scenario.mainBlocks:
                self._block(b)




    def _actorInstance(self, ai):
        self.outLine(
            '-- @actori %s:%s' % (
                 ai.name,
                 ai.actor.name),
            ai.lineNo)


    #===================================================
    #  Blocks
    #===================================================

    def _block(self, b):
        #type:(blocks.Block) -> None
        if isinstance(b, blocks.UsecaseInstanceBlock):
            self._usecaseInstanceBlock(b)
        elif isinstance(b, blocks.TopLevelBlock):
            self._topLevelBlock(b)
        elif isinstance(b, blocks.ContextBlock):
            self._contextBlock(b)


    def _contextBlock(self, b):
        self.outLine('-- @context', b.lineNo)
        for op in b.operations:
            self._operation(op)
        self.outLine('-- @endcontext', None) #TODO

    def _usecaseInstanceBlock(self, b):
        self.outLine(
            '-- @uci %s %s' %(
                b.actorInstance.name,
                b.useCase.name),
            b.lineNo
        )
        for op in b.operations:
            self._operation(op)
        self.outLine('-- @enduci', None) #TODO


    def _topLevelBlock(self, b):
        for op in b.operations:
            self._operation(op)



    #===================================================
    #  Operations
    #===================================================

    def _operation(self, op):
        if isinstance(op, operations.ObjectCreation):
            self._objectCreation(op)
        elif isinstance(op, operations.ObjectDestruction):
            self._objectDestruction(op)
        elif isinstance(op, operations.LinkCreation):
            self._linkCreation(op)
        elif isinstance(op, operations.LinkDestruction):
            self._linkDestruction(op)
        elif isinstance(op, operations.LinkObjectCreation):
            self._linkObjectCreation(op)
        elif isinstance(op, operations.AttributeAssignment):
            self._attributeAssignment(op)
        elif isinstance(op, operations.Query):
            self._query(op)
        elif isinstance(op, operations.Check):
            self._check(op)
        else:
            raise NotImplementedError()


    #--- update operations --------------------------------

    def _objectCreation(self, op):
        self.outLine(
            '! %s := new %s(%s)' % (
                op.name,
                op.class_.name,
                ("'%s'" % op.id) if op.id else ''),
            lineNo=op.lineNo
        )

    def _objectDestruction(self, op):
        self.outLine(
            '! destroy %s' % op.name,
            lineNo=op.lineNo
        )

    def _linkCreation(self, op):
        self.outLine(
            '! insert (%s) into %s' %(
                ', '.join(op.names),
                op.association.name),
            lineNo=op.lineNo
        )

    def _linkDestruction(self, op):
        self.outLine(
            'delete (%s) from %s' % (
                ', '.join(op.names),
                op.association.name),
            lineNo = op.lineNo,
        )

    def _linkObjectCreation(self, op):
        self.outLine(
            '! %s:=new %s(%s) between (%s)' % (
                op.name,
                op.associationClass.name,
                ("'%s'" % op.id) if op.id else '',
                ', '.join(op.names)),
            lineNo = op.lineNo,
        )

    def _attributeAssignment(self, op):
        self.outLine(
            '! %s.%s := %s' % (
                op.variableName,
                op.attributeName,
                op.expression),
            lineNo=op.lineNo
        )



    #--- queries ------------------------------------------

    def _query(self, op):
        self.outLine(
            '%s %s' % (
                '??' if op.verbose else '?',
                op.expression,
            ),

        ),
        if op.queryEvaluation is not None:
            self._queryEvaluation(op.queryEvaluation)
            #TODO: check if the output is correct for ??

    def _queryEvaluation(self, qe):
        for se in qe.subexpressions:
            self.outLine(
                '  %s' %se
            )
        self.outLine('-> %s : %s\n' % (
            qe.resultValue,
            qe.resultType,
        ))




    #--- check ------------------------------------------


    def _check(self, op):
        self.outLine(
            'check%s%s%s' % (
                ' -d' if op.showFaultyObjects else '',
                ' -v' if op.verbose else '',
                ' -a' if op.all else ''),
            lineNo=op.lineNo
        )
        if op.checkEvaluation is not None:
            self._checkEvaluation(op.checkEvaluation)

    def _checkEvaluation(self, ce):
        for c in ce.cardinalityEvaluations.values():
            if isinstance(c, CardinalityViolation):
                self._cardinalityViolation(c)
        for (index,ie) in enumerate(ce.invariantEvaluations.values()):
            self._invariantEvaluation(index+1,ie)
        self.outLine('checked %i invariants in ?.???s, %i failure.' % (
            len(ce.invariantEvaluations),
            999
        ))

    def _cardinalityViolation(self, c):
        for vo in c.violatingObjects:
            self._cardinalityViolatingObject(vo)

    def _cardinalityViolatingObject(self, vo):
        r=vo.cardinalityViolation.role
        obj_label=vo.violatingObject
        class_name=r.type.name
        target_class_name=r.opposite.type.name
        assocname=vo.cardinalityViolation.role.association.name
        self.outLine('Multiplicity constraint violation'
                 ' in association `%s\':' % assocname)
        self.outLine(
            "  Object `%s' of class `%s'"
            " is connected to %i objects of class `%s'" % (
                obj_label,
                class_name,
                vo.actualCardinality,
                target_class_name,
            ))
        self.outLine(
            "  at association end `%s' but the"
            " multiplicity is specified as `%s'." % (

                r.name,
                r.cardinalityLabel
            )
        )

    def _invariantEvaluation(self, nth, ie):
        if isinstance(ie,InvariantValidation):
            self._invariantValidation(nth, ie)
        else:
            self._invariantViolation(nth, ie)

    def _invariantValidation(self, nth, iv):
        self.outLine(
            "checking invariant (%i) `%s': OK." % (
                nth,
                iv.invariant.invariantLabel
            ))

    def _invariantViolation(self, nth, iv):
        self.outLine(
            "checking invariant (%s) `%s': FAILED." % (
                nth,
                iv.invariant.invariantLabel
            ))
        self.outLine('  -> %s : %s' % (
            iv.resultValue,
            iv.resultType,
        ))
        if len(iv.subexpressions) >= 0:
            self.outLine('Results of subexpressions:')
            for e in iv.subexpressions:
                self.outLine('  %s' % e)
        self.outLine('Instances of %s violating the invariant:' % (
            iv.violatingObjectType,
        ))
        self.outLine('  -> Set{%s} : Set(%s)\n' % (
            ','.join(iv.violatingObjects),
            iv.violatingObjectsType,
        ))



    # def cardinalityViolation(self, cv):
    #     _=('Multiplicity constraint violation'
    #        'in association '
    #        '`%s\':\n')
    #     self.out(_ % cv.)




# +r'  Object `%s' of class '
# +r'`(?P<sourceClass>\w+)\' is connected to '
# +r'(?P<numberOfObjects>\d+) objects of class '
# +r'`(?P<targetClass>\w+)\''

class SoilPrinter(PolymorphicPrinter):

    def __init__(self, scenario, displayLineNos=True):
        #type: (ScenarioModel, bool) -> None
        super(SoilPrinter, self).__init__(
            scenario,
            modelHeader='scenario model',
            displayLineNos = displayLineNos
        )


class SexPrinter(PolymorphicPrinter):

    def __init__(self, scenario, displayLineNos=True):
        #type: (ScenarioEvaluation, bool) -> None
        super(SexPrinter, self).__init__(
            scenario,
            modelHeader='scenario evaluation model',
            displayLineNos=displayLineNos
        )


