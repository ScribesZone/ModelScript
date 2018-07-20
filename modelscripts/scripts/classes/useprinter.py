# coding=utf-8
from __future__ import unicode_literals, print_function, absolute_import, \
    division

from typing import Optional, Dict
from collections import OrderedDict
from modelscripts.base.modelprinters import (
    ModelPrinterConfig,
    ModelSourcePrinter
)
from modelscripts.metamodels.classes import (
    METAMODEL,
    ClassModel
)
from modelscripts.base.grammars import (
    AST
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
    ClassModel)
__all__ = [
    'UsePrinter',
]
class TextConfig(AbstractPrinterConfig):
    def __init__(self):
        super(TextConfig, self).__init__(
            styled=False,
            displayLineNos=False
        )

class UsePrinter(AbstractPrinter):

    def __init__(self,
                 theModel):
        #type: (ClassModel) -> None
        super(UsePrinter, self).__init__(config=TextConfig())

        self._oclLineToClassModelElement=OrderedDict()
        #type: Dict[int, 'ClassModelElement']
        # for a given line in the generated .use, the
        # OCLLine object corresponding
        # Only line that corresponds to the OCLLine are stored.
        assert theModel is not None
        self.theModel=theModel
        assert isinstance(theModel, ClassModel)

    def _putElement(self, element, useLine=None):
        """
        Associate the element to the current line number with
        respect to the current output.
        """
        # If various elements are at the same line, the last wins
        # This should not be a problem
        assert element is not None
        use_line=self.currentLineNo if useLine is None else useLine
        self._oclLineToClassModelElement[use_line]=element
        element.useOCLLineNo=use_line
        return AST.nodeLine(element.astNode)

    def getElement(self, useLineNo):
        if useLineNo not in self._oclLineToClassModelElement:
            return None
        else:
            return self._oclLineToClassModelElement[useLineNo]

    def getCLSLine(self, useLineNo):
        element=self.getElement(useLineNo)
        if element is None:
            return None
        else:
            return AST.nodeLine(element.astNode)

    def do(self):
        self.doUseModel(self.theModel)
        return self.output

    def doUseModel(self, model):

        self.outLine('model GenModel')

        # Skip
        #   - packages
        #   - datatypes

        for e in model.enumerations:
            self.doEnumeration(e)

        for c in model.plainClasses:
            self.doPlainClass(c)

        for a in model.plainAssociations:
            self.doPlainAssociation(a)

        for ac in model.associationClasses:
            self.doAssociationClass(ac)

        self.outLine('\nconstraints\n')
        for i in model.invariants:
            self.doInvariant(i)

        return self.output

    def doEnumeration(self, enumeration):
        enum_line=self._putElement(enumeration)
        self.outLine('%s %s { --<<< %i' % (
            'enum',
            enumeration.name,
            enum_line))
        for (i,el) in enumerate(enumeration.literals):
            sep=',' if i+1< len(enumeration.literals) else ''
            self.doEnumerationLiteral(el, sep)
        self.outLine('} --<<< %s (bottom)' % enum_line)

    def doEnumerationLiteral(self, enumerationLiteral, sep):
        literal_line=self._putElement(enumerationLiteral)
        self.outLine('%s%s --<<< %i' % (
            enumerationLiteral.name,
            sep,
            literal_line),
            indent=1)
        return self.output

    def doPlainClass(self, class_):
        enum_line=self._putElement(class_)
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
            sc,
            ' --<<< %i' % enum_line])))

        if class_.ownedAttributes:
            self.outLine(
                'attributes --<<< %i (+1?)' % (enum_line)
                , indent=1)
            for attribute in class_.ownedAttributes:
                self.doAttribute(attribute)

        self.outLine('end -- <<< %i (bottom)' % enum_line)
        return self.output

    def doAttribute(self, attribute):
        att_line=self._putElement(attribute)
        self.outLine('%s %s %s --<<< %i' % (
                attribute.name,
                ':',
                attribute.type.name,
                att_line),
            indent=2)
        return self.output

    def doPlainAssociation(self, association):
        assoc_line=self._putElement(association)
        self.outLine('%s %s --<<< %i' % (
            association.kind,
            association.name,
            assoc_line
        ))
        self.outLine('between --<<< %i (+1?)' % (
            assoc_line+1),
            indent=1)
        for role in association.roles:
            self.doRole(role)
        self.outLine('end --<<< %i (bottom)' % assoc_line)
        return self.output

    def doRole(self, role):
        role_line=self._putElement(role)
        cardinalities=''.join([
            '[',
            str(role.cardinalityMin),
            '..',
            '*' if role.cardinalityMax is None
                else str(role.cardinalityMax),
            ']'])
        self.outLine('%s%s role %s --<<< %i' % (
                     role.type.name,
                     cardinalities,
                     role.name,
                     role_line)
                     , indent=2)
        return self.output

    def doAssociationClass(self, associationClass):
        assocl_line=self._putElement(associationClass)
        if associationClass.superclasses:
            superclass_names = [c.name for c in associationClass.superclasses]
            sc = ' < ' + ','.join(superclass_names)
        else:
            sc = ''
        self.outLine('%s %s%s --<<< %i' % (
            'associationclass',
            associationClass.name,
            sc,
            assocl_line))
        self.outLine('between', indent=1)
        for role in associationClass.roles:
            self.doRole(role)

        if associationClass.attributes:
            self.outLine('attributes', indent=1)
            for attribute in associationClass.attributes:
                self.doAttribute(attribute)

        self.outLine('end --<<< %i (bottom)' % assocl_line)
        return self.output

    def doInvariant(self, invariant):
        for ocl_inv in invariant.oclInvariants:
            self.doOCLInvariant(ocl_inv)
        return self.output

    def doOCLInvariant(self, oclInvariant):
        # skip invariant with no body specified
        if len(oclInvariant.oclLines)>=1:
            context_line=self._putElement(oclInvariant.context)
            self.outLine('context self:%s inv %s : --<<< %i' % (
                oclInvariant.context.class_,
                oclInvariant.name,
                context_line))
            for ocl_line in oclInvariant.oclLines:
                self.doOCLLine(ocl_line)
        return self.output

    def doOCLLine(self, oclLine):
        line_cls = AST.nodeLine(oclLine.astNode)
        oclLine.useOCLLineNo=line_cls
        # print('##'*10,str(oclLine),str())
        self._putElement(oclLine)
        self.outLine('%s -- <<< %i' % (
            oclLine.textLine,
            line_cls),
            indent=1)


# TODO:
# METAMODEL.registerModelPrinter(ClassModelPrinter)
# METAMODEL.registerSourcePrinter(ModelSourcePrinter)

