# coding=utf-8

from __future__ import unicode_literals, print_function, absolute_import, division

from modelscribes.metamodels.scenarios import (
    METAMODEL
)
from modelscribes.use.sex.parser import (
    SexSource,
)

from modelscribes.scripts.scenarios.preprocessor import (
    ScsToSoilPreprocessor
)


class ScenarioEvaluationModelSource(SexSource):

    def __init__(self, originalFileName):

        super(ScenarioEvaluationModelSource, self).__init__(
            originalFileName,
            preprocessor=ScsToSoilPreprocessor())

    @property
    def metamodel(self):
        return METAMODEL


METAMODEL.registerSource(ScenarioEvaluationModelSource)