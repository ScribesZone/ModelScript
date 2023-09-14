# coding=utf-8


from modelscript.megamodels.models import Model
from modelscript.megamodels.metamodels import Metamodel
from modelscript.megamodels.dependencies.metamodels import (
    MetamodelDependency)


class QCModel(Model):
    pass

METAMODEL = Metamodel(
    id='qc',
    label='qc',
    extension='.qcs',
    modelClass=QCModel,
    modelKinds=()
)
MetamodelDependency(
    sourceId='qc',
    targetId='gl',
    optional=True,
    multiple=True,
)

