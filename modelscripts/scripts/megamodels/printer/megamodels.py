# coding=utf-8
from typing import Optional
from modelscripts.base.issues import IssueBox
from modelscripts.scripts.base.printers import (
    ModelPrinter,
    ModelPrinterConfig,
)
from modelscripts.megamodels import Megamodel
from modelscripts.metamodels.megamodels import METAMODEL

class MegamodelPrinter(ModelPrinter):
    def __init__(self,
                 config=None):
        #type: (Optional[ModelPrinterConfig]) -> None
        # if config is None:
        #     config=MegamodelPrinter()
        # config.title='Megamodel'
        super(MegamodelPrinter, self).__init__(
            theModel=Megamodel.model,
            config=config)

    def doModelContent(self):
        super(MegamodelPrinter, self).doModelContent()
        self.doMegamodel(self.theModel)
        return self.output


    # def getIssueBox(self):
    #     return IssueBox()

    # def doSummary(self):
    #     pass
    #
    # def doBody(self):
    #     self.doMegamodel()
    #     return self.output

    def doMegamodel(self, megamodel):
        self.doMetamodelRegistery(megamodel)
        self.doMetaPackageRegistry(megamodel)
        self.doMetaCheckerPackageRegistry(megamodel)
        self.doModelRegistery(megamodel)
        self.doSourceRegistery(megamodel)
        self.doIssueBoxRegistery(megamodel)
        # self.outLine('')
        return self.output

    def doMetamodelRegistery(self, megamodel):
        self.outLine(' (M2) metamodels '.center(80,'-'))
        for mm in megamodel.metamodels():
            self.doMetamodel(mm)
        # for mmd in Megamodel.metamodelDependencies():
        #     self.outLine('%s -> %s' % (
        #         mmd.source.id,
        #         mmd.target.id))
        return self.output

    def doMetamodel(self, mm):
        self.outLine('metamodel %s' % mm.label)
        for mmd in mm.outMetamodels:
            self.outLine('depends on %s' % mmd.label, indent=1)
        self.outLine('')
        return self.output

    def doMetaPackageRegistry(self, megamodel):
        self.outLine(' (M2) metapackages '.center(80,'-'))
        for mm in megamodel.metaPackages():
            self.doMetapackage(mm)
        return self.output

    def doMetapackage(self, mp):
        self.outLine('metapackage %s' % mp.qname)
        return self.output

    def doMetaCheckerPackageRegistry(self, megamodel):
        self.outLine(' (M2) metacheckerspackages '.center(80,'-'))
        for mm in megamodel.metaCheckerPackages():
            self.doMetaCheckerPackage(mm)
        return self.output

    def doMetaCheckerPackage(self, mp):
        self.outLine('metacheckerpackage %s' % mp.qname)
        return self.output

    def doModelRegistery(self, megamodel):
        self.outLine(' (M1) models '.center(80,'-'))
        for m in megamodel.models():
            self.doModel(m)
        # self.outLine(
        #     ', '.join([
        #             m.label for m in megamodel.models()] ))
        # for md in megamodel.modelDependencies():
        #     self.outLine('%s -> %s' % (
        #         md.source.label,
        #         md.target.label))
        return self.output

    def doModel(self, m):
        filespec=(
            "from '%s'" % m.source.basename
            if m.source is not None
            else '')
        self.outLine('%s model %s %s' % (
            m.metamodel.label,
            '_' if m.name=='' else m.name,
            filespec
            ))
        for ud in m.usedModels():
            self.outLine('-> %s' % ud.label, indent=1)
        self.outLine('')
        return self.output

    def doSourceRegistery(self, megamodel):
        self.outLine(' (M1) sources '.center(80,'-'))
        self.outLine(
            ', '.join([
                s.label for s in megamodel.sources()]))
        for sd in megamodel.sourceDependencies():
            self.outLine('%s -> %s' % (
                sd.source.label,
                sd.target.label))
        return self.output

    def doIssueBoxRegistery(self, megamodel):
        self.outLine(' (M1) issues '.center(80,'-'))
        for ib in megamodel.issueBoxes():
            self.doIssueBox(ib)
        return self.output

    def doIssueBox(self, issueBox):
        self.outLine(issueBox.label)
        for p in issueBox.parents:
            self.outLine('-> %s' % p.label, indent=1)
        return self.output



METAMODEL.registerModelPrinter(MegamodelPrinter)