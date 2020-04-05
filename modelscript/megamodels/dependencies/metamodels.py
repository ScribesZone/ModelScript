# coding=utf-8
"""Dependencies between metamodels.
For instance the permission metamodel depend on the usecase and classe
metamodels. That's two metamodel dependencies.
"""

from typing import List
from modelscript.megamodels.metamodels import Metamodel
from modelscript.megamodels.dependencies import Dependency
from modelscript.base.exceptions import (
    UnexpectedState)

ModelDependency = 'ModelDependency'

__all__ = (
    'MetamodelDependency'
)


class MetamodelDependency(Dependency):
    """A metamodel dependency is based on a source metamodel
    and a target metamodel but also on the fact that the
    dependency is optional or not, and multiple or not.
    For instance the dependency between permissions and
    usecases is not optional and it is multiple (not
    implemented yet).
    """

    sourceId: str
    targetId: str
    optional: bool
    multiple: bool

    def __init__(self,
                 sourceId: str,
                 targetId: str,
                 optional: bool = False,
                 multiple: bool = True) -> None:
        """Create a metamodel dependency.
        Note that parameters are ids instead of metamodels.
        This is necessary to avoid python module
        dependency cycles.
        """
        self.sourceId = sourceId
        self.targetId = targetId
        self.optional = optional
        self.multiple = multiple
        from modelscript.megamodels import Megamodel
        Megamodel.registerMetamodelDependency(self)

    @property
    def sourceMetamodel(self) -> Metamodel:
        """Source metamodel ot ValueError if this metamodel
        is not registered yet (which should not happen).
        """
        try:
            from modelscript.megamodels import Megamodel
            return Megamodel.theMetamodel(id=self.sourceId)
        except:
            raise UnexpectedState(  # raise:TODO:3
                'No target "%s" metamodel registered from %s' % (
                    self.targetId,
                    self.sourceId))

    @property
    def source(self):
        return self.sourceMetamodel

    @property
    def targetMetamodel(self) -> Metamodel:
        """
        Target metamodel ot ValueError if this metamodel
        is not registered yet (which should not happen).
        """
        try:
            from modelscript.megamodels import Megamodel

            return Megamodel.theMetamodel(id=self.targetId)
        except:                     # except:to check
            raise UnexpectedState(  # raise:TODO:3
                'From "%s" metamodel not registered to %s' % (
                    self.sourceId,
                    self.targetId
                ))

    @property
    def target(self):
        return self.targetMetamodel

    @property
    def modelDependencies(self) -> List[ModelDependency]:
        """
        Model dependencies based on this metamodel dependency.
        This could raise a ValueError.
        """
        # could raise a ValueError
        from modelscript.megamodels import Megamodel
        return Megamodel.modelDependencies(
            metamodelDependency=self)

    def check(self):
        """
        Check that both source and target are registered.
        If not raise ValueError.
        """
        _ = self.sourceMetamodel
        _ = self.targetMetamodel


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