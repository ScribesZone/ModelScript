# coding=utf-8
import os
import logging

from test.modelscripts import (
    getTestFiles,
)
from modelscribes.use.sex.parser import (
    SexSource,
)
from test.modelscripts.sex import _getModelsForScenario

from modelscribes.scripts.scenarios.printer import (
    ScenarioSourcePrinter
)

SOIL_REL_DIR='soil/employee'


#


def testGenerator_AllSoilFileWithNoUsecases():
    (clm,ucm,pmm)=_getModelsForScenario(
        SOIL_REL_DIR,
        'main.use',
        None,
        None)
    abs_test_soil_files = getTestFiles(
        SOIL_REL_DIR,
        relative=False,
        extension='.soil')
    for abs_test in abs_test_soil_files:
        yield check_hasNoIssues, abs_test, clm # no ucm, no pmm

# def testGenerator_WithUsecaseModel():
#     (clm,ucm,pmm)=_getClassModelAndUsecaseModels('main')
#     for test in test_soil_files:
#         yield check_IsValid, test, clm, ucm, pmm

#---------------------------------------------------------------

def check_hasNoIssues(
        absTestFile,
        classModel,
        usecaseModel=None,
        permissionModel=None):

    print('='*8
          +(' TESTING %s' % os.path.basename(absTestFile))
          +'='*50)
    if usecaseModel is None:
        print('Info: no usecase model provided. Usecase references will be ignored.')
    if permissionModel is None:
        print('Info: no permission model provided. Accesses will not be controlled.')
    soilSexSource = SexSource(
        soilFileName=absTestFile,
        classModel=classModel,
        usecaseModel=usecaseModel,
        permissionModel=permissionModel)

    # if permissionModel is not None:
    #     print(str(permissionModel))
    ScenarioSourcePrinter(
        soilSexSource,
        displayEvaluation=True
    ).display()
    assert soilSexSource.isValid
