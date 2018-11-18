# coding=utf-8

from typing import Optional
import os
import logging

from modelscript.metamodels.usecases import METAMODEL
from modelscript.tools.plantuml.engine import PlantUMLEngine

# logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('test.' + __name__)

def indent(prefix,s):
    return '\n'.join([ prefix+l for l in s.split('\n') ])


class UsecasePlantUMLPrinter(object):

    def __init__(self, usecaseModel):
        self.usecaseModel = usecaseModel
        self.output = ''

    def do(self, outputFile=None):
        self.output = ''
        self._genUsecaseModel()
        if outputFile:
            with open(outputFile, 'w') as f:
                f.write(self.output)
        return self.output


    def _out(self, s):
        self.output += s


    def _genUsecaseModel(self):

        self._out('@startuml')
        self._out('\n\n')
        self._out('skinparam packageStyle rectangle\n')
        self._out('left to right direction\n')

        for a in self.usecaseModel.actorNamed.values():
            self._out('actor %s\n' % a.name)

        self._out('rectangle %s {\n' % (
            self.usecaseModel.system.name))

        for u in self.usecaseModel.system.usecases:
            self._out('usecase %s\n' % u.name)
            for a in u.actors:
                self._out('%s -- %s\n' % (
                    a.name,
                    u.name,
                ))

        self._out('}\n')
        self._out('@enduml\n')

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


METAMODEL.registerDiagramPrinter(UsecasePlantUMLPrinter)