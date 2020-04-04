# coding=utf-8
"""model registry.
This module provides a unique mixin _ModelRegistry to be
included in the Megamodel class.
"""
from collections import OrderedDict
from typing import Dict,  List, Optional, ClassVar

Metamodel = 'Metamodel'
MetamodelDependency = 'MetamodelDepndency'

Model = 'Model'
ModelDependency = 'ModelDependency'

ModelSourceFile = 'ModelOldSourceFile'
SourceFileDependency = 'SourceFileDependency'
OptSource = Optional[ModelSourceFile]

__all__ = (
    '_ModelRegistry'
)


class _ModelRegistry(object):
    """Part of the megamodel dealing with models
    """

    _allModels: \
        ClassVar[List[Model]]\
        = []

    _modelsByMetamodel: \
        ClassVar[Dict[Metamodel, List[Model]]] \
        = OrderedDict()

    _allModelDependencies\
        = []        # checktypes

    _modelDependenciesBySource: \
        Dict[Model, List[ModelDependency]] \
        = OrderedDict()

    # --------------------------------------------------
    #    Registering models and dependencies
    # --------------------------------------------------

    @classmethod
    def registerModel(cls, model: Model) -> None:
        """Register a model. Register the metamodel as well
        if not already done.
        """
        from modelscript.megamodels import Megamodel
        if model not in cls._allModels:
            cls._allModels.append(model)
            metamodel = model.metamodel
            if metamodel not in Megamodel._modelsByMetamodel:
                cls._modelsByMetamodel[metamodel] = []
            cls._modelsByMetamodel[metamodel].append(model)
            # This avoid having undefined index later
            cls._modelDependenciesBySource[model] = []

    @classmethod
    def registerModelDependency(cls,
                                modelDependency: ModelDependency)\
            -> ModelDependency:
        """Register a model dependency. Check first if there is
        not already a dependency between the source and target.
        If this is the case return that model dependency.
        The source of the model is used to index to model
        dependency.
        """
        s = modelDependency.sourceModel
        t = modelDependency.targetModel
        d = cls.modelDependency(s, t)
        if d is not None:
            return d
        else:
            from modelscript.megamodels import Megamodel
            if s not in Megamodel._modelDependenciesBySource:
                Megamodel._modelDependenciesBySource[s] = []
            Megamodel._modelDependenciesBySource[
                s
            ].append(modelDependency)
            cls._allModelDependencies.append(modelDependency)
            return modelDependency

    # --------------------------------------------------
    #    Retrieving information from the megamodel
    # --------------------------------------------------

    @classmethod
    def models(cls, metamodel: Metamodel = None) -> List[Model]:
        """Return all models of a given metamodels.
        If no metamodel is provided, then return all models.
        """
        if metamodel is None:
            return cls._allModels
        else:
            return cls._modelsByMetamodel[metamodel]

    @classmethod
    def _outModelDependencies(cls, sourceModel: Model) \
            -> List[ModelDependency]:
        if sourceModel not in cls._modelDependenciesBySource:
            return []
        else:
            return cls._modelDependenciesBySource[sourceModel]


    @classmethod
    def _inModelDependencies(cls, targetModel: Model) \
        -> List[ModelDependency]:
        return [
            d for d in cls._allModelDependencies
            if d.targetModel == targetModel
        ]

    @classmethod
    def modelDependencies(cls,
                          source: Optional[Model] = None,
                          target: Optional[Model] = None,  # checktypes
                          metamodelDependency=None) \
            -> List[ModelDependency]:
        """Return model dependencies according either to the
        source model, target model, or metamodel dependency.
        If no parameter is provided then return all dependencies.
        """
        # First filter by source and target
        if source is None and target is None:
            # all dependencies
            m_deps = cls._allModelDependencies
        elif source is not None and target is None:
            # return dependencies from source
            m_deps = cls._outModelDependencies(source)
        elif source is None and target is not None:
            # return dependencies to target
            m_deps = cls._inModelDependencies(target)
        else:
            # return dependencies between source and target
            m_deps = [
                d for d in cls._outModelDependencies(source)
                if d.targetModel == target
            ]

        # filter with metamodelDependency
        if metamodelDependency is None:
            return m_deps
        else:
            return [
                m_dep for m_dep in m_deps
                if m_dep.metamodelDependency == metamodelDependency
            ]

    @classmethod
    def modelDependency(cls, source: Model, target: Model) \
            -> Optional[ModelDependency]:
        """ Return the dependency between source and target"""
        l = cls.modelDependencies(source=source, target=target)
        if len(l) == 1:
            return l[0]
        else:
            return None