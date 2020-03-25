# coding=utf-8


from typing import Optional

from modelscript.base.modelprinters import (
    ModelPrinter,
    ModelSourcePrinter,
    ModelPrinterConfig,
)
from modelscript.metamodels.participants import (
    ParticipantModel,
    METAMODEL
)

__all__ = [
    'ParticipantModelPrinter',
]

class ParticipantModelPrinter(ModelPrinter):

    def __init__(self,
                 theModel,
                 config=None):
        #type: (ParticipantModel, Optional[ModelPrinterConfig]) -> None
        super(ParticipantModelPrinter, self).__init__(
            theModel=theModel,
            config=config)

    def doModelContent(self):
        super(ParticipantModelPrinter, self).doModelContent()
        self.doParticipantModel(self.theModel)
        return self.output

    def doParticipantModel(self, relationModel):
        pass


METAMODEL.registerModelPrinter(ParticipantModelPrinter)
METAMODEL.registerSourcePrinter(ModelSourcePrinter)


