# coding=utf-8

"""
Generate a USE OCL specification from a class modeL.
This is currently only a preliminary version.
"""

#TODO: to be continued

import os
import logging
from modelscripts.metamodels.objects import (
    METAMODEL
)

# logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('test.' + __name__)

def indent(prefix,s):
    return '\n'.join([ prefix+l for l in s.split('\n') ])




class ObjectDiagramPrinter(object):
    def __init__(self, state):
        self.state = state
        self.output = ''


    def do(self, outputFile=None):
        self.output = ''
        self.genState()
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


    def genState(self):

        self.out('@startuml')
        self.out('\n\n')

        for o in self.state.objects:
            self.object(o)

        for l in self.state.links:
            self.link(l)

        for lo in self.state.linkObjects:
            self.linkObject(lo)

        self.out('@enduml')

    def object(self, o):
        print('$'*30+str(type(o)))
        _header='"%s : %s" as %s' % (
            '' if o.name is None else o.name,
            o.classifier.name,
            o.uid,
        )
        if o.slotNamed:
            self.out('object %s {\n' % _header)
            for (att,val) in o.slotNamed.iteritems(): #TODO: check
                self.out('    %s = %s\n' % (att,val))
            self.out('}\n\n')
        else:
            self.out('object %s\n' % _header)


    def link(self, l):
        if len(l.roles) >= 3:
            raise NotImplementedError(
                'n-ary link not implemented')
        aname=l.classifier.name
        self.out('%s -- %s %s \n' % (
            l.roles[0].uid,
            l.roles[1].uid,
            "" if aname is None else ": "+aname,
        ))


    def linkObject(self, lo):
        if len(lo.roles) >= 3:
            raise NotImplementedError(
                'n-ary link not implemented')
        self.object(lo)
        aname=lo.classifier.name
        for r in lo.roles:
            self.out('%s .. %s %s \n' % (
                lo.uid,
                r.uid,
                "" if aname is None else ": "+aname,
            ))

METAMODEL.registerDiagramPrinter(ObjectDiagramPrinter)