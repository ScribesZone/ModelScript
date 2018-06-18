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
    TaskExecutant,
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
    'TaskModelSource',
    'ConcreteSyntax'
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


class ConcreteSyntax(object):

    DECOMPOSITION= [
        (':', TaskDecomposition.SEQUENTIAL),
        ('=', TaskDecomposition.PARALLEL),
        ('<', TaskDecomposition.ALTERNATIVE),
        ('~', TaskDecomposition.NOORDER),
        ('#', TaskDecomposition.ELEMENTARY),
        ('?', TaskDecomposition.UNKNOWN),
    ]
    EXECUTANT=[
        ('A', TaskExecutant.ABSTRACT),
        ('I', TaskExecutant.INTERACTION),
        ('U', TaskExecutant.USER),
        ('S', TaskExecutant.SYSTEM),
        ('?', TaskExecutant.UNKNOWN)
    ]
    CONCRETE_OPTIONAL='O'
    CONCRETE_INTERRUPTIBLE='@'

    @classmethod
    def _find_forward(cls, pairs, concrete):
        for (c,a) in pairs:
            if c==concrete:
                return a
        raise NotImplementedError('"%s" is unexpected' % concrete)

    @classmethod
    def _find_backward(cls, pairs, abstract):
        for (c,a) in pairs:
            if a==abstract:
                return c
        raise NotImplementedError('"%s" is unexpected' % abstract)

    @classmethod
    def abstractDecomposition(cls, concrete):
        return cls._find_forward(cls.DECOMPOSITION, concrete)

    @classmethod
    def concreteDecomposition(cls, abstract):
        return cls._find_backward(cls.DECOMPOSITION, abstract)

    @classmethod
    def abstractExecutant(cls, concrete):
        return cls._find_forward(cls.EXECUTANT, concrete)

    @classmethod
    def concreteExecutant(cls, abstract):
        return cls._find_backward(cls.EXECUTANT, abstract)



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
                # no parent decomposition indicator in the concrete
                # syntax
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

                # Check that the decomposition indicator is mentionned
                # in the AST
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
                    parent_decomp_enum=(
                        ConcreteSyntax.abstractDecomposition(
                            parent_decomposition))
                # the decomposition indicator (for the parent) is
                # mentionned in the AST. So add it to the parent.
                if (super_task.decomposition
                    is TaskDecomposition.ELEMENTARY):
                    # First time, this is ok.
                    # Note that the node are set to unknown by default
                    # this is why this is the first time.
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

            #-- executant
            if (task_node.decorations is None
                or task_node.decorations.executant is None):
                executant=TaskExecutant.UNKNOWN
            else:
                executant=ConcreteSyntax.abstractExecutant(
                            task_node.decorations.executant)

            #-- optional
            optional=(
                task_node.decorations is not None and
                task_node.decorations.optional is not None)

            #-- interruptible
            interruptible=(
                task_node.decorations is not None and
                task_node.decorations.interruptible is not None)

            #-- decomposition

            # At this time we don't know if this task will have
            # child, so we assign ELEMENTARY as its decomposition.
            # This will be changed by this parser when children are
            # discovered (see above).
            this_node_decomposition=TaskDecomposition.ELEMENTARY

            task=Task(
                taskModel=self.taskModel,
                name=task_node.name,
                executant=executant,
                optional=optional,
                interruptible=interruptible,
                decomposition=TaskDecomposition.ELEMENTARY,
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


        root=define_task(self.ast.model.rootTask, super_task=None)

        self.taskModel.rootTask=root

    def resolve(self):
        pass



METAMODEL.registerSource(TaskModelSource)
