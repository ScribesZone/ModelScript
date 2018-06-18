# coding=utf-8
import os
import logging
from modelscripts.tools.graphviz import MDigraph, imagePath
from modelscripts.metamodels.usecases import METAMODEL


class UsecaseGraphvizPrinter(object):

    def __init__(self, usecaseModel):
        self.usecaseModel = usecaseModel
        self.graph=None

    def do(self):
        self.graph=MDigraph('G')
        self._gen_model()

    def _gen_model(self):

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

        self.graph.attr(rankdir='LR')
        self.graph.attr('node', shape='box', height='0.0',
               style='filled', fillcolor='moccasin',
               fontname='Helvetica', fontsize='10')

        for a in self.usecaseModel.actors:
            self.graph.node(
                self.graph.id(a, prefixId='actor'),
                label=_actor_struct(a.name),
                shape='plaintext',
                style='')

        for u in self.usecaseModel.system.usecases:
            # self._out('usecase %s\n' % u.name)
            self.graph.node(
                self.graph.id(u, prefixId='usecase'),
                shape='oval',
                label=u.name)

            for a in u.actors:
                self.graph.edge(
                    self.graph.id(a), self.graph.id(u)
                    )

    def generate(self, gvFile, format='png'):
        self.do()
        self.graph.format=format
        self.graph.render(
            filename=os.path.basename(gvFile),
            directory=os.path.dirname(gvFile),
            view=False,
            cleanup=False)


METAMODEL.registerDiagramPrinter(UsecaseGraphvizPrinter)