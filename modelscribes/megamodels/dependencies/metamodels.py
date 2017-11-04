# coding=utf-8
from typing import Text, List
from modelscribes.megamodels.metamodels import Metamodel
# Model='Model'
# Metamodel='Metamodel'
# M='SourceElement'
ModelDependency='ModelDependency'

from modelscribes.megamodels.megamodels import Megamodel


class MetamodelDependency(object):
    """
    'id's parameters are used instead of metamodels to avoid
    python module dependency cycles.
    """
    def __init__(self,
                 sourceId,
                 targetId,
                 optional=False,
                 multiple=True):
        #type: (Text, Text, bool, bool) -> None
        self.sourceId=sourceId #type: Text
        self.targetId=targetId #type: Text
        self.optional=optional #type: bool
        self.multiple=multiple #type: bool
        Megamodel.registerMetamodelDependency(self)

    @property
    def sourceMetamodel(self):
        #type: (MetamodelDependency) -> Metamodel
        try:
            return Megamodel.metamodel(id=self.sourceId)
        except:
            raise ValueError(
                'No target "%s" metamodel registered from %s' % (
                    self.sourceId,
                    self.targetId
                ))

    @property
    def targetMetamodel(self):
        # type: (MetamodelDependency) -> Metamodel
        try:
            return Megamodel.metamodel(id=self.targetId)
        except:
            raise ValueError(
                'From "%s" metamodel not registered to %s' % (
                    self.sourceId,
                    self.targetId
                ))


    @property
    def modelDependencies(self):
        # type: (MetamodelDependency) -> List(ModelDependency)
        # could raise a ValueError
        return Megamodel.modelDependencies(
            metamodelDependency=self)

    def check(self):
        # Check that both source and target are defined
        _=self.sourceMetamodel
        _=self.targetMetamodel


    def _card(self):
        if self.optional and self.multiple:
            return '*'
        elif self.optional and not self.multiple:
            return '0..1'
        elif not self.optional and self.multiple:
            return '1..*'
        else:
            return '1'

    def __str__(self):
        return (
            'A %s model can use [%s] %s model(s)' % (
                self.sourceMetamodel.label,
                self._card(),
                self.targetMetamodel.label
            ))

    def __repr__(self):
        return (
            'A %s model can use [%s] %s model(s)' % (
                self.sourceMetamodel.label,
                self._card(),
                self.targetMetamodel.label
            ))