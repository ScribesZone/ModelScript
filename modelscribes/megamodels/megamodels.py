# coding=utf-8

"""
Provide a global registery of:
- metamodels,
- models,
- metamodel dependencies
- model dependencies
"""
from typing import Dict, Text, List, Optional
from abc import ABCMeta, abstractproperty
from collections import OrderedDict

# from modelscribes.megamodels.dependencies.metamodels import MetamodelDependency
# from modelscribes.megamodels.dependencies.models import ModelDependency

# To avoid circular dependencies
# from modelscribes.megamodels.models import Model
# from modelscribes.megamodels.metamodels import Metamodel

from modelscribes.megamodels.dependencies import Dependency

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



class _MetamodelRegistery(object):
    """
    Part of the megamodel dealing with metamodels
    """

    #----- metamodel registery ------
    _metamodelById=OrderedDict()
    #type: Dict[Text, Metamodel]

    _metamodelByLabel=OrderedDict()
    #type: Dict[Text, Metamodel]

    _metamodelByExtension=OrderedDict()
    #type: Dict[Text, Metamodel]

    _metamodelDependencies=[]
    #type: List[MetamodelDependency]


    #--------------------------------------------------
    #    Registering metamodels and dependencies
    #--------------------------------------------------

    @classmethod
    def registerMetamodel(cls, metamodel):
        # type: (Metamodel) -> None
        """
        Register a metamodel.
        """
        Megamodel._metamodelById[metamodel.id] = metamodel
        Megamodel._metamodelByLabel[metamodel.label] = metamodel
        Megamodel._metamodelByExtension[metamodel.extension] = metamodel

    @classmethod
    def registerMetamodelDependency(cls, metamodelDependency):
        # type: (MetamodelDependency) -> None
        """
        Register a metamodel dependency.
        """
        cls._metamodelDependencies.append(metamodelDependency)


    # --------------------------------------------------
    #    Retrieving information from the megamodel
    # --------------------------------------------------


    @classmethod
    def metamodels(cls):
        #type: () -> List[Metamodel]
        """
        List all registered metamodels.
        """
        return cls._metamodelById.values()

    @classmethod
    def metamodel(cls, id=None, label=None, ext=None):
        #type: () -> Metamodel
        """
        Return a metamodel given either
        its id, label, or extension.
        Raise ValueError if not found.
        """
        assert (
            id is not None
            or label is not None
            or ext is not None)
        if id is not None:
            try:
                return cls._metamodelById[id]
            except:
                raise ValueError('No "%s" metamodel registered'
                          % id)
        if label is not None:
            try:
                return cls._metamodelByLabel[label]
            except:
                raise ValueError('No "%s" metamodel registered'
                                 %label)
        if ext is not None:
            try:
                return cls._metamodelByExtension[ext]
            except:
                raise ValueError('No "%s" metamodel registered'
                                 % ext)

    @classmethod
    def metamodelDependencies(cls, source=None, target=None):
        # type: (Optional[Metamodel], Optional[Metamodel]) -> List[MetamodelDependency]
        """
        Return metamodel dependencies according to the source
        or target metamodel. If no parameter
        is provided then return all dependencies.
        """

        def _like(value, optval):
            return True if optval is None else value == optval

        if source is None and target is None:
            # return all dependencies
            return list(cls._metamodelDependencies)
        else:
            return [
                d for d in cls._metamodelDependencies
                if (_like(d.sourceMetamodel, source)
                    and _like(d.targetMetamodel, target))]

    @classmethod
    def metamodelDependency(cls, source, target):
        # type: (Metamodel, Metamodel) -> MetamodelDependency
        """
        Return the only one dependency between two metamodels.
        Raise ValueError if there are more or less that one.
        To be called only if it is assumed that there is
        only one.
        """
        ds = cls.metamodelDependencies(source=source, target=target)
        if (len(ds) == 0):
            raise ValueError(
                'Invalid dependency between %s'
                ' metamodel towards %s metamodel'
                % (source.label, target.label))
        elif (len(ds) >= 2):
            # This should not occur as metamodels should be ok
            raise ValueError(
                'More that one dependency (%s) '
                'between %s metamodel towards %s metamodel'
                % (len(ds), source.label, target.label))
        else:
            return ds[0]



    @classmethod
    def checkMetamodelLevel(cls):
        """
        Check all metamodel dependencies.
        """
        for mmd in cls.metamodelDependencies():
            mmd.check()


