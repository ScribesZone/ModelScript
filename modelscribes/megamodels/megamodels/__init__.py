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

from modelscribes.megamodels.dependencies import Dependency
from modelscribes.megamodels.megamodels._registeries.metamodels import _MetamodelRegistery
# from modelscribes.megamodels.dependencies.metamodels import MetamodelDependency
# from modelscribes.megamodels.dependencies.models import ModelDependency
# To avoid circular dependencies
# from modelscribes.megamodels.models import Model
# from modelscribes.megamodels.metamodels import Metamodel
from modelscribes.megamodels.megamodels._registeries.models import _ModelRegistery
from modelscribes.megamodels.megamodels._registeries.sources import _SourceRegistery

__all__=(
    'MegamodelElement',
    'Megamodel'
)

Metamodel= 'Metamodel'
MetamodelDependency='MetamodelDepndency'

Model='Model'
ModelDependency='ModelDependency'

ModelSourceFile='ModelSourceFile'
SourceFileDependency='SourceFileDependency'
OptSource=Optional[ModelSourceFile]

# TODO:1 Make a printer for megamodel



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


import os
class Megamodel(
    _MetamodelRegistery,
    _ModelRegistery,
    _SourceRegistery):
    """
    Static class containing a global registry
    of metamodels
    and models and corresponding dependencies.
    """

    @classmethod
    def fileMetamodel(cls, filename):
        try:
            extension=os.path.splitext(filename)[1]
            return cls.metamodel(ext=extension)
        except:
            return None

    @classmethod
    def loadFile(cls, filename):
        if not os.path.exists(filename):
            raise ValueError('File not found: %s' % filename)
        try:
            path = os.path.realpath(filename)
            # check if already registered
            return cls.source(path=path)
        except:
            # source not registered, so builf it
            mm=cls.fileMetamodel(filename)
            if mm is None:
                b=os.path.basename(filename)
                raise ValueError(
                    'No metamodel available for %s' % b)
            try:
                factory=mm.sourceClass
            except NotImplementedError:
                raise ValueError(
                    'No parser available for %s' %
                                 mm.name )
            else:
                return factory(filename)

    @classmethod
    def displayModel(cls,
                     model,
                     config=None):
        printer=model.metamodel.modelPrinterClass(
            theModel=model,
            config=config)
        printer.display()



    @classmethod
    def displaySource(cls,
                      source,
                      config=None):
        printer=source.metamodel.sourcePrinterClass(
            theSource=source,
            config=config)
        printer.display()

    @classmethod
    def displayModelDiagram(
            cls,
            model,
            config=None):
        raise NotImplementedError()