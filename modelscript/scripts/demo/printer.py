# coding=utf-8


from typing import Optional

from modelscript.base.modelprinters import (
    ModelPrinterConfig,
    ModelSourcePrinter
)
from modelscript.metamodels.demo import (
    METAMODEL,
    DemoModel
)

import logging

from typing import Optional

from modelscript.base.modelprinters import (
    ModelPrinter,
    ModelPrinterConfig,
)
from modelscript.base.printers import (
    indent
)
from modelscript.metamodels.classes import (
    ClassModel
)


# logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('test.' + __name__)


__all__ = [
    'DemoModelPrinter',
]


class DemoModelPrinter(ModelPrinter):
    def __init__(self,
                 theModel,
                 config=None):
        #type: (DemoModel, Optional[ModelPrinterConfig]) -> None
        assert theModel is not None
        assert isinstance(theModel, DemoModel)
        super(DemoModelPrinter, self).__init__(
            theModel=theModel,
            config=config
        )

    def doModelContent(self):
        super(DemoModelPrinter, self).doModelContent()
        self.doDemoModel(self.theModel)
        return self.output

    def doDemoModel(self, model):
        self.doModelTextBlock(model.description)

        for c in model.classes:
            self.doPlainClass(c)

        return self.output

    def doClass(self, class_):
        # self.doModelTextBlock(class_.description)

        # if class_.superclasses:
        #     sc = (self.kwd('extends ')
        #           +self.kwd(',').join([s.name for s in class_.superclasses]))
        # else:
        #     sc = ''
        # if class_.isAbstract:
        #     abstract='abstract '
        # abstract='abstract' if class_.isAbstract else None
        # self.outLine(' '.join([_f for _f in [
        #     (self.kwd('abstract') if class_.isAbstract else ''),
        #     self.kwd('class'),
        #     self.qualified(class_),
        #     sc] if _f]))
        #
        # # self.doModelTextBlock(class_.description)
        # if class_.attributes:
        #     self.outLine(self.kwd('attributes'), indent=1)
        #     for attribute in class_.attributes:
        #         self.doAttribute(attribute)

        return self.output



METAMODEL.registerModelPrinter(DemoModelPrinter)
METAMODEL.registerSourcePrinter(ModelSourcePrinter)

