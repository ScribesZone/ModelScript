# coding=utf-8

from __future__ import unicode_literals, print_function, absolute_import, division

from modelscripts.use.sex.parser import (
    SoilSource,
    SexSource,
)


class ScenarioModelSource(SoilSource):

    def __init__(self, filename, classModel, usecaseModel):
        super(ScenarioModelSource, self).__init__(
            classModel=classModel,
            soilFileName=filename,
            usecaseModel=usecaseModel,
        )

class ScenarioEvaluationModelSource(SexSource):

    def __init__(self, filename, classModel, usecaseModel):
        super(ScenarioEvaluationModelSource, self).__init__(
            classModel=classModel,
            soilFileName=filename,
            usecaseModel=usecaseModel,
        )
