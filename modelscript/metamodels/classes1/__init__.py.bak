# coding=utf-8
from __future__ import print_function
from collections import OrderedDict
from typing import List, Optional, Dict, Text, Union
from abc import ABCMeta, abstractmethod

from modelscript.megamodels.models import Model
from modelscript.megamodels.metamodels import Metamodel
from modelscript.megamodels.dependencies.metamodels import (
    MetamodelDependency)
from modelscript.metamodels.glossaries import (
    GlossaryModel,
    METAMODEL as GLOSSARY_METAMODEL
)

class Class1Model(Model):

    def __init__(self):
        super(Class1Model, self).__init__()

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
    id='c1',
    label='class1',
    extension='.cl1',
    modelClass=Class1Model,
    modelKinds=('preliminary', '', 'detailed')
)
MetamodelDependency(
    sourceId='c1',
    targetId='gl',
    optional=True,
    multiple=False,
)

