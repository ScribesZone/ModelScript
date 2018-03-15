# coding=utf-8



import logging

from typing import Union, Text, Optional

from modelscripts.base.styles import Styles
from modelscripts.scripts.base.printers import (
    ModelPrinter,
    ModelSourcePrinter,
    ModelPrinterConfig,
)
from modelscripts.metamodels.scenarios import (
    ScenarioModel,
    operations,
    blocks,
    METAMODEL
)
from modelscripts.metamodels.scenarios.evaluations import (
    ScenarioEvaluation,
)
from modelscripts.metamodels.scenarios.evaluations.operations import InvariantValidation, CardinalityViolation, AssertQueryEvaluation


__all__ =(
    'ScenarioModelPrinter',
    'ScenarioModelPrinterConfig',
    'ScenarioModelPrinterConfigs'
)


# logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('test.' + __name__)

class ScenarioModelPrinterConfig(ModelPrinterConfig):
    def __init__(self,
                 styled=True,
                 width=120,
                 baseIndent=0,
                 displayLineNos=True,
                 lineNoPadding=' ',
                 verbose=0,
                 quiet=False,
                 #------------------------
                 title=None,
                 issuesMode='top',
                 #------------------------
                 contentMode='self',  #self|source|model|no
                 summaryMode='top',  # top | down | no,
                 #------------------------
                 #------------------------
                 #------------------------
                 modelHeader='scenario model',
                 displayBlockSeparators=True,
                 displayEvaluation=True,
                 originalOrder=True,
                 useSyntax=True   #<-- TODO: change to False
                 ):
        super(ScenarioModelPrinterConfig, self).__init__(
            styled=styled,
            width=width,
            baseIndent=baseIndent,
            displayLineNos=displayLineNos,
            lineNoPadding=lineNoPadding,
            verbose=verbose,
            quiet=quiet,
            title=title,
            issuesMode=issuesMode,
            contentMode=contentMode,
            summaryMode=summaryMode)
        self.modelHeader=modelHeader
        self.displayBlockSeparators=displayBlockSeparators
        self.displayEvaluation=displayEvaluation
        self.originalOrder=originalOrder
        self.useSyntax=useSyntax

class ScenarioModelPrinterConfigs(object):
    default=ScenarioModelPrinterConfig()

