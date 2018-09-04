# coding=utf-8
from __future__ import print_function

from modelscripts.megamodels.models import Model
from modelscripts.megamodels.metamodels import Metamodel
from modelscripts.megamodels.dependencies.metamodels import (
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

