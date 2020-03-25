# coding=utf-8
from __future__ import unicode_literals, print_function, absolute_import, \
    division

from typing import Optional

from modelscript.base.modelprinters import (
    ModelPrinter,
    ModelSourcePrinter,
    ModelPrinterConfig,
)
from modelscript.metamodels.aui import (
    AUIModel,
    METAMODEL
)

__all__ = [
    'AUIModelPrinter',
]

class AUIModelPrinter(ModelPrinter):

    def __init__(self,
                 theModel,
                 config=None):
        #type: (AUIModel, Optional[ModelPrinterConfig]) -> None
        super(AUIModelPrinter, self).__init__(
            theModel=theModel,
            config=config)

    def doModelContent(self):
        super(AUIModelPrinter, self).doModelContent()
        self.doAUIModel(self.theModel)
        return self.output

    def doAUIModel(self, relationModel):
        self.doModelTextBlock(relationModel.description)

        for space in relationModel.spaces:
            self.doSpace(space)

        return self.output


    def doSpace(self, space):
        self.outLine(
            '%s %s' %(
                self.kwd('space'),
                space.name),
        )
        self.doModelTextBlock(space.description)
        return self.output


METAMODEL.registerModelPrinter(AUIModelPrinter)
METAMODEL.registerSourcePrinter(ModelSourcePrinter)


