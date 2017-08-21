# coding=utf-8
from __future__ import unicode_literals, print_function, absolute_import, division
from typing import Text, Union, Optional, Dict, List

from modelscripts.source.printer import (
    AbstractPrinter
)

from modelscripts.metamodels.usecases import (
    UsecaseModel,
    Actor,
    System,
    Usecase
)



class Printer(AbstractPrinter):

    def __init__(self, usecaseModel, displayLineNos=True):
        #type: (UsecaseModel, bool) -> None
        super(Printer,self).__init__(
            displayLineNos=displayLineNos)
        self.usecaseModel=usecaseModel

    def do(self):
        super(Printer,self).do()
        self._usecaseModel(self.usecaseModel)
        return self.output

    def _usecaseModel(self, usecaseModel):
        self.outLine(
            'usecase model',
            lineNo=None, #usecaseModel.lineNo)  # TODO: change parser
            linesAfter=1  )

        self.doActorsUsecases(usecaseModel)


        for actor in usecaseModel.actorNamed.values():
            self.actor(actor)

        self.outLine(
            'system %s ' % usecaseModel.system.name,
            lineNo=usecaseModel.system.lineNo,
            linesBefore=1,
            linesAfter=1)

        for usecase in usecaseModel.system.usecases:
            self.usecase(usecase)



    def actor(self, actor):
        self.outLine(
            'actor %s' % actor.name,
            lineNo=actor.lineNo
        )

    def usecase(self, usecase):
        self.outLine(
           'usecase %s' % usecase.name,
            lineNo=usecase.lineNo
        )

    def doActorsUsecases(self, usecaseModel):
        for a in usecaseModel.actors:
            if len(a.usecases)>=1:
                for u in a.usecases:
                    self.outLine('%s %s' % (a.name, u.name))
            else:
                self.outLine('-- %s DO_NOTHING' % a.name)
        for u in usecaseModel.system.usecases:
            if len(u.actors)==0:
                self.outLine('-- NOBODY %s' % u.name)
                self.outLine('')
        self.outLine('')




