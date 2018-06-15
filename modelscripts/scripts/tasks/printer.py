# coding=utf-8
from __future__ import unicode_literals, print_function, absolute_import, \
    division

from typing import Optional

from modelscripts.base.modelprinters import (
    ModelPrinter,
    ModelSourcePrinter,
    ModelPrinterConfig,
)
from modelscripts.metamodels.tasks import (
    TaskModel,
    METAMODEL
)

__all__ = [
    'TaskModelPrinter',
]

class TaskModelPrinter(ModelPrinter):

    def __init__(self,
                 theModel,
                 config=None):
        #type: (TaskModel, Optional[ModelPrinterConfig]) -> None
        super(TaskModelPrinter, self).__init__(
            theModel=theModel,
            config=config)

    def doModelContent(self):
        super(TaskModelPrinter, self).doModelContent()
        self.doTaskModel(self.theModel)
        return self.output

    def doTaskModel(self, taskModel):
        self.doModelTextBlock(taskModel.description)
        self.doTask(taskModel.rootTask, level=0)
        return self.output

    def doTask(self, task, level):
        line = '%s %s %s' % (
            task.decomposition,
            task.name,
            ''.join(task.decorations)
        )
        self.outLine(line, indent=level)
        for subtask in task.subTasks:

            self.doTask(subtask, level+1)
        return self.output

    #
    # def doSystem(self, system):
    #         self.outLine(
    #             '%s %s ' % (
    #                 self.kwd('system'),
    #                 system.name),
    #             lineNo=system.lineNo,
    #             linesBefore=1,
    #             linesAfter=1)
    #         self.doModelTextBlock(system.description)
    #
    #         for usecase in system.usecases:
    #             self.doUsecase(usecase)
    #
    #
    # def doActor(self, actor):
    #     self.outLine(
    #         '%s %s' %(
    #             self.kwd('actor'),
    #             actor.name),
    #         lineNo=actor.lineNo
    #     )
    #     self.doModelTextBlock(actor.description)
    #     return self.output
    #
    #
    # def doUsecase(self, usecase):
    #     self.outLine(
    #        '%s %s' %(
    #            self.kwd('usecase'),
    #            usecase.name ),
    #         lineNo=usecase.lineNo
    #     )
    #     self.doModelTextBlock(usecase.description)
    #     return self.output
    #
    #
    # def doInteractions(self, usecaseModel):
    #     if usecaseModel.nbOfInteractions==0:
    #         self.out('no ')
    #     self.outLine(self.kwd('interactions'))
    #     for a in usecaseModel.actors:
    #         for u in a.usecases:
    #             self.outLine(
    #                 'A %s can %s.' % (a.name, u.name,),
    #                 indent=1)
    #     # if usecaseModel.system.name == '*unknown*':
    #     #     self.outLine('-- NO SYSTEM DEFINED !')
    #     # else:
    #     #     for u in usecaseModel.system.usecases:
    #     #         if len(u.actors)==0:
    #     #             self.outLine(Styles.mediumIssue.do('-- NOBODY %s') % u.name)
    #     #             # self.outLine('')
    #     #     self.outLine('')
    #     return self.output


    # def doSummary(self):
    #     super(UsecaseModelPrinter, self).doSummary()
    #     return self.output

METAMODEL.registerModelPrinter(TaskModelPrinter)
METAMODEL.registerSourcePrinter(ModelSourcePrinter)


