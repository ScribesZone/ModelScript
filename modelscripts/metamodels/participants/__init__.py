# coding=utf-8
from __future__ import print_function

from modelscripts.megamodels.models import Model
from modelscripts.megamodels.metamodels import Metamodel
from modelscripts.megamodels.dependencies.metamodels import (
    MetamodelDependency)


class ParticipantModel(Model):
    pass

METAMODEL = Metamodel(
    id='pa',
    label='participant',
    extension='.pas',
    modelClass=ParticipantModel,
    modelKinds=('preliminary', '', 'detailed')
)
MetamodelDependency(
    sourceId='pa',
    targetId='gl',
    optional=True,
    multiple=True,
)

