# coding=utf-8
import os
import logging

from test.modelscripts import (
    getTestFile,
    getTestFiles,
    getTestDir
)
from modelscripts.use.sex.parser import (
    SoilSource,
    SexSource,
)
from modelscripts.scripts.usecases.parser import UsecaseModelSource
from modelscripts.use.use.parser import UseSource
from modelscripts.scripts.scenarios.printer import (
    ScenarioSourcePrinter
)
from modelscripts.scripts.permissions.parser import (
    PermissionModelSource
)


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('test.' + __name__)


#---------------------------------------------------------------


test_soil_dir =getTestDir(
    'soil/employee' )
    # 'soil/employee-1')

test_soil_files = getTestFiles(
    'soil/employee',
    relative=False,
    extension='.soil')


def _getClassModelAndUsecaseModels(name):
    usefilename = os.path.join(test_soil_dir, '%s.use' % name)
    uf=UseSource(usefilename)
    assert(uf.isValid)
    clm=uf.classModel

    ucmfilename=os.path.join(test_soil_dir, '%s.ucm' % name)
    ucs=UsecaseModelSource(ucmfilename)
    assert(ucs.isValid)
    ucm=ucs.usecaseModel
    assert(ucm is not None)

    pmmfilename=os.path.join(test_soil_dir, '%s.pmm' % name)
    if os.path.isfile(pmmfilename):
        pms= PermissionModelSource(permissionFileName=pmmfilename, usecaseModel=ucm, classModel=clm)
        assert(pms.isValid)
        pmm=pms.permissionModel
        assert(pmm is not None)
    else:
        pmm=None

    return (clm,ucm,pmm)


def testGenerator_AllSoilFileWithNoUsecases():
    (clm,ucm,pmm)=_getClassModelAndUsecaseModels('main')
    for test in test_soil_files:
        yield check_IsValid, test, clm  # no sys

def testGenerator_WithUsecaseModel():
    (clm,ucm,pmm)=_getClassModelAndUsecaseModels('main')
    for test in test_soil_files:
        yield check_IsValid, test, clm, ucm, pmm

#---------------------------------------------------------------


# def check_IsValid(parseExecution, testFile, classModel, usecaseModel=None):

def check_IsValid(
        testFile,
        classModel,
        usecaseModel=None,
        permissionModel=None):

    print('='*8
          +('TEST: Analyzing %s ' % os.path.basename(testFile))
          +'='*50)
    if usecaseModel is None:
        print('Info: no usecase model provided. Usecase references will be ignored.')
    if permissionModel is None:
        print('Info: no permission model provided. Accesses will not be controlled.')
    soilSexSource = SexSource(soilFileName=testFile, classModel=classModel, usecaseModel=usecaseModel,
                              permissionModel=permissionModel)
    # assert (soilSexSource.isValid)

    if permissionModel is not None:
        print(str(permissionModel))
    p = ScenarioSourcePrinter(
        soilSexSource,
        displayEvaluation=True
    )
    print('-'*80)
    print(p.do())
    print('='*80+'\n')
