# coding=utf-8
from __future__ import unicode_literals, print_function, absolute_import, division
from typing import Optional

from modelscripts.scripts.base.printers import (
    ModelPrinter,
    ModelSourcePrinter,
    ModelPrinterConfig,
)

from modelscripts.metamodels.usecases import (
    UsecaseModel,
    METAMODEL
)




class UsecaseModelPrinter(ModelPrinter):

    def __init__(self,
                 theModel,
                 config=None):
        #type: (UsecaseModel, Optional[ModelPrinterConfig]) -> None
        super(UsecaseModelPrinter, self).__init__(
            theModel=theModel,
            config=config)

    def doModelContent(self):
        super(UsecaseModelPrinter, self).doModelContent()
        self.doUsecaseModel(self.theModel)
        return self.output

    def doUsecaseModel(self, usecaseModel):
        self.doModelTextBlock(usecaseModel.description)

        if usecaseModel.isSystemDefined:
            self.doSystem(usecaseModel.system)

        for actor in usecaseModel.actorNamed.values():
            self.doActor(actor)

        self.doInteractions(usecaseModel)
        return self.output

    def doSystem(self, system):
            self.outLine(
                '%s %s ' % (
                    self.kwd('system'),
                    system.name),
                lineNo=system.lineNo,
                linesBefore=1,
                linesAfter=1)
            self.doModelTextBlock(system.description)

            for usecase in system.usecases:
                self.doUsecase(usecase)


    def doActor(self, actor):
        self.outLine(
            '%s %s' %(
                self.kwd('actor'),
                actor.name),
            lineNo=actor.lineNo
        )
        self.doModelTextBlock(actor.description)
        return self.output


    def doUsecase(self, usecase):
        self.outLine(
           '%s %s' %(
               self.kwd('usecase'),
               usecase.name ),
            lineNo=usecase.lineNo
        )
        self.doModelTextBlock(usecase.description)
        return self.output


    def doInteractions(self, usecaseModel):
        if usecaseModel.nbOfInteractions==0:
            self.out('no ')
        self.outLine(self.kwd('interactions'))
        for a in usecaseModel.actors:
            for u in a.usecases:
                self.outLine(
                    'A %s can %s.' % (a.name, u.name,),
                    indent=1)
        # if usecaseModel.system.name == '*unknown*':
        #     self.outLine('-- NO SYSTEM DEFINED !')
        # else:
        #     for u in usecaseModel.system.usecases:
        #         if len(u.actors)==0:
        #             self.outLine(Styles.mediumIssue.do('-- NOBODY %s') % u.name)
        #             # self.outLine('')
        #     self.outLine('')
        return self.output


    # def doSummary(self):
    #     super(UsecaseModelPrinter, self).doSummary()
    #     return self.output

METAMODEL.registerModelPrinter(UsecaseModelPrinter)
METAMODEL.registerSourcePrinter(ModelSourcePrinter)


