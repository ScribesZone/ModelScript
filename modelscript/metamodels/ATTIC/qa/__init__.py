# coding=utf-8


from modelscript.megamodels.models import Model
from modelscript.megamodels.metamodels import Metamodel
from modelscript.megamodels.dependencies.metamodels import (
    MetamodelDependency)


class QAModel(Model):
    pass

METAMODEL = Metamodel(
    id='qa',
    label='qa',
    extension='.qas',
    modelClass=QAModel,
    modelKinds=()
)
MetamodelDependency(
    sourceId='qa',
    targetId='gl',
    optional=True,
    multiple=True,
)

