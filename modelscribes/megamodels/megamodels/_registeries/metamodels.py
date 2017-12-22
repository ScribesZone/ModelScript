# coding=utf-8
from typing import Dict, Text, List, Optional
from collections import OrderedDict

Metamodel= 'Metamodel'
MetamodelDependency='MetamodelDepndency'

Model='Model'
ModelDependency='ModelDependency'

ModelSourceFile='ModelSourceFile'
SourceFileDependency='SourceFileDependency'
OptSource=Optional[ModelSourceFile]

__all__=(
    '_MetamodelRegistery'
)

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
        from modelscribes.megamodels.megamodels import Megamodel
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