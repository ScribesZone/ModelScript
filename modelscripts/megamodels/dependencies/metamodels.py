# coding=utf-8
"""
Dependencies between metamodels. For instance permissions
depend on usecases and classes.
"""
from typing import Text, List
from modelscripts.megamodels.metamodels import Metamodel
from modelscripts.megamodels.dependencies import Dependency
from modelscripts.base.exceptions import (
    UnexpectedState)

# Model='Model'
# Metamodel='Metamodel'
# M='SourceElement'
ModelDependency='ModelDependency'

class MetamodelDependency(Dependency):
    """
    A metamodel dependency is based on a source metamodel
    and a target metamodel but also on the fact that the
    dependency is optional or not, and multiple or not.
    For instance the dependency between permissions and
    usecases is not optional and it is multiple (not
    implemented yet).
    """
    def __init__(self,
                 sourceId,
                 targetId,
                 optional=False,
                 multiple=True):
        #type: (Text, Text, bool, bool) -> None
        """
        Create a metamodel dependency.
        Note that parameters are ids instead of metamodels.
        This is necessary to avoid python module
        dependency cycles.
        """
        self.sourceId=sourceId #type: Text
        self.targetId=targetId #type: Text
        self.optional=optional #type: bool
        self.multiple=multiple #type: bool
        from modelscripts.megamodels import Megamodel
        Megamodel.registerMetamodelDependency(self)

    @property
    def sourceMetamodel(self):
        #type: (MetamodelDependency) -> Metamodel
        """
        Source metamodel ot ValueError if this metamodel
        is not registered yet (which should not happen).
        """
        try:
            from modelscripts.megamodels import Megamodel
            return Megamodel.theMetamodel(id=self.sourceId)
        except:
            raise UnexpectedState( #raise:TODO:3
                'No target "%s" metamodel registered from %s' % (
                    self.sourceId,
                    self.targetId))

    @property
    def source(self):
        return self.sourceMetamodel

    @property
    def targetMetamodel(self):
        # type: (MetamodelDependency) -> Metamodel
        """
        Target metamodel ot ValueError if this metamodel
        is not registered yet (which should not happen).
        """
        try:
            from modelscripts.megamodels import Megamodel

            return Megamodel.theMetamodel(id=self.targetId)
        except:
            raise UnexpectedState( #raise:TODO:3
                'From "%s" metamodel not registered to %s' % (
                    self.sourceId,
                    self.targetId
                ))

    @property
    def target(self):
        return self.targetMetamodel


    @property
    def modelDependencies(self):
        # type: (MetamodelDependency) -> List(ModelDependency)
        """
        Model dependencies based on this metamodel dependency.
        This could raise a ValueError.
        """
        # could raise a ValueError
        from modelscripts.megamodels import Megamodel
        return Megamodel.modelDependencies(
            metamodelDependency=self)

    def check(self):
        """
        Check that both source and target are registered.
        If not raise ValueError.
        """
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