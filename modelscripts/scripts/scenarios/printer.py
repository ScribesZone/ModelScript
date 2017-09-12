# coding=utf-8



import logging

from typing import Union, Text

from modelscripts.base.printers import (
    ModelPrinter,
    SourcePrinter,
    indent
)

from modelscripts.metamodels.scenarios import (
    ScenarioModel,
    operations,
    blocks,
    metamodel
)
from modelscripts.metamodels.scenarios.evaluations import (
    ScenarioEvaluation,
)
from modelscripts.metamodels.scenarios.evaluations.operations import InvariantValidation, CardinalityViolation


__all__ = ['ScenarioModelPrinter']

# logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('test.' + __name__)


# def printStatus(self):
#     """
#     Print the status of the file:
#
#     * the list of errors if the file is invalid,
#     * a short summary of entities (classes, attributes, etc.) otherwise
#     """
#     if self.isValid:
#         p = ScenarioModelPrinter(
#             scenario=self.scenario,
#             displayLineNos=True,
#             displayBlockSeparators=True,
#             displayEvaluation=True,
#             originalOrder=True)
#         print(p.do())
#     else:
#         print('%s error(s) in the model' % len(self.issues))
#         for e in self.issues:
#             print(e)

class ScenarioModelPrinter(ModelPrinter):

    def __init__(self,
                 theModel,
                 summary=False,
                 modelHeader='scenario model',
                 displayLineNos=True,
                 displayBlockSeparators=True,
                 displayEvaluation=True,
                 originalOrder=True):
        #type: (Union[ScenarioModel, ScenarioEvaluation], bool, Text, bool, bool, bool, bool) -> None
        # Check if it make sense for ScenarioEvaluation
        assert isinstance(theModel, ScenarioModel)
        super(ScenarioModelPrinter, self).__init__(
            theModel=theModel,
            summary=summary,
            displayLineNos=displayLineNos
        )
        self.scenario=theModel
        self.scenarioEvaluation=self.scenario.scenarioEvaluation
        self.modelHeader=modelHeader
        self.displayBlockSeparators=displayBlockSeparators
        self.doDisplayEvaluation=(
            displayEvaluation
            and self.scenarioEvaluation is not None)
        self.originalOrder=originalOrder
        self.output = ''

    def do(self):
        self.output = ''
        self._issues()
        self._model()
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


    def _model(self):

        if self.scenario.name is not None:
            self.outLine(
                '-- @%s %s' % (self.modelHeader, self.scenario.name),
                self.scenario.lineNo)

        for ai in self.scenario.actorInstanceNamed.values():
            self._actorInstance(ai)

        if self.doDisplayEvaluation and self.scenario.scenarioEvaluation is not None:
            self._accessSet(self.scenario.scenarioEvaluation.accessSet)

        if self.originalOrder:
            blocks = self.scenario.originalOrderBlocks
        else:
            blocks = self.scenario.logicalOrderBlocks
        for b in blocks:
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
        if self.displayBlockSeparators:
            self.outLine('')
        if isinstance(b, blocks.UsecaseInstanceBlock):
            self._usecaseInstanceBlock(b)
        elif isinstance(b, blocks.TopLevelBlock):
            self._topLevelBlock(b)
        elif isinstance(b, blocks.ContextBlock):
            self._contextBlock(b)
        else:
            raise NotImplementedError()

    def _blockEvaluation(self, be):
        self.outLine('---> TODO: block access set ')

    def _contextBlock(self, b):
        self.outLine('-- @context', b.lineNo)
        if self.doDisplayEvaluation and b.blockEvaluation is not None:
            self._blockEvaluation(b.blockEvaluation)
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
        if self.doDisplayEvaluation and b.blockEvaluation is not None:
            self._blockEvaluation(b.blockEvaluation)
        for op in b.operations:
            self._operation(op)
        self.outLine('-- @enduci', None) #TODO


    def _topLevelBlock(self, b):
        if self.doDisplayEvaluation and b.blockEvaluation is not None:
            self._blockEvaluation(b.blockEvaluation)
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
        if op.operationEvaluation is not None:
            e=op.operationEvaluation
            self._operationAccesses(e.accesses)

    def _operationAccesses(self, accesses):
        for a in accesses:
            self._operationAccess(a)

    def _operationAccess(self, access):
        self.outLine('---> %s' % str(access))


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
        if self.doDisplayEvaluation and op.operationEvaluation is not None:
            self._queryEvaluation(op.operationEvaluation)
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
        if self.doDisplayEvaluation and op.operationEvaluation is not None:
            self._checkEvaluation(op.operationEvaluation)

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
        r=vo.cardinalityViolation._role
        obj_label=vo.violatingObject
        class_name=r.type.name
        target_class_name=r.opposite.type.name
        assocname=vo.cardinalityViolation._role._association.name
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


    def _accessSet(self, accessSet):
        self.outLine('->  %i accesses' % len(accessSet.accesses))
        for a in accessSet.accesses:
            self._access(a)

    def _access(self, access):
        self.outLine('   %s %s' % (
            access.action,
            access.resource.label ))


class ScenarioSourcePrinter(SourcePrinter):

    def __init__(self,
                 theSource,
                 summary=False,
                 displayLineNos=True,
                 modelHeader='scenario model',
                 displayBlockSeparators=True,
                 displayEvaluation=True,
                 originalOrder=True,
                 ):
        super(ScenarioSourcePrinter, self).__init__(
            theSource=theSource,
            summary=False,
            displayLineNos=True)

    def do(self):
        self.output=''
        if self.theSource.model is not None:
            p=ScenarioModelPrinter(
                theModel=self.theSource.model,
                summary=self.summary,
                modelHeader='scenario model',
                displayLineNos=self.displayLineNos,
                displayBlockSeparators=True,
                displayEvaluation=True,
                originalOrder=True,
            ).do()
            self.out(p)
        else:
            self._issues()
        return self.output

metamodel.registerSourcePrinter(ScenarioSourcePrinter)
metamodel.registerModelPrinter(ScenarioModelPrinter)