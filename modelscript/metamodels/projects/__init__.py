# coding=utf-8


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
    targetId='qa',
    optional=True,
    multiple=True,
)
MetamodelDependency(
    sourceId='pr',
    targetId='qc',
    optional=True,
    multiple=True,
)
