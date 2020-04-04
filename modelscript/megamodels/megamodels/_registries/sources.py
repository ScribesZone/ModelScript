# coding=utf-8
"""Source registry.
This module provides a unique mixin _SourceFileRegistry to be
included in the Megamodel class.
"""

from collections import OrderedDict
from typing import List, Dict, Optional, ClassVar

from modelscript.base.exceptions import (
    NotFound)

DEBUG = 0

Metamodel = 'Metamodel'
MetamodelDependency = 'MetamodelDependency'
Model = 'Model'
ModelDependency = 'ModelDependency'
ModelSourceFile = 'ModelOldSourceFile'
SourceFileDependency = 'SourceFileDependency'


__all__ = (
    '_SourceFileRegistry'
)




class _SourceFileRegistry(object):
    """ Part of the megamodel dealing with source files. """

    _allSourceFiles: \
        ClassVar[List[ModelSourceFile]] \
        = []

    _sourceFileByPath: \
        ClassVar[Dict[Metamodel, ModelSourceFile]] \
        = OrderedDict()

    _sourceFilesByMetamodel: \
        ClassVar[Dict[Metamodel, List[ModelSourceFile]]] \
        = OrderedDict()

    _allSourceFileDependencies:\
        ClassVar[List[SourceFileDependency]] \
        = []

    _sourceFileDependenciesBySource:\
        ClassVar[Dict[Metamodel, List[SourceFileDependency]]] \
        = OrderedDict()

    _sourceFileDependenciesByTarget: \
        ClassVar[Dict[Metamodel, List[SourceFileDependency]]] \
        = {}

    # --------------------------------------------------
    #    Registering sources and dependencies
    # --------------------------------------------------

    @classmethod
    def registerSourceFile(cls, source: ModelSourceFile) -> None:
        """ Register a source. Register the corresponding model as well.
        """
        if DEBUG >= 1:
            print(('RSC: registerSourceFile(%s)' % source.fileName))
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
                from modelscript.megamodels import Megamodel
                Megamodel.registerModel(source.model)

    @classmethod
    def registerSourceFileDependency(
            cls,
            sourceDependency: SourceFileDependency) -> None:
        """ Register a source file dependency.
        Register before the source and target if not done before.
        Also register the model dependency if needed.
        """
        source = sourceDependency.source
        target = sourceDependency.target

        # Element registration
        cls.registerSourceFile(source)
        cls.registerSourceFile(target)
        from modelscript.megamodels import Megamodel
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
        # of SourceFileDependency. Nothing to do here.

    # --------------------------------------------------
    #    Retrieving information from the megamodel
    # --------------------------------------------------

    @classmethod
    # The name sourceFile instead of source is due to a conflict
    # with the method sources() (with "sources" and "targets"()) in the
    # MegamodelElement class.
    def sourceFiles(cls,
                    metamodel: Optional[Metamodel] = None)\
            -> List[ModelSourceFile]:
        """Return all source files for a given metamodel.
        If no metamodel is provided, then return all sources.
        """
        if metamodel is None:
            return cls._allSourceFiles
        else:
            return cls._sourceFilesByMetamodel[metamodel]

    @classmethod
    def sourceFile(cls, path: str) -> Metamodel:
        """Return a source given its path.
        If the path does not corresponds to this file then
        raise NotFound.
        """
        if path in cls._sourceFileByPath:
            return cls._sourceFileByPath[path]
        else:
            raise NotFound(  # raise:ok
                'No source at "%s"' % path)

    @classmethod
    def _outSourceDependencies(
            cls,
            source: ModelSourceFile) \
            -> List[SourceFileDependency]:
        """Dependencies from source or None """
        if source not in cls._sourceFileDependenciesBySource:
            return []
        else:
            return cls._sourceFileDependenciesBySource[source]

    @classmethod
    def _inSourceDependencies(
            cls,
            target: ModelSourceFile)\
            -> List[SourceFileDependency]:
        """Dependencies to target or None """
        if target not in cls._sourceFileDependenciesByTarget:
            return []
        else:
            return cls._sourceFileDependenciesByTarget[target]

    @classmethod
    def sourceDependencies(
            cls,
            source: Optional[ModelSourceFile] = None,
            target: Optional[ModelSourceFile] = None,
            metamodelDependency: Optional[MetamodelDependency] = None) \
            -> List[SourceFileDependency]:
        """Return sources dependencies according either to the
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
    def sourceDependency(cls,
                         source: ModelSourceFile,
                         target: ModelSourceFile)\
            -> Optional[SourceFileDependency]:
        """Return the dependency between source and target"""
        d = cls.sourceDependencies(source=source, target=target)
        if len(d) == 1:
            return d[0]
        else:
            return None

    @classmethod
    def sourceFileList(cls, origins=None):
        if origins is None:
            origins = cls.sourceFiles()
        visited = []
        output = []
        # def visit(source_file):
        #     if source_file not in visited:
        #         visited.insert(0, source_file)
        #         for x in source_file.usedSourceFiles:
        #             if x not in visited:
        #                 visit(x)
        # for x in origins:
        #     visit(x)

        def visit(source_file):
            if source_file not in visited:
                visited.append(source_file)
                for x in source_file.usedSourceFiles:
                    if x not in visited:
                        visit(x)
                output.append(source_file)

        for x in list(origins):
            visit(x)

        return output
