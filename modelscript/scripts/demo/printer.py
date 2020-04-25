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
                 theModel: DemoModel,
                 config: Optional[ModelPrinterConfig] = None) \
            -> None:
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
        # self.doModelTextBlock(model.description)

        for c in model.classes:
            self.doClass(c)
        return self.output

    def doClass(self, class_):
        if class_.superclasses:
            superc = (self.kwd('is based on ')
                  + self.kwd(',').join( [
                        s.name for s in class_.superclasses
                    ]))
        else:
            superc = ''
        self.outLine(' '.join(_f  for _f in [
            (self.kwd('abstract') if class_.isAbstract else ''),
            self.kwd('class'),
            class_.name,
            superc
        ] if _f))
        if class_.subclasses:
            self.outLine(
                self.kwd('// subclasses: ')
                + ', '.join(
                    sub.name for sub in class_.subclasses),
                indent=1)
        self.doModelTextBlock(class_.description, indent=1)
        for ref in class_.references:
            self.doReference(ref)
        self.outLine('')
        return self.output

    def doReference(self, reference):
        multiplicity = 'many' if reference.isMultiple else 'one'
        self.outLine(
            reference.name+' '
            + self.kwd(':') + ' '
            + self.kwd(multiplicity) + ' '
            + reference.target.name
            , indent=1)
        self.doModelTextBlock(reference.description, indent=2)


METAMODEL.registerModelPrinter(DemoModelPrinter)
METAMODEL.registerSourcePrinter(ModelSourcePrinter)

