# coding=utf-8
from collections import OrderedDict
from typing import List, Dict, Optional

__all__=(
    '_SourceRegistery'
)


Metamodel= 'Metamodel'
MetamodelDependency='MetamodelDepndency'

Model='Model'
ModelDependency='ModelDependency'

ModelSourceFile='ModelSourceFile'
SourceFileDependency='SourceFileDependency'
OptSource=Optional[ModelSourceFile]

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
                from modelscribes.megamodels.megamodels import Megamodel
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
        from modelscribes.megamodels.megamodels import Megamodel
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