# coding=utf-8
from __future__ import print_function
from collections import OrderedDict
from typing import List, Optional, Dict, Text, Union
from abc import ABCMeta, abstractmethod

from modelscripts.megamodels.models import Model
from modelscripts.megamodels.metamodels import Metamodel
from modelscripts.megamodels.dependencies.metamodels import (
    MetamodelDependency)
from modelscripts.metamodels.glossaries import (
    GlossaryModel,
    METAMODEL as GLOSSARY_METAMODEL
)

class ParticipantModel(Model):

    def __init__(self):
        super(ParticipantModel, self).__init__()

        self._glossaryModel='**not yet**'
        #type: Union[Text, Optional[GlossaryModel]]
        # will be set to the glossary model if any or None

    @property
    def glossaryModel(self):
        #type: ()-> GlossaryModel
        if self._glossaryModel is '**not yet**':
            self._glossaryModel=self.theModel(GLOSSARY_METAMODEL)
        return self._glossaryModel

    @property
    def metamodel(self):
        #type: () -> Metamodel
        return METAMODEL

METAMODEL = Metamodel(
    id='pa',
    label='participant',
    extension='.pas',
    modelClass=ParticipantModel,
    modelKinds=('preliminary', '', 'detailed')
)
MetamodelDependency(
    sourceId='pa',
    targetId='gl',
    optional=True,
    multiple=False,
)