class _ModelRegistery(object):
    """
    Part of the megamodel dealing with models
    """

    _allModels = []
    #type: List[Model]

    _modelsByMetamodel = OrderedDict()
    #type: Dict[Metamodel, List[Model]]


    _allModelDependencies = []

    _modelDependenciesBySource = OrderedDict()
    #type: Dict[Model, List[ModelDependency]]

    #--------------------------------------------------
    #    Registering models and dependencies
    #--------------------------------------------------

    @classmethod
    def registerModel(cls, model):
        # type: (Model) -> None
        """
        Register a model. Register the metamodel as well
        if not already done.
        """
        if model not in cls._allModels:
            cls._allModels.append(model)
            metamodel = model.metamodel
            if metamodel not in Megamodel._modelsByMetamodel:
                cls._modelsByMetamodel[metamodel] = []
            cls._modelsByMetamodel[metamodel].append(model)
            # This avoid having undefined index later
            cls._modelDependenciesBySource[model] = []

    @classmethod
    def registerModelDependency(cls, modelDependency):
        # type: (ModelDependency) -> ModelDependency
        """
        Register a model dependency. Check first if there is
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
    def models(cls, metamodel=None):
        # type: () -> List[Model]
        """
        Return all models of a given metamodels.
        If no metamodel is provided, then return all models.
        """
        if metamodel is None:
            return cls._allModels
        else:
            return cls._modelsByMetamodel[metamodel]

    @classmethod
    def _outModelDependencies(cls, sourceModel):
        # type: (Model) -> List[ModelDependency]
        if sourceModel not in cls._modelDependenciesBySource:
            return []
        else:
            return cls._modelDependenciesBySource[sourceModel]


    @classmethod
    def _inModelDependencies(cls, targetModel):
        # type: (Model) -> List[ModelDependency]
        return [
            d for d in cls._allModelDependencies
            if d.targetModel == targetModel
        ]

    @classmethod
    def modelDependencies(cls,
                          source=None,
                          target=None,
                          metamodelDependency=None):
        # type: (Optional[Model], Optional[Model]) -> List[ModelDependency]
        """
        Return model dependencies according either to the
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
    def modelDependency(cls, source, target):
        #type: (Model, Model) -> Optional[ModelDependency]
        """ Return the dependency between source and target"""
        l=cls.modelDependencies(source=source, target=target)
        if len(l)==1:
            return l[0]
        else:
            return None

