# coding=utf-8

"""
Generate a USE OCL specification from a modeL.
This is currently only a preliminary version.
"""

from typing import Optional

import logging

from modelscribes.base.printers import (
    indent
)
from modelscribes.base.styles import Styles
from modelscribes.scripts.base.printers import (
    ModelPrinter,
    ModelSourcePrinter,
    ModelPrinterConfig,
)

from modelscribes.metamodels.classes import (
    ClassModel
)
from modelscribes.metamodels.classes.expressions import (
    PreCondition,
    PostCondition,
)

# logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('test.' + __name__)


__all__ = [
    'UseModelPrinter',
    'UseSourcePrinter',
]

class UseModelPrinter(ModelPrinter):
    def __init__(self,
                 theModel,
                 config=None):
        #type: (ClassModel, Optional[ModelPrinterConfig]) -> None
        assert theModel is not None
        assert isinstance(theModel, ClassModel)
        super(UseModelPrinter, self).__init__(
            theModel=theModel,
            config=config
        )

    # def __init__(self,
    #              theModel,
    #              summary=False,
    #              displayLineNos=True):
    #     #type: (ClassModel, bool, bool) -> None
    #
    #     super(UseModelPrinter, self).__init__(
    #         theModel=theModel,
    #         summary=summary,
    #         displayLineNos=displayLineNos
    #     )

    # def do(self):
    #     self.output=''
    #     self._issues()
    #     self._model()
    #     return self.output

    def doModelContent(self):
        super(UseModelPrinter, self).doModelContent()
        self.doUseModel(self.theModel)
        return self.output

    def doDocComment(self, source_element, indent):
        c = source_element.docComment   # multiple lines
        if c is not None:
            for line in c:
                self.out(indent + self.cmt('--' + line) + '\n')

    def doEolComment(self, source_element):
        c = source_element.eolComment
        if c is not None:
            self.out(self.cmt(' --' + c))
        # TODO: this should be arranged if needed
        # self.out('\n')

    def doUseModel(self, model):

        if self.theModel.basicTypes is not None:
            for t in self.theModel.basicTypes:
                self.outLine(
                    self.cmt('-- basic type : %s') % t.name)

        #TODO: Add again management of doccomment for model
        # Model does not inherit anymore from doccomment
        # but it still make sense to add comment for them
        # self.doDocComment(self.theModel, '')

        #TODO: Add again management of eolcomment for model
        # Model does not inherit anymore from doccomment
        # but it still make sense to add comment for them
        # self.doDocComment(self.theModel, '')
        # self.doEolComment(self.theModel)
        self.outLine('')

        for e in model.enumerations:
            self.doEnumeration(e)

        for c in model.classes:
            self.doClass(c)

        for a in model.associations:
            self.doAssociation(a)

        for ac in model.associationClasses:
            self.doAssociationClass(ac)

        # TODO: invariants, operationConditions, basicTypes

    def doEnumeration(self, enumeration):
        self.doDocComment(enumeration, '')
        self.outLine('%s %s { %s' % (
            self.kwd('enum'),
            enumeration.name,
            self.doEolComment(enumeration)))
        for l in enumeration.literals:
            self.outLine(l, indent=1)
        self.outLine(self.kwd('}'))
        # self.out(
        #     ',\n'.join(
        #         ['    %s' % l
        #          for l in enumeration.literals]
        #     )
        # )
        # self.out('\n}\n\n')

    def doClass(self, class_):
        self.doDocComment(class_, '')
        if class_.superclasses:
            sc = (self.kwd('< ')
                  +self.kwd(',').join(map(
                        lambda s:s.name, class_.superclasses)))
        else:
            sc = ''
        self.outLine("%s %s %s %s" % (
            self.kwd('class'),
            class_.name,
            sc,
            self.doEolComment(class_)))

        if class_.attributes:
            self.outLine(self.kwd('attributes'))
            for attribute in class_.attributes:
                self.doAttribute(attribute)

        if class_.operations:
            self.outLine(self.kwd('operations'))
            for operation in class_.operations:
                self.doOperation(operation)

        if class_.invariants:
            for invariant in class_.invariants:
                self.doInvariant(invariant)

        self.outLine(self.kwd('end'),
                     linesAfter=1)


    def doAssociation(self, association):
        self.doDocComment(association, '')
        self.outLine('%s %s %s' % (
            self.kwd(association.kind),
            association.name,
            self.kwd('between'),
        ))
        self.doEolComment(association)
        for role in association.roles:
            self.doRole(role)
        self.outLine(self.kwd('end'), linesAfter=1)


    def doAssociationClass(self, associationClass):
        self.doDocComment(associationClass, '')
        if associationClass.superclasses:
            superclass_names = [c.name for c in associationClass.superclasses]
            sc = self.kwd(' < ') + self.kwd(',').join(superclass_names)
        else:
            sc = ''
        self.out('%s %s%s %s' % (
            self.kwd('associationclass'),
            associationClass.name,
            sc,
            self.kwd('between')))
        self.doEolComment(associationClass)


        for role in associationClass.roles:
            self.doRole(role)

        if associationClass.attributes:
            self.outLine(self.kwd('attributes'))
            for attribute in associationClass.attributes:
                self.doAttribute(attribute)

        if associationClass.operations:
            self.outLine(self.kwd('operations'))
            for operation in associationClass.operations:
                self.doOperation(operation)

        self.outLine(self.kwd('end'), linesAfter=1)

    def doAttribute(self, attribute):
        self.doDocComment(attribute, '    ')
        self.outLine('%s %s %s' % (
                attribute.name,
                self.kwd(':'),
                attribute.type.name),
            indent=1)
        self.doEolComment(attribute)
        if attribute.isDerived:
            self.outLine('%s %s' % (
                    self.kwd('derive ='),
                    attribute.expression),
                indent=2
            )


    def doOperation(self, operation):
        self.doDocComment(operation, '    ')
        self.outLine('%s%s' % (
                operation.signature,
                ' =' if operation.hasImplementation
                    else ''),
            indent=1
        )
        self.doEolComment(operation)
        if operation.hasImplementation:
            self.outLine(indent('        ',operation.expression)+'\n')
        for condition in operation.conditions:
            self._operationCondition(condition)


    def doInvariant(self, invariant):
        if invariant.class_ is None:
            prefix_comment = ''
            prefix_first = self.kwd('context ')
            prefix_rest = '    '
        else:
            prefix_comment = '    '
            prefix_first = '    '
            prefix_rest  = '        '
        self.doDocComment(invariant, '    ')
        self.outLine('%s%s%s %s:' % (
            prefix_first,
            self.kwd('existential ') if invariant.isExistential else '',
            self.kwd('inv'),
            invariant.name,
        ))
        self.doEolComment(invariant)
        self.out(indent(prefix_rest, invariant.expression)+'\n')

    def doRole(self, role):
        self.doDocComment(role, '    ')
        if role.name:
            rn = self.kwd('role ') + role.name
        else:
            rn = ''
        max = '*' if role.cardinalityMax is None else role.cardinalityMax
        self.outLine('    %s[%s..%s] %s'
                 % (role.type.name, role.cardinalityMin, max, rn ))
        self.doEolComment(role)

    def _operationCondition(self, condition):
        prefix_first = '        '
        prefix_rest  = '            '
        keyword='pre' if isinstance(condition,PreCondition) else 'post'
        self.doDocComment(condition, '    ')
        self.outLine('%s%s %s:' % (
            prefix_first,
            self.kwd(keyword),
            condition.name,
        ))
        self.doEolComment(condition)
        self.out(indent(prefix_rest,condition.expression)+'\n')

# # TODO: to be replaced by a generic version
# class UseSourcePrinter(SourcePrinter):
#
#     def __init__(self,
#                  theSource,
#                  summary=False,
#                  displayLineNos=True):
#         super(UseSourcePrinter, self).__init__(
#             theSource=theSource,
#             summary=summary,
#             displayLineNos=displayLineNos)
#
#     def do(self):
#         self.output=''
#         if self.theSource.isValid:
#             p=UseModelPrinter(
#                 theModel=self.theSource.model,
#                 summary=self.summary,
#                 displayLineNos=self.displayLineNos
#             ).do()
#             self.out(p)
#         else:
#             self._issues()
#         return self.output




