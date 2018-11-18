# coding=utf-8
from __future__ import print_function

from modelscript.megamodels.models import Model
from modelscript.megamodels.metamodels import Metamodel
from modelscript.megamodels.dependencies.metamodels import (
    MetamodelDependency)


class QualityModel(Model):
    pass

METAMODEL = Metamodel(
    id='qu',
    label='quality',
    extension='.qus',
    modelClass=QualityModel,
    modelKinds=()
)
MetamodelDependency(
    sourceId='qu',
    targetId='gl',
    optional=True,
    multiple=True,
)

