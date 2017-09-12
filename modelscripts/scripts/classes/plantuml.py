# coding=utf-8

"""
Generate a USE OCL specification from a class modeL.
This is currently only a preliminary version.
"""

#TODO: to be continued

import os
import logging
from modelscripts.metamodels.classes import metamodel
# logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('test.' + __name__)

def indent(prefix,s):
    return '\n'.join([ prefix+l for l in s.split('\n') ])





class ClassDiagramPrinter(object):
    def __init__(self, classModel):
        self.classModel = classModel
        self.output = ''


    def do(self, outputFile=None):
        self.output = ''
        self.model(self.classModel)
        if outputFile:
            with open(outputFile, 'w') as f:
                f.write(self.output)
        return self.output


    def out(self, s):
        self.output += s

    # def docComment(self, source_element, indent):
    #     c = source_element.docComment   # multiple lines
    #     if c is not None:
    #         for line in c:
    #             self.out(indent+'--'+line+'\n')
    #
    # def eolComment(self, source_element):
    #     c = source_element.eolComment
    #     if c is not None:
    #         self.out(' --'+c)
    #     self.out('\n')


    def model(self, model):

        self.out('@startuml')
        self.out('\n\n')

        for e in model.enumerations:
            self.enumeration(e)

        for c in model.classes:
            self.class_(c)

        for a in model.associations:
            self.association(a)

        for ac in model.associationClasses:
            self.associationClass(ac)

        # TODO: invariants, operationConditions

        self.out('@enduml')

    def enumeration(self, enumeration):
        self.out('enum %s {\n' % enumeration.name)
        self.out(
            '\n'.join(
                ['    %s' % l
                 for l in enumeration.literals]
            )
        )
        self.out('\n}\n\n')

    def class_(self, class_):

        self.out('class %s [[%s{%s}]]\n' %(
            class_.name,
            'http://something.org/'+class_.name,
            'tooltoip for %s' %class_.name
        ))
        self.out("class %s {\n" % class_.name)

        for attribute in class_.attributes:
            self.attribute(attribute)


        self.out('--\n')
        for operation in class_.operations:
            self.operation(operation)

        if class_.invariants:
            self.out('--\n')
            for invariant in class_.invariants:
                 self.invariant(invariant)

        self.out('}\n\n')

        for sc in class_.superclasses:
            self.out('%s <|-- %s\n' % (sc.name, class_.name))

        self.out('\n\n')


    def association(self, association):
        kindrepr = {
                'association' : '-',
                'associationclass' : '-',
                'composition': '*--',
                'aggregation': 'o--',
            } [association.kind]
        if len(association.roles) >= 3:
            raise NotImplementedError('%s have %i roles. n-ary association are not implemented' % (
                association.name,
                len(association.roles),
            ))
        r1 = association.roles[0]
        r2 = association.roles[1]
        self.out(r1.type.name+' ')
        # self.out(self.roleText(r1))
        self.out(' '+kindrepr+' ')
        # self.out(self.roleText(r2))
        self.out(' '+r2.type.name+' : ')
        self.out(association.name)
        self.out('[[http://something{%s -- %s -- %s}.]]' % (
            self.roleText(r1),
            association.name,
            self.roleText(r2),
        ))
        self.out('\n\n')
        #     '%s %s %s %s %s : %s\n\n' %(
        #         r1.type.name,
        #         self.role(r1),
        #         kindrepr,
        #         self.role(r2),
        #         r2.type.name,
        #         association.name
        #     )
        # )

    def associationClass(self, associationClass):
        self.association(associationClass)
        self.class_(associationClass)
        r1 = associationClass.roles[0]
        r2 = associationClass.roles[1]
        self.out('( %s, %s) .. %s\n\n' %(
            r1.type.name,
            r2.type.name,
            associationClass.name
        ))




    def attribute(self, attribute):
        self.out('{field} %s %s : %s\n' % (
            '/' if attribute.isDerived else '',
            attribute.name,
            attribute.type.name,
        ))

    def operation(self, operation):
        self.out('{method}    %s%s\n' % (
            operation.signature,
            ' =' if operation.hasImplementation else ''
        ))
        # if operation.hasImplementation:
        #     self.out(indent('        ',operation.expression)+'\n')
        # for condition in operation.conditions:
        #     self.operationCondition(condition)

    def invariant(self, invariant):
        self.out('%sinv %s\n' % (
            'existential ' if invariant.isExistential else '',
            invariant.name,
        ))

    # def invariant(self, invariant):
    #     if invariant.class_ is None:
    #         prefix_comment = ''
    #         prefix_first = 'context '
    #         prefix_rest = '    '
    #     else:
    #         prefix_comment = '    '
    #         prefix_first = '    '
    #         prefix_rest  = '        '
    #     self.docComment(invariant, '    ')
    #     self.out('%s%sinv %s:' % (
    #         prefix_first,
    #         'existential ' if invariant.isExistential else '',
    #         invariant.name,
    #     ))
    #     self.eolComment(invariant)
    #     self.out(indent(prefix_rest,invariant.expression)+'\n')

    def roleText(self, role):
        return ('"%s..%s %s"' % (
            role.cardinalityMin,
            '*' if role.cardinalityMax is None else role.cardinalityMax,
            role.name,
    ))

    # def operationCondition(self, condition):
    #     # if invariant.class_ is None:
    #     #     prefix_comment = ''
    #     #     prefix_first = 'context '
    #     #     prefix_rest = '    '
    #     # else:
    #     prefix_comment = '        '
    #     prefix_first = '        '
    #     prefix_rest  = '            '
    #     keyword='pre' if isinstance(condition,PreCondition) else 'post'
    #     self.docComment(condition, '    ')
    #     self.out('%s%s %s:' % (
    #         prefix_first,
    #         keyword,
    #         condition.name,
    #     ))
    #     self.eolComment(condition)
    #     self.out(indent(prefix_rest,condition.expression)+'\n')

metamodel.registerDiagramPrinter(ClassDiagramPrinter)