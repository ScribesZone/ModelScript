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
from modelscripts.megamodels.megamodels._registries.sources import _SourceRegistry

__all__=(
    'MegamodelElement',
)

Metamodel= 'Metamodel'
MetamodelDependency='MetamodelDepndency'

# Model='Model'
ModelDependency='ModelDependency'

ModelSourceFile='ModelSourceFile'
SourceFileDependency='SourceFileDependency'
OptSource=Optional[ModelSourceFile]


class MegamodelElement(object):
    __metaclass__ = ABCMeta

    @abstractproperty
    def outgoingDependencies(self):
        #type: () -> List[Dependency]
        raise NotImplementedError

    @abstractproperty
    def incomingDependencies(self):
        #type: () -> List[Dependency]
        raise NotImplementedError

    def targets(self):
        #type: () -> List[MegamodelElement]
        return [d.target for d in self.outgoingDependencies]

    def sources(self):
        #type: () -> List[MegamodelElement]
        return [d.source for d in self.incomingDependencies]

