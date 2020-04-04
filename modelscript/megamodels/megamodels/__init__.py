# coding=utf-8

"""
Provide a global registery of:
- metamodels,
- models,
- metamodel dependencies
- model dependencies
"""
from abc import ABCMeta, abstractmethod

from typing import List, Optional

from modelscript.megamodels.dependencies import Dependency
from modelscript.megamodels.megamodels._registries.metamodels import _MetamodelRegistry
# from modelscript.megamodels.dependencies.metamodels import MetamodelDependency
# from modelscript.megamodels.dependencies.models import ModelDependency
# To avoid circular dependencies
# from modelscript.megamodels.models import Model
# from modelscript.megamodels.metamodels import Metamodel
from modelscript.megamodels.megamodels._registries.models import _ModelRegistry
from modelscript.megamodels.megamodels._registries.sources import _SourceFileRegistry
from modelscript.base.exceptions import (
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


class MegamodelElement(object, metaclass=ABCMeta):
    @property
    @abstractmethod
    def outgoingDependencies(self):
        #type: () -> List[Dependency]
        raise MethodToBeDefined( #raise:OK
            'outgoingDependencies() is not defined.')

    @property
    @abstractmethod
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

