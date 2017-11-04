# coding=utf-8
from typing import Dict, Text, List, Optional


# from modelscribes.megamodels.dependencies.metamodels import MetamodelDependency
# from modelscribes.megamodels.dependencies.models import ModelDependency

# To avoid circular dependencies
# from modelscribes.megamodels.models import Model
# from modelscribes.megamodels.metamodels import Metamodel


Metamodel= 'Metamodel'
Model='Model'
MetamodelDependency='MetamodelDepndency'
ModelDependency='ModelDependency'

# XXX TODO: Make a print for megamodel
# XXX TODO: add a import modelscribes to load everything

class Megamodel(object):

    _metamodelById={}
    #type: Dict[Text, Metamodel]

    _metamodelByLabel={}
    #type: Dict[Text, Metamodel]

    _metamodelByExtension={}
    #type: Dict[Text, Metamodel]

    _modelsByMetamodel={}
    #type:Dict[Metamodel, List[Model]]

    _modelDependenciesBySource={}
    #type: Dict[Model, List['ModelDependency']]

    _metamodelDependencies=[]
    #type: List['MetamodelDependency']

    @classmethod
    def registerModel(cls, model):
        #type: (Model) -> None
        metamodel=model.metamodel
        if metamodel not in Megamodel._modelsByMetamodel:
            Megamodel._modelsByMetamodel[metamodel]=[]
        Megamodel._modelsByMetamodel[metamodel].append(model)
        # This avoid having undefined index later
        Megamodel._modelDependenciesBySource[model]=[]


    @classmethod
    def registerMetamodel(cls, metamodel):
        #type: (Metamodel) -> None
        Megamodel._metamodelById[metamodel.id]=metamodel
        Megamodel._metamodelByLabel[metamodel.label]=metamodel
        Megamodel._metamodelByExtension[metamodel.extension]=metamodel
        # print('+++'*30+'\n')
        #print('Register metamodel', metamodel)
        # print('+++'*30+'\n')
        # This avoid having undefined index later



    @classmethod
    def registerModelDependency(cls, modelDependency):
        #type: (ModelDependency) -> None
        sm=modelDependency.sourceModel
        if sm not in Megamodel._modelDependenciesBySource:
            Megamodel._modelDependenciesBySource[sm]=[]
        Megamodel._modelDependenciesBySource[
            sm
        ].append(modelDependency)


    @classmethod
    def registerMetamodelDependency(cls, metamodelDependency):
        #type: (MetamodelDependency) -> None
        cls._metamodelDependencies.append(metamodelDependency)



    @classmethod
    def metamodels(cls):
        #type: () -> List[Metamodel]
        return cls._metamodelById.values()

    @classmethod
    def metamodel(cls, id=None, label=None, ext=None):
        #type: () -> Metamodel
        # Raise ValueError if not found
        assert id is not None or label is not None or ext is not None
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
    def models(cls, metamodel=None):
        #type: () -> List[Model]
        if metamodel is None:
            return cls._modelsByMetamodel.values()
        else:
            return cls._modelsByMetamodel[metamodel]

    @classmethod
    def _outModelDependencies(cls, sourceModel):
        #type: (Model) -> List[ModelDependency]
        if sourceModel not in cls._modelDependenciesBySource:
            return []
        else:
            return cls._modelDependenciesBySource[sourceModel]

    @classmethod
    def _allModelDependencies(cls):
        return [
            d for ds in cls._modelDependenciesBySource.values()
                for d in ds
        ]

    @classmethod
    def _inModelDependencies(cls, targetModel):
        #type: (Model) -> List[ModelDependency]
        return [
            d for d in cls._allModelDependencies()
                if d.targetModel == targetModel
        ]

    @classmethod
    def modelDependencies(cls,
                          source=None,
                          target=None,
                          metamodelDependency=None):
        #type: (Optional[Model], Optional[Model]) -> List[ModelDependency]
        # First filter by source and target
        if source is None and target is None:
            # all dependencies
            m_deps=cls._allModelDependencies()
        elif source is not None and target is None:
            # return dependencies from source
            m_deps=cls._outModelDependencies(source)
        elif source is None and target is not None:
            # return dependencies to target
            m_deps=cls._inModelDependencies(target)
        else:
            # return dependencies between source and target
            m_deps= [
                d for d in cls._outModelDependencies(source)
                    if d.targetModel == target
            ]

        # filter with metamodelDependency
        if metamodelDependency is None:
            return m_deps
        else:
            return [
                m_dep for m_dep in m_deps
                    if m_dep.metamodelDependency==metamodelDependency
            ]


    @classmethod
    def metamodelDependencies(cls, source=None, target=None):
        #type: (Optional[Metamodel], Optional[Metamodel]) -> List[MetamodelDependency]

        def _like(value, optval):
            return True if optval is None else value==optval

        if source is None and target is None:
            # return all dependencies
            return list(cls._metamodelDependencies)
        else:
            return [
                d for d in cls._metamodelDependencies
                    if (_like(d.sourceMetamodel, source)
                        and _like(d.targetMetamodel, target)) ]

    @classmethod
    def metamodelDependency(cls, source, target):
        #type: (Metamodel, Metamodel) -> MetamodelDependency
        """
        Return the only one metamodel dependency between two metamodels.
        Raise an exception if there are more or less that one.
        To be called only if it is assumed that there is only one.
        """
        ds=cls.metamodelDependencies(source=source, target=target)
        if (len(ds)==0):
            raise ValueError(
                'Invalid dependency between %s metamodel towards %s metamodel'
                % (source.label, target.label))
        elif (len(ds)>=2):
            # This should not occur as metamodels should be ok
            raise ValueError(
                'More that one dependency (%s) between %s metamodel towards %s metamodel'
                % (len(ds), source.label, target.label))
        else:
            return ds[0]

    @classmethod
    def checkMetamodelLevel(cls):
        for mmd in cls.metamodelDependencies():
            mmd.check()

# TODO: add megamodel print