# coding=utf-8

"""
Generate a usecase model from a usecase script.
"""

from __future__ import (
    unicode_literals, print_function, absolute_import, division
)

import os

from typing import Text

from modelscripts.base.grammars import (
    # ModelSourceAST, \
    # ASTBasedModelSourceFile,
    ASTNodeSourceIssue
)
from modelscripts.base.issues import (
    Levels,
)
from modelscripts.metamodels.tasks import (
    TaskModel,
    Task,
    TaskDecomposition,
    METAMODEL
)
from modelscripts.megamodels.metamodels import Metamodel

from modelscripts.megamodels.sources import (
    ASTBasedModelSourceFile
)
from modelscripts.scripts.textblocks.parser import (
    astTextBlockToTextBlock
)

__all__=(
    'TaskModelSource'
)

DEBUG=0

ISSUES={
    'DECOMPO_ROOT':'ta.syn.Task.RootDecompo',
    'NO_DECOMPO':'ta.syn.Task.SubDecompo',
    'WRONG_DECOMPO':'ta.syn.Task.WrongDecompo',
    # 'ACTOR_NO_SUPER':'us.syn.Actor.NoSuper',
    # 'USECASE_TWICE': 'us.syn.Usecase.Twice'
}
def icode(ilabel):
    return ISSUES[ilabel]


class TaskModelSource(ASTBasedModelSourceFile):

    def __init__(self, taskFileName):
        #type: (Text) -> None
        this_dir=os.path.dirname(os.path.realpath(__file__))
        print('KK'*40)
        super(TaskModelSource, self).__init__(
            fileName=taskFileName,
            grammarFile=os.path.join(this_dir, 'grammar.tx')
        )



    @property
    def taskModel(self):
        #type: () -> TaskModel
        m=self.model #type: TaskModel
        return m


    @property
    def metamodel(self):
        #type: () -> Metamodel
        return METAMODEL


    def fillModel(self):

        def define_task(task_node, super_task):

            #------------- Deal with parent_decomposition --------
            # This is non trivial because the decomposition is
            # logically associated with super task (and this is
            # like that in the metamodel), but in the syntax
            # it is defined in front each subclasses.
            # All decomposition indicators have to be the same
            # for subtasks.
            parent_decomposition = task_node.parentDecomposition
            if super_task is None:
                # This is the root node, just check that it has
                # no parent decomposition indicator
                if parent_decomposition is not None:
                    ASTNodeSourceIssue(
                        code=icode('DECOMPO_ROOT'),
                        astNode=task_node,
                        level=Levels.Error,
                        message=(
                            'The root task "%s" cannot be preceded'
                            ' by a decomposition marker ("%s").'
                            ' Ignored.' % (
                                task_node.name,
                                parent_decomposition)))
                # nothing to do.

            else:
                # This is a subtask.

                # Check that the decomposition indicator is there
                if (parent_decomposition is None):
                    ASTNodeSourceIssue(
                        code=icode('NO_DECOMPO'),
                        astNode=task_node,
                        level=Levels.Error,
                        message=(
                            'Decomposition marker missing in '
                            'subtask "%s"'
                            ' Assuming "sequential".' % (
                                task_node.name)))
                    parent_decomp_enum=TaskDecomposition.SEQUENTIAL
                else:
                    parent_decomp_enum={
                        '/' : TaskDecomposition.ALTERNATIVE,
                        '=' : TaskDecomposition.PARALLEL,
                        ':' : TaskDecomposition.SEQUENTIAL
                    }[parent_decomposition]
                # Check that the parent
                if super_task.decomposition is None:
                    super_task.decomposition=parent_decomp_enum
                elif super_task.decomposition==parent_decomp_enum:
                    # repetition of same decomposition: ok
                    pass
                else:
                    ASTNodeSourceIssue(
                        code=icode('WRONG_DECOMPO'),
                        astNode=task_node,
                        level=Levels.Error,
                        message=(
                            'Decomposition marker of subtask "%s"'
                            'is "%s". Cannot be mixed with "%s"'
                            ' Marker ignored' % (
                                task_node.name,
                                parent_decomp_enum,
                                super_task.decomposition
                            )))

            #------------- Deal with current task ----------------
            task=Task(
                taskModel=self.taskModel,
                name=task_node.name,
                decomposition=None, # set by subtask
                decorations=task_node.decorations,
                superTask=super_task,
                astNode=task_node,
            )
            task.description = astTextBlockToTextBlock(
                container=task,
                astTextBlock=task_node.textBlock)

            #------------- Deal with subtasks --------

            for subtask_node in task_node.subtasks:
                define_task(subtask_node, task)

            return task

        print('DD'*100, 'fillModel')

        root=define_task(self.ast.model.rootTask, super_task=None)
        print('DD'*30, root)

        self.taskModel.rootTask=root

    def resolve(self):
        pass



METAMODEL.registerSource(TaskModelSource)
