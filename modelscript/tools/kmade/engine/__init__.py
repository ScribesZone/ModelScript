# coding=utf-8
"""
Reader and writer of Kmade files (.kxml).
The modality is ignored (seems to be always COGN).
Assume that the content of the kxml file has only one root.
The reader consider only the first task root, and take
the corresponding tree. The rest is ignored.

The observation field is not taken into account yet.
This would imply converting the textblock into a AST textblovk,
that is launching the text block parser. Not so useful anyway
as description are seldom used with kxml.
"""
import sys
import os
from typing import Optional
import xml.etree.ElementTree as ET

# root.tag
# root.text
# root.attrib['id']
# root[2][1]
# root.find('a')
# root.findall('a')
# root.iter('a')

# decomposition:  SEQ, LEAF
# executant: ABS USER SYS INT
from modelscript.base.exceptions import (
    UnexpectedCase)
from modelscript.scripts.textblocks.parser import (
    astTextBlockToTextBlock)
from modelscript.metamodels.tasks import (
    TaskModel,
    TaskDecomposition,
    TaskExecutant,
    Task)
from modelscript.scripts.tasks.printer import (
    TaskModelPrinter)

HEADER='''
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE kmad-model SYSTEM "file:KMADModelJT.dtd">
<kmad-model version="1.3">
    <projects classkmad="projects.Project" id-projects-information="K2" idkmad="K1">
        <projectinformation classkmad="projects.GeneralInformation" idkmad="K2">
            <projectinformation-compagny>MyTheatre_ConfiguReduc</projectinformation-compagny>
        </projectinformation>
    </projects>
'''
FOOTER='''
</kmad-model>
'''


class KmadeConcreteSyntax(object):

    DECOMPOSITION= [
        ('SEQ', TaskDecomposition.SEQUENTIAL),
        ('PAR', TaskDecomposition.PARALLEL),
        ('ALT', TaskDecomposition.ALTERNATIVE),
        ('ENT', TaskDecomposition.NOORDER),
        ('LEAF', TaskDecomposition.ELEMENTARY),
        ('UNK', TaskDecomposition.UNKNOWN),
    ]
    EXECUTANT=[
        ('ABS', TaskExecutant.ABSTRACT),
        ('INT', TaskExecutant.INTERACTION),
        ('USER', TaskExecutant.USER),
        ('SYS', TaskExecutant.SYSTEM),
        ('UNK', TaskExecutant.UNKNOWN)
    ]

    @classmethod
    def _find_forward(cls, pairs, concrete):
        for (c,a) in pairs:
            if c==concrete:
                return a
        raise UnexpectedCase( #raise:TODO:4
            # check how to catch this exception if needed
            '"%s" is unexpected' % concrete)

    @classmethod
    def _find_backward(cls, pairs, abstract):
        for (c,a) in pairs:
            if a==abstract:
                return c
        raise UnexpectedCase( #raise:TODO:4
            # check how to catch this exception if needed
            '"%s" is unexpected' % abstract)

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


class KmadeReader(object):

    def __init__(self, filename):
        self.filename=filename
        self.xmlTree = ET.parse(filename)
        self.root = self.xmlTree.getroot()

    def _task_tree(self, node, model, superTask=None):
        #type: ('ETNode', TaskModel, Optional[Task]) -> Task

        name = node.find('task-name').text

        executant = KmadeConcreteSyntax.abstractExecutant(
            node.find('task-executant').text)
         # modality = node.find('task-modality').text
        optional = node.find('task-optional') == 'true'
        interruptible = node.find('task-interruptible') == 'true'
        decomposition = KmadeConcreteSyntax.abstractDecomposition(
            node.find('task-decomposition').text)

        task=Task(
            taskModel=model,
            name=name,
            executant=executant,
            optional=optional,
            interruptible=interruptible,
            decomposition=decomposition,
            superTask=superTask,
            # description=description, NOT SUPPORTED
            astNode=None,
            lineNo=None
        )
        # Support of observation ->description is not supported yet
        # ---------------------------------------------------------
        # It would look like this :
        # observation = node.find('task-observation').text
        # if observation=='':
        #     description=None
        # else:
        #     description=astTextBlockToTextBlock(
        #         container=task,
        #         SOME PARSING WITH TEXT BLOCK PARSER
        #         )
        for sub_task in node.findall('task'):
            self._task_tree(
                node=sub_task,
                model=model,
                superTask=task)
        return task



    def taskModel(self):
        model=TaskModel()
        root_node=self.root.find('task')
        if root_node is None:
            # The file is empty => we create one node named "EMPTY"
            task=Task(
                taskModel=model,
                name='EMPTY',
                executant=TaskExecutant.UNKNOWN,
                optional=True,
                interruptible=True,
                decomposition=TaskDecomposition.UNKNOWN,
                superTask=None,
                # description=description, NOT SUPPORTED
                astNode=None,
                lineNo=None
            )
            model.rootTask=task
        else:
            root_task=self._task_tree(
                node=root_node,
                model=model,
                superTask=None)
            model.rootTask=root_task
        return model



    def _display_tree(self, node, indent=0):
        id=node.attrib['idkmad']
        name=node.find('task-name').text
        # # numero=int(node.find('task-numero').text)
        observation=node.find('task-observation').text
        executant= KmadeConcreteSyntax.abstractExecutant(
            node.find('task-executant').text)
        modality=node.find('task-modality').text
        optional=node.find('task-optional')=='true'
        interruptible=node.find('task-interruptible')=='true'
        decomposition=KmadeConcreteSyntax.abstractDecomposition(
            node.find('task-decomposition').text)
        _=' '.join([
            ' ' * (indent * 4),
            decomposition,
            name,
            modality,
            executant,
            unicode(optional),
            unicode(interruptible),
            '(#%s)' % str()
        ])
        print(_)
        for child in node.findall('task'):
            self._display_tree(child, indent+1)

    def display(self):
        root_task=self.root.find('task')
        self._display_tree(node=root_task, indent=0)


class KmadeWriter(object):
    # TODO:4 implement writing .kxml file from task model
    pass

if __name__ == '__main__':
    for file in sys.argv:
        if file.endswith('.kxml'):
            if os.path.isfile(file):
                print('PROCESSING %s' % file)
                reader=KmadeReader(file)
                model=reader.taskModel()
                print(TaskModelPrinter(model).doModelContent())
            else:
                print('IGNORING %s (file does not exist)' % file )