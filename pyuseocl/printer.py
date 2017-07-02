# coding=utf-8

"""
Generate a USE OCL specification from a modeL.
This is currently only a preliminary version.
"""

#TODO: to be continued

__all__ = [
    'UseOCLPrinter',
]

import logging
from pyuseocl.model import PreCondition, PostCondition

# logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('test.' + __name__)

def indent(prefix,s):
    return '\n'.join([ prefix+l for l in s.split('\n') ])

class UseOCLPrinter(object):
    def __init__(self, model):
        self.theModel = model
        self.output = ''


    def do(self):
        self.output = ''
        self.model(self.theModel)
        return self.output


    def out(self, s):
        self.output += s

    def docComment(self, source_element, indent):
        c = source_element.docComment   # multiple lines
        if c is not None:
            for line in c:
                self.out(indent+'--'+line+'\n')

    def eolComment(self, source_element):
        c = source_element.eolComment
        if c is not None:
            self.out(' --'+c)
        self.out('\n')


    def model(self, model):

        if model.basicTypes is not None:
            for t in model.basicTypes:
                self.out('-- basic type : %s \n' % t.name)

        self.docComment(model, '')
        self.out('model %s' % model.name)
        self.eolComment(model)
        self.out('\n')

        for e in model.enumerations:
            self.enumeration(e)

        for c in model.classes:
            self.class_(c)

        for a in model.associations:
            self.association(a)

        for ac in model.associationClasses:
            self.associationClass(ac)

        # TODO: invariants, operationConditions, basicTypes

    def enumeration(self, enumeration):
        self.docComment(enumeration, '')
        self.out('enum %s {' % enumeration.name)
        self.eolComment(enumeration)
        self.out(
            ',\n'.join(
                ['    %s' % l
                 for l in enumeration.literals]
            )
        )
        self.out('\n}\n\n')

    def class_(self, class_):
        self.docComment(class_,'')
        if class_.superclasses:
            sc = '< '+','.join(map(lambda s:s.name, class_.superclasses))
        else:
            sc = ''
        self.out("class %s %s" % (class_.name, sc))
        self.eolComment(class_)

        if class_.attributes:
            self.out('attributes\n')
            for attribute in class_.attributes:
                self.attribute(attribute)

        if class_.operations:
            self.out('operations\n')
            for operation in class_.operations:
                self.operation(operation)

        if class_.invariants:
            for invariant in class_.invariants:
                self.invariant(invariant)

        self.out('end\n\n')


    def association(self, association):
        self.docComment(association, '')
        self.out('%s %s between' % (association.kind, association.name))
        self.eolComment(association)
        for role in association.roles:
            self.role(role)
        self.out('end\n\n')


    def associationClass(self, associationClass):
        self.docComment(associationClass, '')
        if associationClass.superclasses:
            superclass_names = [c.name for c in associationClass.superclasses]
            sc = ' < ' + ','.join(superclass_names)
        else:
            sc = ''
        self.out('associationclass %s%s between'
                 % (associationClass.name, sc))
        self.eolComment(associationClass)


        for role in associationClass.roles:
            self.role(role)

        if associationClass.attributes:
            self.out('attributes\n')
            for attribute in associationClass.attributes:
                self.attribute(attribute)

        if associationClass.operations:
            self.out('operations\n')
            for operation in associationClass.operations:
                self.operation(operation)

        self.out('end\n\n')


    def attribute(self, attribute):
        self.docComment(attribute, '    ')
        self.out('    %s : %s' % (attribute.name, attribute.type.name))
        self.eolComment(attribute)
        if attribute.isDerived:
            self.out('        derive =')
            self.out(attribute.expression)


    def operation(self, operation):
        self.docComment(operation, '    ')
        self.out('    %s%s' % (
            operation.signature,
            ' =' if operation.hasImplementation else ''
        ))
        self.eolComment(operation)
        if operation.hasImplementation:
            self.out(indent('        ',operation.expression)+'\n')
        for condition in operation.conditions:
            self.operationCondition(condition)


    def invariant(self, invariant):
        if invariant.class_ is None:
            prefix_comment = ''
            prefix_first = 'context '
            prefix_rest = '    '
        else:
            prefix_comment = '    '
            prefix_first = '    '
            prefix_rest  = '        '
        self.docComment(invariant, '    ')
        self.out('%s%sinv %s:' % (
            prefix_first,
            'existential ' if invariant.isExistential else '',
            invariant.name,
        ))
        self.eolComment(invariant)
        self.out(indent(prefix_rest,invariant.expression)+'\n')

    def role(self, role):
        self.docComment(role, '    ')
        if role.name:
            rn = 'role '+role.name
        else:
            rn = ''
        max = '*' if role.cardinalityMax is None else role.cardinalityMax
        self.out('    %s[%s..%s] %s'
                 % (role.type.name, role.cardinalityMin, max, rn ))
        self.eolComment(role)

    def operationCondition(self, condition):
        # if invariant.class_ is None:
        #     prefix_comment = ''
        #     prefix_first = 'context '
        #     prefix_rest = '    '
        # else:
        prefix_comment = '        '
        prefix_first = '        '
        prefix_rest  = '            '
        keyword='pre' if isinstance(condition,PreCondition) else 'post'
        self.docComment(condition, '    ')
        self.out('%s%s %s:' % (
            prefix_first,
            keyword,
            condition.name,
        ))
        self.eolComment(condition)
        self.out(indent(prefix_rest,condition.expression)+'\n')