class ScenarioModelPrinter(ModelPrinter):

    def __init__(self,
                 theModel,
                 config=None):
        #type: (Union[ScenarioModel, ScenarioEvaluation],  Optional[ScenarioModelPrinterConfig]) -> None
        if config is None:
            config=ScenarioModelPrinterConfig()
        else:

            #----------------------------------------------
            #TODO: the following code is an adapter that
            #       must be removed when a solution is found
            #       to have configuration dependent options
            #       In that case, the config provide will
            #       be directly
            assert(isinstance(config, ModelPrinterConfig))
            config.modelHeader='scenario model'
            config.displayBlockSeparators=True
            config.displayEvaluation=True
            config.originalOrder=True
            config.useSyntax=True
            #----------------------------------------------



        self.config=config #type: ScenarioModelPrinterConfig
        super(ScenarioModelPrinter, self).__init__(
            theModel=theModel,
            config=config
        )

    # def __init__(self,
    #              theModel,
    #              summary=False,
    #              displayLineNos=True,
    #              displayBlockSeparators=True,
    #              displayEvaluation=True,
    #              originalOrder=True):
    #     #type: (Union[ScenarioModel, ScenarioEvaluation], bool, Text, bool, bool, bool, bool) -> None
        # Check if it make sense for ScenarioEvaluation
        assert isinstance(theModel, ScenarioModel)
        # super(ScenarioModelPrinter, self).__init__(
        #     theModel=theModel,
        #     summary=summary,
        #     displayLineNos=displayLineNos
        # )
        self.scenario=theModel
        self.scenarioEvaluation=self.scenario.scenarioEvaluation
        self.modelHeader=self.config.modelHeader
        self.displayBlockSeparators=self.config.displayBlockSeparators

        self.doDisplayEvaluation=(
            self.config.displayEvaluation
            and self.scenarioEvaluation is not None)
        self.originalOrder=self.config.originalOrder

    def doModelContent(self):
        super(ScenarioModelPrinter, self).doModelContent()
        self.scenarioModel(self.theModel)
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


    def scenarioModel(self, scenario):
        # super(ScenarioModelPrinter, self).doModelContent()

        for ai in scenario.actorInstanceNamed.values():
            self.doActorInstance(ai)

        if self.doDisplayEvaluation and self.scenario.scenarioEvaluation is not None:
            self.doAccessSet(self.scenario.scenarioEvaluation.accessSet)

        if self.originalOrder:
            blocks = self.scenario.originalOrderBlocks
        else:
            blocks = self.scenario.logicalOrderBlocks
        for b in blocks:
            self.doBlock(b)
        return self.output


    def doActorInstance(self, ai):
        self.outLine('%s%s %s%s%s'%(
                '' if not self.config.useSyntax else self.cmt('-- @'),
                self.kwd('actori'),
                ai.name,
                self.kwd(':'),
                ai.actor.name),
            ai.lineNo)
        return self.output


    #===================================================
    #  Blocks
    #===================================================

    def doBlock(self, b):
        #type:(blocks.Block) -> None
        if self.displayBlockSeparators:
            self.outLine('')
        if isinstance(b, blocks.UsecaseInstanceBlock):
            self.doUsecaseInstanceBlock(b)
        elif isinstance(b, blocks.TopLevelBlock):
            self.doTopLevelBlock(b)
        elif isinstance(b, blocks.ContextBlock):
            self.doContextBlock(b)
        else:
            raise NotImplementedError()

    def doBlockEvaluation(self, be):
        self.outLine(
            Styles.highlight.do(
                '---> TODO: block access set ',
                styled=self.config.styled))
        return self.output


    def doContextBlock(self, b):
        self.outLine(self.kwd('context'), b.lineNo)
        self.indent(1)
        if self.doDisplayEvaluation and b.blockEvaluation is not None:
            self.doBlockEvaluation(b.blockEvaluation)
        for op in b.operations:
            self.doOperation(op)
        self.indent(-1)
        self.outLine(self.kwd('end'), None) #TODO
        return self.output


    def doUsecaseInstanceBlock(self, b):
        self.outLine(
            '%s %s %s' %(
                self.kwd('usecasei'),
                b.actorInstance.name,
                b.useCase.name),
            b.lineNo
        )
        self.indent(1)
        if self.doDisplayEvaluation and b.blockEvaluation is not None:
            self.doBlockEvaluation(b.blockEvaluation)
        for op in b.operations:
            self.doOperation(op)
        self.indent(-1)
        self.outLine(self.kwd('end'), None) #TODO
        return self.output



    def doTopLevelBlock(self, b):
        self.outLine(
            '%s' %(
                self.kwd('scenario begin'))
        )
        if self.doDisplayEvaluation and b.blockEvaluation is not None:
            self.doBlockEvaluation(b.blockEvaluation)
        for op in b.operations:
            self.doOperation(op)
        self.outLine(
            '%s' % (
                self.kwd('scenario end'))
        )
        return self.output




    #===================================================
    #  Operations
    #===================================================

    def doOperation(self, op):
        if isinstance(op, operations.ObjectCreation):
            self.doObjectCreation(op)
        elif isinstance(op, operations.ObjectDestruction):
            self.doObjectDestruction(op)
        elif isinstance(op, operations.LinkCreation):
            self.doLinkCreation(op)
        elif isinstance(op, operations.LinkDestruction):
            self.doLinkDestruction(op)
        elif isinstance(op, operations.LinkObjectCreation):
            self.doLinkObjectCreation(op)
        elif isinstance(op, operations.AttributeAssignment):
            self.doAttributeAssignment(op)
        elif isinstance(op, operations.Query):
            self.doQuery(op) # do not change order
        elif isinstance(op, operations.Check):
            self.doCheck(op)
        else:
            raise NotImplementedError()
        if op.operationEvaluation is not None:
            e=op.operationEvaluation
            self.doOperationAccesses(e.accesses)
        return self.output

    def doOperationAccesses(self, accesses):
        for a in accesses:
            self.doOperationAccess(a)
        return self.output


    def doOperationAccess(self, access):
        self.outLine(
            Styles.highlight.do(
                '---> %s' % str(access),
                styled=self.config.styled))
        return self.output


    #--- update operations --------------------------------

    def doObjectCreation(self, op):
        if self.config.useSyntax:
            self.outLine(
                '%s %s %s %s %s%s%s%s' % (
                    self.kwd('!'),
                    op.name,
                    self.kwd(':='),
                    self.kwd('new'),
                    op.class_.name,
                    self.kwd('('),
                    ("'%s'" % op.id) if op.id else '',
                    self.kwd(')')),
                lineNo=op.lineNo
            )
        else:
            self.outLine(Styles.highlight.do('TODO doObjectCreation'))
        return self.output

    def doObjectDestruction(self, op):
        if self.config.useSyntax:
            self.outLine('%s %s %s' %(
                self.kwd('!'),
                self.kwd('destroy'),
                op.name),
            lineNo=op.lineNo)
        else:
            self.outLine(Styles.highlight.do('TODO doObjectDestruction'))
        return self.output

    def doLinkCreation(self, op):
        if self.config.useSyntax:
            self.outLine(
                '%s %s %s%s%s %s %s' %(
                    self.kwd('!'),
                    self.kwd('insert'),
                    self.kwd('('),
                    self.kwd(', ').join(op.names),
                    self.kwd(')'),
                    self.kwd('into'),
                    op.association.name),
                lineNo=op.lineNo
            )
        else:
            self.outLine(Styles.highlight.do('TODO doLinkCreation'))
        return self.output

    def doLinkDestruction(self, op):
        if self.config.useSyntax:
            self.outLine(
                '%s %s %s%s%s %s %s' % (
                    self.kwd('!'),
                    self.kwd('delete'),
                    self.kwd('('),
                    self.kwd(', ').join(op.names),
                    self.kwd(')'),
                    self.kwd('from'),
                    op.association.name),
                lineNo = op.lineNo,
            )
        else:
            self.outLine(Styles.highlight.do('TODO doLinkDestruction'))

        return self.output

    def doLinkObjectCreation(self, op):
        if self.config.useSyntax:
            self.outLine(
                '%s %s %s %s %s%s%s%s %s %s%s%s' % (
                    self.kwd('!'),
                    op.name,
                    self.kwd(':='),
                    self.kwd('new'),
                    op.associationClass.name,
                    self.kwd('('),
                    ("'%s'" % op.id) if op.id else '',
                    self.kwd(')'),
                    self.kwd('between'),
                    self.kwd('('),
                    self.kwd(', ').join(op.names),
                    self.kwd(')')),
                lineNo = op.lineNo,
                )
        else:
            self.outLine(Styles.highlight.do('TODO doLinkObjectCreation'))
        return self.output

    def doAttributeAssignment(self, op):
        if self.config.useSyntax:
            self.outLine(
                '%s %s%s%s %s %s' % (
                    self.kwd('!'),
                    op.variableName,
                    self.kwd('.'),
                    op.attributeName,
                    self.kwd(':='),
                    op.expression),
                lineNo=op.lineNo
            )
        else:
            self.outLine(Styles.highlight.do('TODO doAttributeAssignment'))
        return self.output



    #--- queries or assert queries ------------------


    def doQuery(self, op):
        is_assert=isinstance(op, operations.AssertQuery)
        if self.config.useSyntax:
            if is_assert:
                self.outLine('%s %s' %(
                    self.kwd('assert'),
                    op.expression))
            else:
                self.outLine('%s %s' % (
                    self.kwd('??' if op.verbose else '?'),
                    op.expression))
        else:
            self.outLine(Styles.highlight.do('TODO doQuery'))
        if self.doDisplayEvaluation and op.operationEvaluation is not None:
            self.indent(1)
            self.doQueryEvaluation(op.operationEvaluation)
            #TODO: check if the output is correct for ??
            self.indent(-1)
        return self.output

    def doQueryEvaluation(self, qe):
        is_assert=isinstance(qe, AssertQueryEvaluation)
        if is_assert:
            self.outLine('Assertion : %s' % qe.status)
        for se in qe.subexpressions:
            self.outLine(
                self.ann('%s' %se)
            )
        self.outLine(self.ann('-> %s : %s') % (
            qe.resultValue,
            qe.resultType,
        ))
        return self.output




    #--- check ------------------------------------------


    def doCheck(self, op):
        if self.config.useSyntax:
            self.outLine(
                '%s' % (
                    self.kwd('? check')),
                    # self.kwd(' -d') if op.showFaultyObjects else '',
                    # self.kwd(' -v') if op.verbose else '',
                    # self.kwd(' -a') if op.all else ''),
                lineNo=op.lineNo
            )
        else:
            self.outLine(Styles.highlight.do('TODO doCheck'))
        if self.doDisplayEvaluation and op.operationEvaluation is not None:
            self.indent(1)
            self.doCheckEvaluation(op.operationEvaluation)
            self.indent(-1)
        return self.output

    def doCheckEvaluation(self, ce):
        for c in ce.cardinalityEvaluations:
            if isinstance(c, CardinalityViolation):
                self.doCardinalityViolation(c)
        for (index,ie) in enumerate(ce.invariantEvaluations):
            self.doInvariantEvaluation(index + 1, ie)
        # self.outLine(self.ann('checked %i invariants in ?.???s, %i failure.' % (
        #     len(ce.invariantEvaluations),
        #     999
        # )))
        return self.output

    def doCardinalityViolation(self, c):
        for vo in c.violatingObjects:
            self.doCardinalityViolatingObject(vo)
        return self.output


    def doCardinalityViolatingObject(self, vo):
        r=vo.cardinalityViolation.role
        obj_label=vo.violatingObject
        target_class_name=r.type.name
        class_name=r.opposite.type.name
        assocname=vo.cardinalityViolation.role.association.name
        self.outLine(self.ann('Multiplicity constraint violation'
                 ' in association `%s\':' % assocname))
        self.outLine(
            self.ann("  Object `%s' of class `%s'"
            " is connected to %i objects of class `%s'" % (
                obj_label,
                class_name,
                vo.actualCardinality,
                target_class_name,
            )))
        self.outLine(
            self.ann(
            "  at association end `%s' but the"
            " multiplicity is specified as `%s'." % (
                r.name,
                r.cardinalityLabel
            ))
        )
        return self.output


    def doInvariantEvaluation(self, nth, ie):
        if isinstance(ie,InvariantValidation):
            self.doInvariantValidation(nth, ie)
        else:
            self.doInvariantViolation(nth, ie)
        return self.output

    def doInvariantValidation(self, nth, iv):
        self.outLine(
            self.ann("checking invariant (%i) `%s': OK." % (
                nth,
                iv.invariant.invariantLabel
            )))
        return self.output

    def doInvariantViolation(self, nth, iv):
        self.outLine(
            self.ann("checking invariant (%s) `%s': FAILED." % (
                nth,
                iv.invariant.invariantLabel
            )))
        self.outLine(self.ann('  -> %s : %s' % (
            iv.resultValue,
            iv.resultType,
        )))
        if len(iv.subexpressions) >= 0:
            self.outLine(self.ann('Results of subexpressions:'))
            for e in iv.subexpressions:
                self.outLine(self.ann('  %s' % e))
        self.outLine(self.ann('Instances of %s violating the invariant:' % (
            iv.violatingObjectType,
        )))
        self.outLine(self.ann('  -> Set{%s} : Set(%s)\n' % (
            ','.join(iv.violatingObjects),
            iv.violatingObjectType,
        )))


    def doAccessSet(self, accessSet):
        self.outLine(self.ann('->  %i accesses' % len(accessSet.accesses)))
        for a in accessSet.accesses:
            self.doAccess(a)
        return self.output

    def doAccess(self, access):
        self.outLine(self.ann('   %s %s' % (
            access.action,
            access.resource.label )))
        return self.output

METAMODEL.registerModelPrinter(ScenarioModelPrinter)
METAMODEL.registerSourcePrinter(ModelSourcePrinter)
