# coding=utf-8

"""
Generate a USE OCL specification from a class modeL.
This is currently only a preliminary version.
"""

#TODO: to be continued

import os
import logging
from modelscripts.metamodels.classes import (
    METAMODEL)
from modelscripts.metamodels.classes.associations import Association
from modelscripts.tools.plantuml.engine import PlantUMLEngine

# logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('test.' + __name__)

def indent(prefix,s):
    return '\n'.join([ prefix+l for l in s.split('\n') ])





class ClassPlantUMLPrinter(object):

    def __init__(self, classModel):
        self.classModel = classModel
        self.output = ''


    def do(self, outputFile=None):
        self.output = ''
        self.doModel(self.classModel)
        if outputFile:
            with open(outputFile, 'w') as f:
                f.write(self.output)
        return self.output


    def out(self, s):
        self.output += s

    # def description(self, source_element, indent):
    #     c = source_element.description   # multiple lines
    #     if c is not None:
    #         for line in c:
    #             self.out(indent+'--'+line+'\n')
    #
    # def eolComment(self, source_element):
    #     c = source_element.eolComment
    #     if c is not None:
    #         self.out(' --'+c)
    #     self.out('\n')


    def doModel(self, model):

        self.out('@startuml')
        self.out('\n\n')
        self.out('hide empty members\n')
        self.doPackages(model)

        for e in model.enumerations:
            self.doEnumeration(e)

        for d in model.dataTypes:
            if not d.isCore:
                self.doDataType(d)

        for c in model.classes:
            self.doClass(c)

        for a in model.associations:
            self.doAssociation(a)

        for ac in model.associationClasses:
            self.doAssociationClass(ac)

        # TODO: invariants, operationConditions

        self.out('@enduml')

    def doPackages(self, model):
        if len(model.packages)>=2:
            for package in model.packages:
                if package.name=='':
                    pname='.'
                else:
                    pname=package.name
                self.out('package "%s" {\n' % pname)
                for element in package.elements:
                    if not isinstance(element, Association):
                        self.out('    class %s\n' % element.name)
                self.out('}\n\n')


    def doEnumeration(self, enumeration):
        self.out('enum %s {\n' % enumeration.name)
        self.out(
            '\n'.join(
                ['    %s' % l.name
                 for l in enumeration.literals]
            )
        )
        self.out('\n}\n\n')

    def doDataType(self, datatype):
        self.out('class %s << (D,orchid) >> {\n}\n\n' % datatype.name)

    def doClass(self, class_):

        self.out('class %s [[%s{%s}]]\n' %(
            class_.name,
            'http://something.org/'+class_.name,
            'tooltip for %s' %class_.name
        ))
        self.out("class %s {\n" % class_.name)

        for attribute in class_.attributes:
            self.doAttribute(attribute)

        self.out('--\n')
        for operation in class_.operations:
            self.doOperation(operation)

        self.out('}\n\n')

        for sc in class_.superclasses:
            self.out('%s <|-- %s\n' % (sc.name, class_.name))

        self.out('\n\n')

    def doAssociation(self, association):
        # The rendering is better with vertical layout (--) for
        # associations because roles+assoc names creates a lot
        # # of horizontal text.
        # basic_kindrepr = {
        #         'association' : 'x-->',    # better rendering --
        #         'associationclass' : '--',
        #         'composition': '*--x',
        #         'aggregation': 'o--',
        #     } [association.kind]
        kindrepr={
            ('association','both') : '--',
            ('association','none') : 'x--x',
            ('association','backward') : '<--x',
            ('association','forward') : 'x-->',
            ('associationclass','both') : '--',
            ('associationclass','none') : 'x--x',
            ('associationclass','backward') : '<--x',
            ('associationclass','forward') : 'x-->',
            ('composition','both') : '*--',
            ('composition','none') : '*--x',
            ('composition','backward') : '*--x',
            ('composition','forward') : '*-->',
            ('aggregation','both') : 'o--',
            ('aggregation','none') : 'o--x',
            ('aggregation','backward') : 'o--x',
            ('aggregation','forward') : 'o-->',
        }[ (association.kind, association.navigability)]
        if len(association.roles) >= 3:
            raise NotImplementedError('%s have %i roles. n-ary association are not implemented' % (
                association.name,
                len(association.roles),
            ))
        r1 = association.roles[0]
        r2 = association.roles[1]
        self.out(r1.type.name+' ')
        self.out(self.roleText(r1))
        self.out(' '+kindrepr+' ')
        self.out(self.roleText(r2))
        self.out(' '+r2.type.name+' : ')
        self.out(association.name+' >')
        # self.out('[[http://something{%s -- %s -- %s}.]]' % (
        #     self.roleText(r1),
        #     association.name+' >',
        #     self.roleText(r2),
        # ))
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

    def doAssociationClass(self, associationClass):
        self.doAssociation(associationClass)
        self.doClass(associationClass)
        r1 = associationClass.roles[0]
        r2 = associationClass.roles[1]
        self.out('( %s, %s) .. %s\n\n' %(
            r1.type.name,
            r2.type.name,
            associationClass.name
        ))

    def doAttribute(self, attribute):
        self.out('{field} %s %s : %s\n' % (
            '/' if attribute.isDerived else '',
            attribute.name,
            attribute.type.name,
        ))

    def doOperation(self, operation):
        self.out('{method}    %s%s\n' % (
            operation.signature,
            ' =' if operation.hasImplementation else ''
        ))
        # if operation.hasImplementation:
        #     self.out(indent('        ',operation.expression)+'\n')
        # for condition in operation.conditions:
        #     self.operationCondition(condition)


    def roleText(self, role):
        return ('"%s..%s %s"' % (
            role.cardinalityMin,
            '*' if role.cardinalityMax is None else role.cardinalityMax,
            role.name,
    ))


    ## TODO: remove code duplication (class, object, usecase)
    def generate(self, pumlFile, finalOutputDir=None, format='svg'):
        """
        Generate directly the .plantuml file and the output (e.g. .svg)
        This is a shorthand method to avoid creating the plantUMLEngine
        apart. OK if only one kind of generation is needed.
        :param pumlFile: the name of the .puml file to be saved
        :param format: the format (e.g. svg)
        :param finalOutputDir: the place where the final output will be.
        """
        self.do(pumlFile)
        puml_engine=PlantUMLEngine(checks=False)
        puml_engine.generate(
            pumlFile=pumlFile,
            format=format,
            finalOutputDir=finalOutputDir)


METAMODEL.registerDiagramPrinter(ClassPlantUMLPrinter)