# coding=utf-8
"""
Define dependencies between model.
"""

from typing import Optional
from modelscript.megamodels.models import Model
# from modelscript.megamodels import Megamodel
from modelscript.megamodels.dependencies.metamodels import (
    MetamodelDependency
)
from modelscript.megamodels.dependencies import Dependency


class ModelDependency(Dependency):
    """
    Model dependency is:
    - a source model
    - a target model
    - an optional "SourceElement"
    - a metamodel dependency
    """
    def __init__(self,
                 sourceModel,
                 targetModel,
                 sourceElement=None):
        #type: (Model, Model, Optional['SourceElement']) -> None
        self.sourceModel=sourceModel
        self.targetModel=targetModel
        self.sourceElement=sourceElement
        from modelscript.megamodels import Megamodel
        Megamodel.registerModelDependency(self)

    @property
    def source(self):
        return  self.sourceModel

    @property
    def target(self):
        return self.targetModel

    @property
    def metamodelDependency(self):
        #type: (ModelDependency) -> MetamodelDependency
        """
        Return the metamodel dependency this model dependency
        conforms to.
        This could raise a ValueError if there are more
        than one or no metamodel dependency.This should not
        occur unless the metamodels are not built with care.
        """
        # could raise a ValueError, but should not
        from modelscript.megamodels import Megamodel
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