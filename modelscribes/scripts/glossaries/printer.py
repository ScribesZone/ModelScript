# coding=utf-8
from __future__ import unicode_literals, print_function, absolute_import, division
from typing import Text, Union, Optional, Dict, List

from modelscribes.base.printers import (
    AbstractPrinter
)
from modelscribes.metamodels.glossaries import (
    GlossaryModel,
    metamodel
)
from modelscribes.metamodels.texts import (
    Reference
)


# TODO: separate SourcePrinter and ModelPrinter
class GlossaryModelPrinter(AbstractPrinter):

    # TODO: adapt signature
    def __init__(self, glossaryModel, displayLineNos=True):
        #type: (GlossaryModel, bool) -> None
        super(GlossaryModelPrinter, self).__init__(
            displayLineNos=displayLineNos)
        self.glossaryModel=glossaryModel

    def do(self):
        super(GlossaryModelPrinter, self).do()
        self.doGlossaryModel(self.glossaryModel)
        return self.output


    # def out(self, s):
    #     self.output += s
    #
    # def outLine(self, s, lineNo=None):
    #     if self.lineNos:
    #         if lineNo is not None:
    #             self.out('% 5i|' % lineNo)
    #         else:
    #             self.out('     |')
    #     self.out('%s\n' % s )

    def doGlossaryModel(self, glossary):
        self.outLine('glossary model', lineNo=glossary.lineNo)
        for domain in glossary.domainNamed.values():
            self.domain(domain)

    def domain(self, domain):
        self.outLine(
            'domain %s' % domain.name,
            lineNo=domain.lineNo,
            linesBefore=1)
        for entry in domain.entryNamed.values():
            self.entry(entry)

    def entry(self, entry):
        self.outLine(
            '    %s:' % (
                ' '.join([entry.mainTerm] + entry.alternativeTerms)),
            lineNo=entry.lineNo,
            linesBefore=1
         )
        self.description(entry.description)

    def description(self, description):
        # TODO: move this to text printer

        for line in description.lines:
            self.lines(line)

    def lines(self, line):
        _='        '
        for token in line.tokens:
            if isinstance(token, Reference):
                _+=('`%s`' % token.string)
                if token.entry is not None:
                    _+=('!')
                else:
                    _+=('?')
            else:
                _+=token.string
        self.outLine(_,lineNo=line.lineNo)

#TODO: define GlossaryModelSourcePrinter


metamodel.registerModelPrinter(GlossaryModelPrinter)
#TODO: register GlossaryModelSourcePrinter when ready