class _SourceRegistery(object):
    """
    Part of the megamodel dealing with source files
    """

    _allSourceFiles=[]
    #type: List[ModelSourceFile]

    _sourceFileByPath = OrderedDict()
    # type:Dict[Metamodel, ModelSourceFile]

    _sourceFilesByMetamodel = OrderedDict()
    # type:Dict[Metamodel, List[ModelSourceFile]


    _allSourceFileDependencies = []
    # type: List[SourceFileDependency]

    _sourceFileDependenciesBySource = OrderedDict()
    # type:Dict[Metamodel, List[SourceFileDependency]

    _sourceFileDependenciesByTarget = {}
    # type:Dict[Metamodel, List[SourceFileDependency]

    # --------------------------------------------------
    #    Registering sources and dependencies
    # --------------------------------------------------

    @classmethod
    def registerSource(cls, source):
        # type: (ModelSourceFile) -> None
        """
        Register a source. Register the model as well.
        """

        if source.path not in cls._sourceFileByPath:
            cls._allSourceFiles.append(source)

            # ByPath
            metamodel = source.metamodel
            cls._sourceFileByPath[source.path] = source

            # ByMetamodel
            if metamodel not in cls._sourceFilesByMetamodel:
                cls._sourceFilesByMetamodel[metamodel] = []
            if source not in cls._sourceFilesByMetamodel[metamodel]:
                cls._sourceFilesByMetamodel[metamodel].append(source)

            # Register model
            if source.model is not None:
                Megamodel.registerModel(source.model)

    @classmethod
    def registerSourceDependency(cls, sourceDependency):
        # type: (SourceFileDependency) -> None
        """
        Register a source file dependency. Register
        before the source and target if not done before.
        Also register the model dependency if needed.
        """
        source = sourceDependency.source
        target = sourceDependency.target

        # Element registration
        cls.registerSource(source)
        cls.registerSource(target)
        Megamodel.registerModel(source.model)
        Megamodel.registerModel(target.model)

        cls._allSourceFileDependencies.append(sourceDependency)

        # BySource
        if source not in cls._sourceFileDependenciesBySource:
            cls._sourceFileDependenciesBySource[source] = []
        cls._sourceFileDependenciesBySource[source].append(sourceDependency)

        # ByTarget
        if target not in cls._sourceFileDependenciesByTarget:
            cls._sourceFileDependenciesByTarget[target] = []
        cls._sourceFileDependenciesByTarget[target].append(sourceDependency)

        # Model dependency creation is done in constructor
        # of SourceFileDependency. Nothiing to do here



    # --------------------------------------------------
    #    Retrieving information from the megamodel
    # --------------------------------------------------

    @classmethod
    def sources(cls, metamodel=None):
        # type: () -> List[ModelSourceFile]
        """
        Return all source files for a given metamodel.
        If no metamodel is provided, then return all sources.
        """
        if metamodel is None:
            return cls._allSourceFiles
        else:
            return cls._sourceFilesByMetamodel[metamodel]

    @classmethod
    def source(cls, path):
        # type: () -> Metamodel
        """
        Return a source given its path or raise ValueError.
        """
        try:
            return cls._sourceFileByPath[path]
        except:
            raise ValueError('No source at "%s" % path')

    @classmethod
    def _outSourceDependencies(cls, source):
        # type: (ModelSourceFile) -> List[SourceFileDependency]
        """ Dependencies from source or None """
        if source not in cls._sourceFileDependenciesBySource:
            return []
        else:
            return cls._sourceFileDependenciesBySource[source]

    @classmethod
    def _inSourceDependencies(cls, target):
        # type: (ModelSourceFile) -> List[SourceFileDependency]
        """ Dependencies to target or None """
        if target not in cls._sourceFileDependenciesByTarget:
            return []
        else:
            return cls._sourceFileDependenciesByTarget[target]

    @classmethod
    def sourceDependencies(cls,
                           source=None,
                           target=None,
                           metamodelDependency=None):
        # type: (OptSource, OptSource, Optional[MetamodelDependency]) -> List[SourceFileDependency]
        """
        Return sources dependencies according either to the
        source source file, target source file, or metamodel
        dependency.
        If no parameter is provided then return all dependencies.
        """

        # (1) First filter by source and target
        if source is None and target is None:
            # all dependencies
            deps = cls._allSourceFileDependencies
        elif source is not None and target is None:
            # return dependencies from source
            deps = cls._outSourceDependencies(source)
        elif source is None and target is not None:
            # return dependencies to target
            deps = cls._inSourceDependencies(target)
        else:
            # return dependencies between source and target
            deps = [
                d for d in cls._outSourceDependencies(source)
                if d.target == target
            ]

        # (2) Second filter with metamodelDependency
        if metamodelDependency is None:
            return deps
        else:
            return [
                dep for dep in deps
                if dep.metamodelDependency == metamodelDependency
            ]

    @classmethod
    def sourceDependency(cls, source, target):
        #type: (ModelSourceFile, ModelSourceFile) -> Optional[SourceFileDependency]
        """ Return the dependency between source and target"""
        d=cls.sourceDependencies(source=source, target=target)
        if len(d)==1:
            return d[0]
        else:
            return None

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
            try:
                factory=mm.sourceClass
            except NotImplementedError:
                raise ValueError('No parser available for %s' %
                                 mm.name )
            else:
                return factory(filename)

