# coding=utf-8

"""
Provide a global registery of:
- metamodels,
- models,
- metamodel dependencies
- model dependencies
"""
from abc import ABCMeta, abstractproperty

from typing import List, Optional

from modelscripts.megamodels.dependencies import Dependency
from modelscripts.megamodels.megamodels._registries.metamodels import _MetamodelRegistry
# from modelscripts.megamodels.dependencies.metamodels import MetamodelDependency
# from modelscripts.megamodels.dependencies.models import ModelDependency
# To avoid circular dependencies
# from modelscripts.megamodels.models import Model
# from modelscripts.megamodels.metamodels import Metamodel
from modelscripts.megamodels.megamodels._registries.models import _ModelRegistry
from modelscripts.megamodels.megamodels._registries.sources import _SourceFileRegistry
from modelscripts.base.exceptions import (
    MethodToBeDefined)

__all__=(
    'MegamodelElement',
)

Metamodel= 'Metamodel'
MetamodelDependency='MetamodelDependency'

# Model='Model'
ModelDependency='ModelDependency'

ModelSourceFile='ModelOldSourceFile'
SourceFileDependency='SourceFileDependency'
OptSource=Optional[ModelSourceFile]


class MegamodelElement(object):
    __metaclass__ = ABCMeta

    @abstractproperty
    def outgoingDependencies(self):
        #type: () -> List[Dependency]
        raise MethodToBeDefined( #raise:OK
            'outgoingDependencies() is not defined.')

    @abstractproperty
    def incomingDependencies(self):
        #type: () -> List[Dependency]
        raise MethodToBeDefined( #raise:OK
            'incomingDependencies() is not defined.')

    def targets(self):
        #type: () -> List[MegamodelElement]
        return [d.target for d in self.outgoingDependencies]

    def sources(self):
        #type: () -> List[MegamodelElement]
        return [d.source for d in self.incomingDependencies]

