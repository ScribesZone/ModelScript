# coding=utf-8
from __future__ import print_function

import collections

from typing import Dict, Text, Optional, List

from modelscripts.base.issues import Issue, Levels
from modelscripts.base.symbols import Symbol
from modelscripts.megamodels.issues import ModelElementIssue
from modelscripts.megamodels.elements import SourceModelElement
from modelscripts.base.metrics import Metrics
from modelscripts.megamodels.metamodels import Metamodel
from modelscripts.megamodels.dependencies.metamodels import (
    MetamodelDependency
)
from modelscripts.megamodels.models import Model

META_CLASSES=(
    'TaskModel',
    'Task',
)

__all__= META_CLASSES


class TaskModel(Model):


    def __init__(self):
        super(TaskModel, self).__init__()

        self.rootTask=None
        #type: Optional[Task]

    @property
    def metamodel(self):
        #type: () -> Metamodel
        return METAMODEL

    @property
    def metrics(self):
        #type: () -> Metrics
        ms=super(TaskModel, self).metrics
        if self.rootTask is not None:
            # rootTask could be None in case of syntactic error
            ms.addList((
                ('task', self.rootTask.taskNb),
                ('task depth', self.rootTask.depth)
            ))
        return ms



class TaskDecomposition(object):
    SEQUENTIAL='sequential'
    PARALLEL='parallel'
    ALTERNATIVE='alternative'
    NOORDER='noorder'
    ELEMENTARY='elementary'
    UNKNOWN='unkown'

class TaskExecutant(object):
    ABSTRACT='abstract'
    INTERACTION='interaction'
    USER='user'
    SYSTEM='system'
    UNKNOWN='unknown'

class Task(SourceModelElement):

    def __init__(self,
                 taskModel,
                 name,
                 executant,
                 # modality ?
                 optional,
                 interruptible,
                 decomposition,
                 superTask=None,
                 description=None,
                 astNode=None,
                 lineNo=None
                 ):
        super(Task, self).__init__(
            model=taskModel,
            name=name,
            astNode=astNode,
            lineNo=lineNo,
            description=description)

        self.executant=executant
        #type: 'TaskExecutantString'

        self.optional=optional
        #type: bool

        self.interruptible=interruptible
        #type: bool

        self.decomposition=decomposition
        #type: 'TaskDecompositionString'
        # The type of the decomposition applied to
        # subtasks (parallel, sequential, ...).
        # If no value is provided it will be set to 'unknown'
        # This value is used by Kmade, but it is also used
        # temporarily by the parser.

        self.superTask=superTask
        #type: Optional[Task]

        self.subTasks=[]
        #type: List[Task]

        if self.superTask is not None:
            self.superTask.subTasks.append(self)

    @property
    def taskNb(self):
        return 1+sum([st.taskNb for st in self.subTasks])

    @property
    def depth(self):
        if len(self.subTasks)==0:
            return 0
        else:
            return 1+max([st.depth for st in self.subTasks])


class ConceptReference(SourceModelElement):

    def __init__(self,
                 task,
                 names,
                 multiple,
                 astNode=None,
                 lineNo=None):
        super(ConceptReference, self).__init__(
            model=task.model,
            name=None,
            astNode=astNode,
            lineNo=lineNo)

        self.task=task
        #type: Task

        self.names=names,
        #type: List[Text]

        self.multiple=multiple
        #type: bool


METAMODEL = Metamodel(
    id='ta',
    label='task',
    extension='.tas',
    modelClass=TaskModel,
    modelKinds=('preliminary', '', 'detailed')
)
MetamodelDependency(
    sourceId='ta',
    targetId='gl',
    optional=True,
    multiple=False,
)

