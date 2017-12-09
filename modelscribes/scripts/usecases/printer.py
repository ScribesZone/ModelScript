# coding=utf-8
from __future__ import unicode_literals, print_function, absolute_import, division
from typing import Optional

from modelscribes.scripts.base.printers import (
    ModelPrinter,
    ModelSourcePrinter,
    ModelPrinterConfig,
)

from modelscribes.metamodels.usecases import (
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
            config=config
        )

    def doModelContent(self):
        super(UsecaseModelPrinter, self).doModelContent()
        self.doUsecaseModel(self.theModel)
        return self.output

    def doUsecaseModel(self, usecaseModel):

        for actor in usecaseModel.actorNamed.values():
            self.doActor(actor)

        if usecaseModel.isSystemDefined:
            self.outLine(
                '%s %s ' % (
                    self.kwd('system'),
                    usecaseModel.system.name),
                lineNo=usecaseModel.system.lineNo,
                linesBefore=1,
                linesAfter=1)

            for usecase in usecaseModel.system.usecases:
                self.doUsecase(usecase)

        self.doActorsUsecases(usecaseModel)
        return self.output


    def doActor(self, actor):
        self.outLine(
            '%s %s' %(
                self.kwd('actor'),
                actor.name),
            lineNo=actor.lineNo
        )
        return self.output


    def doUsecase(self, usecase):
        self.outLine(
           '%s %s' %(
               self.kwd('usecase'),
               usecase.name ),
            lineNo=usecase.lineNo
        )
        return self.output


    def doActorsUsecases(self, usecaseModel):
        for a in usecaseModel.actors:
            for u in a.usecases:
                self.outLine('%s %s' % (a.name, u.name))
        # if usecaseModel.system.name == '*unknown*':
        #     self.outLine('-- NO SYSTEM DEFINED !')
        # else:
        #     for u in usecaseModel.system.usecases:
        #         if len(u.actors)==0:
        #             self.outLine(Styles.smallIssue.do('-- NOBODY %s') % u.name)
        #             # self.outLine('')
        #     self.outLine('')
        return self.output


    # def doSummary(self):
    #     super(UsecaseModelPrinter, self).doSummary()
    #     return self.output

METAMODEL.registerModelPrinter(UsecaseModelPrinter)
METAMODEL.registerSourcePrinter(ModelSourcePrinter)


