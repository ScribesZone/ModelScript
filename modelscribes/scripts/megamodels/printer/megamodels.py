# coding=utf-8
from modelscribes.base.issues import IssueBox
from modelscribes.base.printers import StructuredPrinter, StructuredPrinterConfig
from modelscribes.megamodels.megamodels import Megamodel


class MegamodelPrinter(StructuredPrinter):
    def __init__(self,
                 config=None):
        if config is None:
            config=StructuredPrinterConfig()
        config.title='Megamodel'
        super(MegamodelPrinter, self).__init__(
            config=config)

    def getIssueBox(self):
        return IssueBox()

    # def doSummary(self):
    #     pass

    def doBody(self):
        self.doMegamodel()
        return self.output

    def doMegamodel(self):
        self.outLine('%'*80)
        self.doMetamodelRegistery()
        self.doModelRegistery()
        self.doSourceRegistery()
        self.outLine('%'*80)
        self.outLine('')


    def doMetamodelRegistery(self):
        self.outLine('-'*30+' metamodels '+'-'*30)
        self.outLine(
            ', '.join([mm.id for mm in Megamodel.metamodels()] ))
        for mmd in Megamodel.metamodelDependencies():
            self.outLine('%s -> %s' % (
                mmd.source.id,
                mmd.target.id))

    def doModelRegistery(self):
        self.outLine('-'*32+' models '+'-'*32)
        self.outLine(
            ', '.join([
                    m.label for m in Megamodel.models()] ))
        for md in Megamodel.modelDependencies():
            self.outLine('%s -> %s' % (
                md.source.label,
                md.target.label))

    def doSourceRegistery(self):
        self.outLine('-' * 32 + ' sources ' + '-' * 31)
        self.outLine(
            ', '.join([
                s.label for s in Megamodel.sources()]))
        for sd in Megamodel.sourceDependencies():
            self.outLine('%s -> %s' % (
                sd.source.label,
                sd.target.label))