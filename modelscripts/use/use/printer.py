# coding=utf-8

"""
Generate a USE OCL specification from a modeL.
This is currently only a preliminary version.
"""

import logging

from typing import Optional

from modelscripts.base.modelprinters import (
    ModelPrinter,
    ModelPrinterConfig,
)
from modelscripts.base.printers import (
    indent
)
from modelscripts.metamodels.classes import (
    ClassModel
)
from modelscripts.metamodels.classes.expressions import (
    PreCondition,
)

# logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('test.' + __name__)


__all__ = [
    'UseModelPrinter',
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

    def doModelContent(self):
        super(UseModelPrinter, self).doModelContent()
        self.doUseModel(self.theModel)
        return self.output

    def doDocComment(self, source_element, indent):
        c = source_element.docComment   # multiple lines
        if c is not None:
            for line in c:
                self.out(indent + self.cmt('--' + line) + '\n')
        return self.output

    def doEolComment(self, source_element):
        c=source_element.eolComment
        if c is not None:
            self.out(self.cmt(' --' + c))
            print('PP'*10+c)

        # TODO: this should be arranged if needed
        # self.out('\n')
        return self.output

    def doUseModel(self, model):
        self.doModelTextBlock(model.description)

        if self.theModel.dataTypes is not None:
            for t in self.theModel.dataTypes:
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
        # self.outLine('')

        for e in model.enumerations:
            self.doEnumeration(e)

        for c in model.classes:
            self.doClass(c)

        for a in model.associations:
            self.doAssociation(a)

        for ac in model.associationClasses:
            self.doAssociationClass(ac)

        # TODO: invariants, operationConditions, dataTypes
        return self.output

    def doEnumeration(self, enumeration):
        self.doDocComment(enumeration, '')
        self.out('%s %s {' % (
            self.kwd('enum'),
            enumeration.name))
        self.doEolComment(enumeration)
        self.doModelTextBlock(enumeration.description)
        for (i,el) in enumerate(enumeration.literals):
            self.doEnumerationLiteral(el)
            if i+1< len(enumeration.literals):
                self.outLine(',')
        self.outLine(self.kwd('}'))
        return self.output

    def doEnumerationLiteral(self, enumerationLiteral):
        self.out(enumerationLiteral.name)
        return self.output

    def doClass(self, class_):
        self.doDocComment(class_, '')
        if class_.superclasses:
            sc = (self.kwd('< ')
                  +self.kwd(',').join(map(
                        lambda s:s.name, class_.superclasses)))
        else:
            sc = ''
        self.outLine("%s %s %s " % (
            self.kwd('class'),
            class_.name,
            sc,
            ))
        # self.outLine("%s %s %s %s" % (
        #     self.kwd('class'),
        #     class_.name,
        #     sc,
        #     self.doEolComment(class_)))
        self.doModelTextBlock(class_.description)
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
        return self.output

    def doAssociation(self, association):
        self.doDocComment(association, '')
        self.outLine('%s %s %s' % (
            self.kwd(association.kind),
            association.name,
            self.kwd('between'),
        ))
        self.doModelTextBlock(association.description)
        self.doEolComment(association)
        for role in association.roles:
            self.doRole(role)
        self.outLine(self.kwd('end'), linesAfter=1)
        return self.output

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
        self.doModelTextBlock(associationClass.description)


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
        return self.output

    def doAttribute(self, attribute):
        self.doDocComment(attribute, '    ')
        self.outLine('%s %s %s' % (
                attribute.name,
                self.kwd(':'),
                attribute.type.name),
            indent=1)
        self.doModelTextBlock(attribute.description)
        self.doEolComment(attribute)
        if attribute.isDerived:
            self.outLine('%s %s' % (
                    self.kwd('derive ='),
                    attribute.expression),
                indent=2
            )
        return self.output

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
        self.doModelTextBlock(operation.description)

        for condition in operation.conditions:
            self.doOperationCondition(condition)
        return self.output

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
        self.doModelTextBlock(invariant.description)
        self.doEolComment(invariant)
        self.out(indent(prefix_rest, invariant.expression)+'\n')
        return self.output

    def doRole(self, role):
        self.doDocComment(role, '    ')
        if role.name:
            rn = self.kwd('role ') + role.name
        else:
            rn = ''
        max = '*' if role.cardinalityMax is None else role.cardinalityMax
        self.outLine('    %s[%s..%s] %s'
                 % (role.type.name, role.cardinalityMin, max, rn ))
        self.doModelTextBlock(role.description)
        self.doEolComment(role)
        return self.output

    def doOperationCondition(self, condition):
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
        self.doModelTextBlock(condition.description)
        self.out(indent(prefix_rest,condition.expression)+'\n')
        return self.output


