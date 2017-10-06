# coding=utf-8

from typing import Optional
from modelscribes.megamodels.models import Model
from modelscribes.megamodels.megamodels import Megamodel
from modelscribes.megamodels.dependencies.metamodels import (
    MetamodelDependency
)

class ModelDependency(object):
    def __init__(self,
                 sourceModel,
                 targetModel,
                 sourceElement=None):
        #type: (Model, Model, Optional['SourceElement']) -> None
        self.sourceModel=sourceModel
        self.targetModel=targetModel
        self.sourceElement=sourceElement
        Megamodel.registerModelDependency(self)

    @property
    def metamodelDependency(self):
        #type: (ModelDependency) -> MetamodelDependency
        """
        This could raise a ValueError if there are more
        than one or no metamodel dependency.This should not
        occur unless the metamodels are not built with care.
        """
        # could raise a ValueError, but should not
        return Megamodel.metamodelDependency(
            source=self.sourceModel.metamodel,
            target=self.targetModel.metamodel)


    # @property
    # def check(self):
    #     """
    #     Check if the ModelDependency is valid.
    #     Do nothing if it is else raise a ValueError.
    #     This could be because there is no corresponding metadependency between metamodel.
    #     This could also due because of too much depedency of the same type
    #     with the same source model.
    #     """
    #     # this could raise a ValueError
    #     deps_same_type=self.sourceModel.outDependencies(
    #         targetMetamodel=self.targetModel.metamodel)
    #     if len(deps_same_type)>=2 and not self.metamodelDependency.multiple:
    #         raise ValueError('A %s model can depend on at most one %s model.'
    #                          % (self.sourceModel.metamodel.label,
    #                             self.targetModel.metamodel.label))