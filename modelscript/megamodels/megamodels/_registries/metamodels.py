# coding=utf-8
from typing import Dict, Text, List, Optional
from collections import OrderedDict
from modelscript.base.exceptions import (
    UnexpectedValue,
    UnexpectedState)

Metamodel= 'Metamodel'
MetamodelDependency='MetamodelDepndency'

Model='Model'
ModelDependency='ModelDependency'

ModelSourceFile='ModelOldSourceFile'
SourceFileDependency='SourceFileDependency'
OptSource=Optional[ModelSourceFile]

__all__=(
    '_MetamodelRegistry'
)

class _MetamodelRegistry(object):
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
        from modelscript.megamodels import Megamodel
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
        # TODO:4 2to3 was cls._metamodelById.values()
        return list(cls._metamodelById.values())

    @classmethod
    def metamodelExtensions(cls):
        #type: () -> List[Text]
        """
        List all registered extensions.
        """
        # TODO:4 2to3 was cls._metamodelByExtension.keys()
        return list(cls._metamodelByExtension.keys())

    @classmethod
    def theMetamodel(cls, id=None, label=None, ext=None):
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
            if id in cls._metamodelById:
                return cls._metamodelById[id]
            else:
                raise UnexpectedValue( #raise:TODO:4
                    'No "%s" metamodel registered' % id)
        if label is not None:
            if label in cls._metamodelByLabel:
                return cls._metamodelByLabel[label]
            else:
                raise UnexpectedValue( #raise:TODO:4
                    'No "%s" metamodel registered' % label)
        if ext is not None:
            if ext in cls._metamodelByExtension:
                return cls._metamodelByExtension[ext]
            else:
                raise UnexpectedValue( #raise:TODO:4
                      'No "%s" metamodel registered' % ext)

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
            raise UnexpectedState( #raise:TODO:2
                'Invalid dependency between %s'
                ' metamodel towards %s metamodel'
                % (source.label, target.label))
        elif (len(ds) >= 2):
            # This should not occur as metamodels should be ok
            raise UnexpectedState( #raise:TODO:2
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