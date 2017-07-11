# coding=utf-8

"""
Generate a USE OCL specification from a class modeL.
This is currently only a preliminary version.
"""

#TODO: to be continued

import os
import logging
from pyuseocl.metamodel.classes import PreCondition, PostCondition

# logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('test.' + __name__)

def indent(prefix,s):
    return '\n'.join([ prefix+l for l in s.split('\n') ])




class Generator(object):
    def __init__(self, system):
        self.system = system
        self.output = ''


    def do(self, outputFile=None):
        self.output = ''
        self.genSystem()
        if outputFile:
            with open(outputFile, 'w') as f:
                f.write(self.output)
        return self.output


    def out(self, s):
        self.output += s

    def genSystem(self):

        self.out('@startuml')
        self.out('\n\n')
        self.out('skinparam packageStyle rectangle\n')
        self.out('left to right direction\n')

        for a in self.system.actorNamed.values():
            self.out('actor %s\n' % a.name)

        self.out('rectangle %s {\n' % self.system.name)
        for u in self.system.usecaseNamed.values():
            self.out('usecase %s\n' % u.name)
            for a in u.actors:
                self.out('%s -- %s\n' % (
                    a.name,
                    u.name,
                ))

        self.out('}\n')
        self.out('@enduml\n')

