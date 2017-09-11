# coding=utf-8
import os

from test.modelscripts import (
    getTestFiles,
)
from test.modelscripts.sex import _getModelsForScenario
from modelscripts.use.sex.parser import (
    SexSource,
)
from modelscripts.scripts.scenarios.printer import (
    ScenarioSourcePrinter
)


#---------------------------------------------------------------

SOIL_REL_DIR='soil/issues'


def testGenerator_RunWithNoUCNoPMM():
    (clm,_1,_2)=_getModelsForScenario(
        SOIL_REL_DIR,
        'main.use',
        None,
        None)
    abs_test_soil_files = getTestFiles(
        SOIL_REL_DIR,
        relative=False,
        extension='.soil')
    for abs_test in abs_test_soil_files:
        # https://stackoverflow.com/questions/11189699/change-names-of-tests-created-by-nose-test-generators
        # check_hasIssues.description=os.path.basename(abs_test)
        # check_hasIssues.__name__ = os.path.basename(abs_test)
        yield check_hasIssues, abs_test, clm

def check_hasIssues(
        absTestFile,
        classModel):

    print('='*8
      +(' TESTING %s with no usecase model' % os.path.basename(absTestFile))
          +'='*50)

    # soilSexSource = SoilSource(
    #     soilFileName=relTestFile,
    #     classModel=classModel)

    soilSexSource = SexSource(
        soilFileName=absTestFile,
        classModel=classModel,
        )

    ScenarioSourcePrinter(
        soilSexSource,
        displayEvaluation=False
    ).display()

    assert soilSexSource.hasIssues


