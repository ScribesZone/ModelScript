# coding=utf-8
from __future__ import unicode_literals, print_function, absolute_import, division

from modelscripts.base.printers import (
    AbstractPrinter
)
from modelscripts.metamodels.permissions.accesses import (
    metamodel,
    AccessModel,
)
from modelscripts.scripts.permissions.printer import (
    opString,  # FIXME: check where is this stuff
    resourceString
)


class AccessModelPrinter(AbstractPrinter): # TODO: check this

    def __init__(self, accessModel, displayLineNos=True):
        #type: (AccessModel, bool) -> None
        super(AccessModelPrinter, self).__init__(
            displayLineNos=displayLineNos)
        self.accessModel=accessModel

    def do(self):
        super(AccessModelPrinter, self).do()
        self._accessModel(self.accessModel)
        return self.output

    def _accessModel(self, accessModel):
        self.outLine(
            'access model',
            lineNo=None, #usecaseModel.lineNo)  # TODO: change parser
            linesAfter=1 )
        self._accessSet(accessModel.accessSet)

    def _accessSet(self, accessSet):
        self.container   # TODO: check this
        for access in accessSet.accesses:
            self._access(access)

    def _access(self, access):
        self.outLine('    %s %s' % (
            opString(access.op),
            resourceString(access.resource)
        ))


metamodel.registerModelPrinter(AccessModelPrinter)
