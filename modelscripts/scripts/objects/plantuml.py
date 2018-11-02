# coding=utf-8

import os
import logging
import codecs

from modelscripts.metamodels.objects import (
    METAMODEL
)
from modelscripts.tools.plantuml.engine import PlantUMLEngine

# logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('test.' + __name__)

def indent(prefix,s):
    return '\n'.join([ prefix+l for l in s.split('\n') ])


class ObjectPlantUMLPrinter(object):

    def __init__(self, state):
        self.state = state
        self.output = ''


    def do(self, outputFile=None):
        self.output = ''
        self.genState()
        if outputFile:
            with codecs.open(outputFile, 'w', "utf-8") as f:
                f.write(self.output)
        return self.output


    def out(self, s):
        self.output += s


    def genState(self):

        self.out('@startuml')
        self.out('\n\n')

        for o in self.state.objects:
            self.doObject(o)

        for l in self.state.links:
            self.doLink(l)

        for lo in self.state.linkObjects:
            self.doLinkObject(lo)

        self.out('@enduml')

    def doObject(self, o):
        print('$'*30+str(type(o)))
        _header='"%s : %s" as %s' % (
            '' if o.name is None else o.name,
            o.class_.name,
            o.name,
        )
        if len(o.slotNames)>0:
            self.out('object %s {\n' % _header)
            for slot_name in o.slotNames:
                self.out('    %s = %s\n' % (
                    slot_name,
                    unicode(o.slot(slot_name).simpleValue)))
            self.out('}\n\n')
        else:
            self.out('object %s\n' % _header)


    def doLink(self, l):
        aname=l.association.name
        self.out('%s -- %s %s \n' % (
            l.sourceObject.name,
            l.targetObject.name,
            "" if aname is None else ": "+aname,
        ))


    def doLinkObject(self, lo):
        self.doObject(lo)
        aname=lo.classifier.name
        for r in lo.roles:
            self.out('%s .. %s %s \n' % (
                lo.name,
                r.uid,
                "" if aname is None else ": "+aname,
            ))

    #TODO:4 remove code duplication (class, object, usecase)
    # This method is the same as the in classes/plantuml.py ...
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


METAMODEL.registerDiagramPrinter(ObjectPlantUMLPrinter)