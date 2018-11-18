# coding=utf-8
from __future__ import print_function

from modelscript.megamodels.models import Model
from modelscript.megamodels.metamodels import Metamodel
from modelscript.megamodels.dependencies.metamodels import (
    MetamodelDependency)


class ProjectModel(Model):
    pass

METAMODEL = Metamodel(
    id='pr',
    label='project',
    extension='.prs',
    modelClass=ProjectModel,
    modelKinds=()
)
MetamodelDependency(
    sourceId='pr',
    targetId='gl',
    optional=True,
    multiple=True,
)
MetamodelDependency(
    sourceId='pr',
    targetId='qu',
    optional=True,
    multiple=True,
)

