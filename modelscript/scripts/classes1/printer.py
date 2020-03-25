# coding=utf-8


from typing import Optional

from modelscript.base.modelprinters import (
    ModelPrinter,
    ModelSourcePrinter,
    ModelPrinterConfig,
)
from modelscript.metamodels.classes1 import (
    Class1Model,
    METAMODEL
)

__all__ = [
    'Class1ModelPrinter',
]

class Class1ModelPrinter(ModelPrinter):

    def __init__(self,
                 theModel,
                 config=None):
        #type: (Class1Model, Optional[ModelPrinterConfig]) -> None
        super(Class1ModelPrinter, self).__init__(
            theModel=theModel,
            config=config)

    def doModelContent(self):
        super(Class1ModelPrinter, self).doModelContent()
        self.doClass1Model(self.theModel)
        return self.output

    def doClass1Model(self, relationModel):
        pass


METAMODEL.registerModelPrinter(Class1ModelPrinter)
METAMODEL.registerSourcePrinter(ModelSourcePrinter)


