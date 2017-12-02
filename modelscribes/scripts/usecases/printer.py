# coding=utf-8
from __future__ import unicode_literals, print_function, absolute_import, division

from modelscribes.base.printers import (
    Styles
)
from modelscribes.scripts.base.printers import (
    ModelPrinter,
    ModelSourcePrinter,
)

from modelscribes.metamodels.usecases import (
    UsecaseModel,
    METAMODEL
)




class UsecaseModelPrinter(ModelPrinter):

    def __init__(self,
                 theModel,
                 title='',
                 issuesMode='bottom',  # top|bottom|inline
                 displayContent=True,
                 preferStructuredContent=True,
                 displaySummary=False,
                 summaryFirst=False,
                 config=None):
        #type: (UsecaseModel, bool) -> None
        super(UsecaseModelPrinter, self).__init__(
            theModel=theModel,
            title=title,
            issuesMode=issuesMode,  # top|bottom|inline
            displayContent=displayContent,
            preferStructuredContent=preferStructuredContent,
            displaySummary=displaySummary,
            summaryFirst=summaryFirst,
            config=config
        )

    def doModelContent(self):
        super(UsecaseModelPrinter, self).doModelContent()
        self.doUsecaseModel(self.theModel)
        return self.output


    def doUsecaseModel(self, usecaseModel):
        self.outLine(
            Styles.keyword.do('usecase model'),
            lineNo=None, #usecaseModel.lineNo)  # TODO: change parser
            linesAfter=1  )

        for actor in usecaseModel.actorNamed.values():
            self.doActor(actor)

        if usecaseModel.isSystemDefined:
            self.outLine(
                '%s %s ' % (
                    Styles.keyword.do('system'),
                    usecaseModel.system.name),
                lineNo=usecaseModel.system.lineNo,
                linesBefore=1,
                linesAfter=1)

            for usecase in usecaseModel.system.usecases:
                self.usecase(usecase)

        self.doActorsUsecases(usecaseModel)
        return self.output


    def doActor(self, actor):
        self.outLine(
            '%s %s' %(
                Styles.keyword.do('actor'),
                actor.name),
            lineNo=actor.lineNo
        )
        return self.output


    def usecase(self, usecase):
        self.outLine(
           '%s %s' %(
               Styles.keyword.do('usecase'),
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


    def doSummary(self):
        super(UsecaseModelPrinter, self).doSummary()
        return self.output

METAMODEL.registerModelPrinter(UsecaseModelPrinter)
METAMODEL.registerSourcePrinter(ModelSourcePrinter)


