# coding=utf-8
from __future__ import unicode_literals, print_function, absolute_import, \
    division

from typing import Optional

from modelscripts.base.modelprinters import (
    ModelPrinterConfig,
    ModelSourcePrinter
)
from modelscripts.metamodels.classes import (
    METAMODEL,
    ClassModel
)

import logging

from typing import Optional

from modelscripts.base.printers import (
    AbstractPrinterConfig,
    AbstractPrinter)
from modelscripts.base.printers import (
    indent
)
from modelscripts.metamodels.classes import (
    ClassModel
)

__all__ = [
    'UsePrinter',
]
class Config(AbstractPrinterConfig):
    def __init__(self):
        super(Config, self).__init__(
            styled=False,
            displayLineNos=False
        )

class UsePrinter(AbstractPrinter):
    def __init__(self,
                 theModel,
                 config=Config()):
        #type: (ClassModel, Optional[ModelPrinterConfig]) -> None
        super(UsePrinter, self).__init__(config=Config())
        assert theModel is not None
        self.theModel=theModel
        assert isinstance(theModel, ClassModel)

    def save(self, outputFile):
        with open(outputFile, "w") as f:
            f.write(self.output)

    def do(self):
        self.doUseModel(self.theModel)
        return self.output

    def doUseModel(self, model):

        self.outLine('model GenModel')

        for e in model.enumerations:
            self.doEnumeration(e)

        for c in model.plainClasses:
            self.doPlainClass(c)

        for a in model.plainAssociations:
            self.doPlainAssociation(a)

        for ac in model.associationClasses:
            self.doAssociationClass(ac)

        # TODO: invariants, operationConditions, dataTypes
        return self.output

    def doEnumeration(self, enumeration):
        self.out('%s %s {' % (
            'enum',
            enumeration.name))
        for (i,el) in enumerate(enumeration.literals):
            self.doEnumerationLiteral(el)
            if i+1< len(enumeration.literals):
                self.outLine(',')
        self.outLine('}')

    def doEnumerationLiteral(self, enumerationLiteral):
        self.outLine(enumerationLiteral.name, indent=1)
        return self.output

    def doPlainClass(self, class_):
        if class_.superclasses:
            sc = ('< '
                  +','.join(map(
                        lambda s:s.name, class_.superclasses)))
        else:
            sc = ''
        self.outLine(' '.join(filter(None,[
            ('abstract' if class_.isAbstract else None),
            'class',
            class_.name,
            sc])))

        if class_.attributes:
            self.outLine('attributes', indent=1)
            for attribute in class_.attributes:
                self.doAttribute(attribute)

        if class_.operations:
            self.outLine('operations', indent=1)
            for operation in class_.operations:
                self.doOperation(operation)

        # if class_.invariants:
        #     for invariant in class_.invariants:
        #         self.doInvariant(invariant)
        self.outLine('end',
                     linesAfter=1)
        return self.output

    def doPlainAssociation(self, association):
        self.outLine('%s %s' % (
            association.kind,
            association.name,
        ))
        self.outLine('between', indent=1)
        for role in association.roles:
            self.doRole(role)
        self.outLine('end', linesAfter=1)
        return self.output

    def doAssociationClass(self, associationClass):
        if associationClass.superclasses:
            superclass_names = [c.name for c in associationClass.superclasses]
            sc = ' < ' + ','.join(superclass_names)
        else:
            sc = ''
        self.outLine('%s %s%s' % (
            'associationclass',
            associationClass.name,
            sc))
        self.outLine('between', indent=1)
        for role in associationClass.roles:
            self.doRole(role)

        if associationClass.attributes:
            self.outLine('attributes', indent=1)
            for attribute in associationClass.attributes:
                self.doAttribute(attribute)

        if associationClass.operations:
            self.outLine('operations', indent=1)
            for operation in associationClass.operations:
                self.doOperation(operation)

        self.outLine('end', linesAfter=1)
        return self.output

    def doAttribute(self, attribute):
        self.outLine('%s %s %s' % (
                attribute.name,
                ':',
                attribute.type.name),
            indent=2)
        return self.output

    def doOperation(self, operation):
        self.doModelTextBlock(operation.description)
        self.outLine('%s%s' % (
                operation.signature,
                ' =' if operation.hasImplementation
                    else ''),
            indent=1
        )
        if operation.hasImplementation:
            self.outLine(indent('        ',operation.expression)+'\n')
        self.doModelTextBlock(operation.description)

        # for condition in operation.conditions:
        #     self.doOperationCondition(condition)
        return self.output

    # def doInvariant(self, invariant):
    #     if invariant.class_ is None:
    #         prefix_comment = ''
    #         prefix_first = self.kwd('context ')
    #         prefix_rest = '    '
    #     else:
    #         prefix_comment = '    '
    #         prefix_first = '    '
    #         prefix_rest  = '        '
    #     self.doModelTextBlock(invariant.description)
    #     self.outLine('%s%s%s %s:' % (
    #         prefix_first,
    #         self.kwd('existential ') if invariant.isExistential else '',
    #         self.kwd('inv'),
    #         invariant.name,
    #     ))
    #     self.doModelTextBlock(invariant.description)
    #     self.out(indent(prefix_rest, invariant.expression)+'\n')
    #     return self.output

    def doRole(self, role):
        cardinalities=''.join([
            '[',
            str(role.cardinalityMin),
            '..',
            '*' if role.cardinalityMax is None
                else str(role.cardinalityMax),
            ']'])
        self.outLine('%s%s role %s' % (
                     role.type.name,
                     cardinalities,
                     role.name )
                     , indent=2)
        return self.output



# TODO:
# METAMODEL.registerModelPrinter(ClassModelPrinter)
# METAMODEL.registerSourcePrinter(ModelSourcePrinter)

