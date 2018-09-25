# coding=utf-8


from collections import OrderedDict
from typing import List, Optional, Dict, Text, Union
from abc import ABCMeta, abstractmethod

from modelscripts.megamodels.elements import SourceModelElement
from modelscripts.base.metrics import Metrics
from modelscripts.megamodels.metamodels import Metamodel
from modelscripts.megamodels.models import (
    Model,
    Placeholder)
from modelscripts.megamodels.dependencies.metamodels import (
    MetamodelDependency
)
from modelscripts.metamodels.permissions.sar import Resource
# used for typing
from modelscripts.metamodels.glossaries import (
    GlossaryModel,
    METAMODEL as GLOSSARY_METAMODEL
)
from modelscripts.metamodels.tasks import (
    TaskModel,
    METAMODEL as TASK_METAMODEL
)
from modelscripts.metamodels.textblocks import (
    TextBlock
)

__all__=(
    'AUIModel',
    #TODO:3 Add 'Space', 'Link' and 'Concept'
)


class AUIModel(Model):

    def __init__(self):
        super(AUIModel, self).__init__()

        self._spaceNamed = OrderedDict()
        # type: Dict[Text, Space]

        self._glossaryModel='**not yet**'
        #type: Union[Text, Optional[GlossaryModel]]
        # will be set to the glossary model if any or None

        self._taskModel='**not yet**'
        #type: Union[Text, Optional[TaskModel]]
        # will be set to the class model if any or None

    @property
    def glossaryModel(self):
        #type: ()-> GlossaryModel
        if self._glossaryModel is '**not yet**':
            self._glossaryModel=self.theModel(GLOSSARY_METAMODEL)
        return self._glossaryModel

    @property
    def taskModel(self):
        #type: ()-> TaskModel
        if self._taskModel is '**not yet**':
            self._taskModel=self.theModel(TASK_METAMODEL)
        return self._taskModel

    def space(self, name):
        if name in self._spaceNamed:
            return self._spaceNamed[name]
        else:
            return None

    @property
    def spaces(self):
        #type: () -> List[Space]
        return self._spaceNamed.values()

    @property
    def metrics(self):
        #type: () -> Metrics
        ms=super(AUIModel, self).metrics
        ms.addList((
            ('space', len(self.spaces)),
        ))
        return ms

    @property
    def metamodel(self):
        #type: () -> Metamodel
        return METAMODEL


METAMODEL = Metamodel(
    id='au',
    label='aui',
    extension='.aus',
    modelClass=AUIModel
)
MetamodelDependency(
    sourceId='au',
    targetId='gl',
    optional=True,
    multiple=True,
)
MetamodelDependency(
    sourceId='au',
    targetId='cl',
    optional=True,
    multiple=True,
)