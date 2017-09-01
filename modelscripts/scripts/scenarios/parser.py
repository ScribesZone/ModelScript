# coding=utf-8

from __future__ import unicode_literals, print_function, absolute_import, division

from typing import Text, Optional

from modelscripts.metamodels.classes import (
    ClassModel
)
from modelscripts.metamodels.usecases import (
    UsecaseModel
)
from modelscripts.metamodels.permissions import (
    PermissionModel
)
from modelscripts.use.sex.parser import (
    SoilSource,
    SexSource,
)


class ScenarioModelSource(SoilSource):

    def __init__(self, soilFileName, classModel, usecaseModel):
        #type: (Text, ClassModel, Optional[UsecaseModel]) -> None
        super(ScenarioModelSource, self).__init__(
            soilFileName=soilFileName,
            classModel=classModel,
            usecaseModel=usecaseModel)

class ScenarioEvaluationModelSource(SexSource):

    def __init__(self, soilFileName, classModel, usecaseModel, permissionModel):
        #type: (Text, ClassModel, Optional[UsecaseModel], Optional[PermissionModel]) -> None
        super(ScenarioEvaluationModelSource, self).__init__(
            soilFileName=soilFileName,
            classModel=classModel,
            usecaseModel=usecaseModel,
            permissionModel=permissionModel)
