# coding=utf-8

#TODO: to be continued

from typing import Optional
import os
import logging
from modelscripts.tools.graphviz import Digraph, Mapping, imagePath

from modelscripts.metamodels.usecases import METAMODEL
from modelscripts.tools.plantuml.engine import PlantUMLEngine

# logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('test.' + __name__)

def indent(prefix,s):
    return '\n'.join([ prefix+l for l in s.split('\n') ])


class UsecaseGraphvizPrinter(object):

    def __init__(self, usecaseModel):
        self.usecaseModel = usecaseModel

    def do(self, outputFile=None):
        g=Digraph('G', filename=outputFile)
        self._genUsecaseModel(g)
        g.view()

    def _genUsecaseModel(self, g):

        def _actor_struct(actorName):
            image=imagePath('actor.png')
            return (
                       """<
                       <TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0">
                       <TR><TD><IMG SRC="{image}"/></TD></TR>
                       <TR><TD>{name}</TD></TR>
                       </TABLE>
                       >"""
                   ).format(name=actorName, image=image)

        g.attr(rankdir='LR')
        g.attr('node', shape='box', height='0.0',
               style='filled', fillcolor='moccasin',
               fontname='Helvetica', fontsize='10')

        m=Mapping()

        for a in self.usecaseModel.actors:
            g.node(
                m.id(a, prefix='actor'),
                label=_actor_struct(a.name),
                shape='plaintext',
                style='')

        for u in self.usecaseModel.system.usecases:
            # self._out('usecase %s\n' % u.name)
            g.node(
                m.id(u, prefix='usecase'),
                shape='oval',
                label=u.name)

            for a in u.actors:
                g.edge(
                    m.id(a), m.id(u)
                    )

        # self._out('}\n')
        # self._out('@enduml\n')
    # def generate(self, pumlFile, finalOutputDir=None, format='svg'):
    #     """
    #     Generate directly the .plantuml file and the output (e.g. .svg)
    #     This is a shorthand method to avoid creating the plantUMLEngine
    #     apart. OK if only one kind of generation is needed.
    #     :param pumlFile: the name of the .puml file to be saved
    #     :param format: the format (e.g. svg)
    #     :param finalOutputDir: the place where the final output will be.
    #     """
    #     self.do(pumlFile)
    #     puml_engine=PlantUMLEngine(checks=False)
    #     puml_engine.generate(
    #         pumlFile=pumlFile,
    #         format=format,
    #         outputDir=finalOutputDir)


METAMODEL.registerDiagramPrinter(UsecaseGraphvizPrinter)