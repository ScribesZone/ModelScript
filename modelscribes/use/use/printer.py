# coding=utf-8

"""
Generate a USE OCL specification from a modeL.
This is currently only a preliminary version.
"""

#TODO: to be continued

__all__ = [
    'UseModelPrinter',
    'UseSourcePrinter',
]

import logging

from modelscribes.base.printers import (
    ModelPrinter,
    SourcePrinter,
    indent
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





class UseModelPrinter(ModelPrinter):
    def __init__(self,
                 theModel,
                 summary=False,
                 displayLineNos=True):
        #type: (ClassModel, bool, bool) -> None
        assert theModel is not None
        assert isinstance(theModel, ClassModel)
        super(UseModelPrinter, self).__init__(
            theModel=theModel,
            summary=summary,
            displayLineNos=displayLineNos
        )

    def do(self):
        self.output=''
        self._issues()
        self._model()
        return self.output


    def _docComment(self, source_element, indent):
        c = source_element.docComment   # multiple lines
        if c is not None:
            for line in c:
                self.out(indent+'--'+line+'\n')

    def _eolComment(self, source_element):
        c = source_element.eolComment
        if c is not None:
            self.out(' --'+c)
        self.out('\n')


    def _model(self):

        if self.theModel.basicTypes is not None:
            for t in self.theModel.basicTypes:
                self.out('-- basic type : %s \n' % t.name)

        self._docComment(self.theModel, '')
        self.out('model %s' % self.theModel.name)
        self._eolComment(self.theModel)
        self.out('\n')

        for e in self.theModel.enumerations:
            self._enumeration(e)

        for c in self.theModel.classes:
            self._class(c)

        for a in self.theModel.associations:
            self._association(a)

        for ac in self.theModel.associationClasses:
            self._associationClass(ac)

        # TODO: invariants, operationConditions, basicTypes

    def _enumeration(self, enumeration):
        self._docComment(enumeration, '')
        self.out('enum %s {' % enumeration.name)
        self._eolComment(enumeration)
        self.out(
            ',\n'.join(
                ['    %s' % l
                 for l in enumeration.literals]
            )
        )
        self.out('\n}\n\n')

    def _class(self, class_):
        self._docComment(class_, '')
        if class_.superclasses:
            sc = '< '+','.join(map(lambda s:s.name, class_.superclasses))
        else:
            sc = ''
        self.out("class %s %s" % (class_.name, sc))
        self._eolComment(class_)

        if class_.attributes:
            self.out('attributes\n')
            for attribute in class_.attributes:
                self._attribute(attribute)

        if class_.operations:
            self.out('operations\n')
            for operation in class_.operations:
                self._operation(operation)

        if class_.invariants:
            for invariant in class_.invariants:
                self._invariant(invariant)

        self.out('end\n\n')


    def _association(self, association):
        self._docComment(association, '')
        self.out('%s %s between' % (association.kind, association.name))
        self._eolComment(association)
        for role in association.roles:
            self._role(role)
        self.out('end\n\n')


    def _associationClass(self, associationClass):
        self._docComment(associationClass, '')
        if associationClass.superclasses:
            superclass_names = [c.name for c in associationClass.superclasses]
            sc = ' < ' + ','.join(superclass_names)
        else:
            sc = ''
        self.out('associationclass %s%s between'
                 % (associationClass.name, sc))
        self._eolComment(associationClass)


        for role in associationClass.roles:
            self._role(role)

        if associationClass.attributes:
            self.out('attributes\n')
            for attribute in associationClass.attributes:
                self._attribute(attribute)

        if associationClass.operations:
            self.out('operations\n')
            for operation in associationClass.operations:
                self._operation(operation)

        self.out('end\n\n')


    def _attribute(self, attribute):
        self._docComment(attribute, '    ')
        self.out('    %s : %s' % (attribute.name, attribute.type.name))
        self._eolComment(attribute)
        if attribute.isDerived:
            self.out('        derive =')
            self.out(attribute.expression)


    def _operation(self, operation):
        self._docComment(operation, '    ')
        self.out('    %s%s' % (
            operation.signature,
            ' =' if operation.hasImplementation else ''
        ))
        self._eolComment(operation)
        if operation.hasImplementation:
            self.out(indent('        ',operation.expression)+'\n')
        for condition in operation.conditions:
            self._operationCondition(condition)


    def _invariant(self, invariant):
        if invariant.class_ is None:
            prefix_comment = ''
            prefix_first = 'context '
            prefix_rest = '    '
        else:
            prefix_comment = '    '
            prefix_first = '    '
            prefix_rest  = '        '
        self._docComment(invariant, '    ')
        self.out('%s%sinv %s:' % (
            prefix_first,
            'existential ' if invariant.isExistential else '',
            invariant.name,
        ))
        self._eolComment(invariant)
        self.out(indent(prefix_rest, invariant.expression)+'\n')

    def _role(self, role):
        self._docComment(role, '    ')
        if role.name:
            rn = 'role '+role.name
        else:
            rn = ''
        max = '*' if role.cardinalityMax is None else role.cardinalityMax
        self.out('    %s[%s..%s] %s'
                 % (role.type.name, role.cardinalityMin, max, rn ))
        self._eolComment(role)

    def _operationCondition(self, condition):
        prefix_first = '        '
        prefix_rest  = '            '
        keyword='pre' if isinstance(condition,PreCondition) else 'post'
        self._docComment(condition, '    ')
        self.out('%s%s %s:' % (
            prefix_first,
            keyword,
            condition.name,
        ))
        self._eolComment(condition)
        self.out(indent(prefix_rest,condition.expression)+'\n')


class UseSourcePrinter(SourcePrinter):

    def __init__(self,
                 theSource,
                 summary=False,
                 displayLineNos=True):
        super(UseSourcePrinter, self).__init__(
            theSource=theSource,
            summary=summary,
            displayLineNos=displayLineNos)

    def do(self):
        self.output=''
        if self.theSource.model is not None:
            p=UseModelPrinter(
                theModel=self.theSource.model,
                summary=self.summary,
                displayLineNos=self.displayLineNos
            ).do()
            self.out(p)
        else:
            self._issues()
        return self.output




