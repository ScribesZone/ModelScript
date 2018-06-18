# coding=utf-8
import os
from modelscripts.tools.graphviz import MDigraph, imagePath
from modelscripts.metamodels.usecases import METAMODEL
from modelscripts.scripts.tasks.printer import TaskModelPrinter
from modelscripts.scripts.tasks.parser import ConcreteSyntax
class TaskGraphvizPrinter(object):

    def __init__(self, usecaseModel):
        self.usecaseModel = usecaseModel
        self.graph=None

    def do(self):
        self.graph=MDigraph('G')
        self._gen_usecase_model()

    def _gen_usecase_model(self):

        self.graph.attr(rankdir='LR')
        self.graph.attr('node', shape='box', height='0.0',
               style='filled', fillcolor='yellow',
               fontname='Helvetica', fontsize='10')

        self._gen_task_tree(self.usecaseModel.rootTask)

    def _gen_task_tree(self, task):

        def _struct(name, operators):
            html_version=\
                """<
                   <TABLE BORDER="0" 
                        CELLPADDING="2" CELLBORDER="1" 
                        CELLSPACING="0" BGCOLOR="yellow">
                   <TR><TD>{name}</TD></TR>
                   <TR><TD>A B C</TD></TR>
                   </TABLE>
                   >"""
            struct_version=\
                """
                %s|%s 
                """

            # return (
            #            """<
            #            <TABLE BORDER="0"
            #                 CELLPADDING="2" CELLBORDER="1"
            #                 CELLSPACING="0" BGCOLOR="yellow">
            #            <TR><TD>{name}</TD></TR>
            #            <TR><TD>A B C</TD></TR>
            #            </TABLE>
            #            >"""
            #        ).format(name=actorName)
            return struct_version % (name, operators)

        self.graph.node(
            name=self.graph.id(task),
            label=_struct(
                task.name,
                TaskModelPrinter.postOperators(task)),
            shape='record',
            width = '0', height = '0'
        )
        decom_symbol=ConcreteSyntax.concreteDecomposition(
            task.decomposition)

        for subtask in task.subTasks:
            self._gen_task_tree(subtask)

            if subtask.optional:
                head='odot'
            else:
                head='dot'
            self.graph.edge(
                self.graph.id(task),
                self.graph.id(subtask),
                label=decom_symbol,
                arrowhead=head)

        # for a in self.usecaseModel.actors:
        #     self.graph.node(
        #         m.id(a, prefix='actor'),
        #         label=_actor_struct(a.name),
        #         shape='plaintext',
        #         style='')
        #
        # for u in self.usecaseModel.system.usecases:
        #     # self._out('usecase %s\n' % u.name)
        #     self.graph.node(
        #         m.id(u, prefix='usecase'),
        #         shape='oval',
        #         label=u.name)
        #
        #     for a in u.actors:
        #         self.graph.edge(
        #             m.id(a), m.id(u)
        #             )

    def generate(self, gvFile, format='png'):
        self.do()
        self.graph.format=format
        self.graph.render(
            filename=os.path.basename(gvFile),
            directory=os.path.dirname(gvFile),
            view=False,
            cleanup=False)


METAMODEL.registerDiagramPrinter(TaskGraphvizPrinter)