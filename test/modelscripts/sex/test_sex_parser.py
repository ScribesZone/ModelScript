# coding=utf-8
import os
import logging

from test.modelscripts import TEST_CASES_DIRECTORY
from modelscripts.use.sex.parser import (
    SoilSource,
    SexSource,
)
from modelscripts.scripts.usecases.parser import UsecaseModelSource
from modelscripts.use.use.parser import UseSource
from modelscripts.scripts.scenarios.printer import ScenarioPrinter
from modelscripts.scripts.permissions.parser import (
    PermissionModelSource
)


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('test.' + __name__)


#---------------------------------------------------------------


test_soil_dir = os.path.join(
    TEST_CASES_DIRECTORY,
    'soil',
    # 'employee-1')
    'employee')

test_soil_files = [
    os.path.join(test_soil_dir,f)
    for f in os.listdir(test_soil_dir)
    if f.endswith('.soil')]


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


def te____________stGenerator_AllSoilFileWithNoUsecases():
    (clm,ucm,pmm)=_getClassModelAndUsecaseModels('main')
    for test in test_soil_files:
        yield check_IsValid, test, clm  # no sys

def testGenerator_WithUsecaseModel():
    (clm,ucm,pmm)=_getClassModelAndUsecaseModels('main')
    for test in test_soil_files:
        yield check_IsValid, test, clm, ucm, pmm

#---------------------------------------------------------------


# test_sex_dir = os.path.join(
#     TEST_CASES_DIRECTORY,
#     'sex')
#
# test_sex_files = [
#     os.path.join(test_sex_dir,f)
#     for f in os.listdir(test_sex_dir)
#     if f.endswith('.sex')]
#
# def _getSexClassModel(name):
#     usefilename = os.path.join(test_sex_dir, '%s.use' % name)
#     uf=UseSource(usefilename)
#     assert(uf.isValid)
#     clm=uf.classModel
#     return clm
#
# def testGenerator_Sex():
#     clm=_getSexClassModel('main')
#     for test in test_sex_files:
#         yield check_IsValid, 'sex', test, clm


#---------------------------------------------------------------


# def check_IsValid(parseExecution, testFile, classModel, usecaseModel=None):

def check_IsValid(
        testFile,
        classModel,
        usecaseModel=None,
        permissionModel=None):

    print('='*8
          +(' Analyzing %s ' % os.path.basename(testFile))
          +'='*50)
    if usecaseModel is None:
        print('Info: no usecase model provided. Usecase references will be ignored.')
    if permissionModel is None:
        print('Info: no permission model provided. Accesses will not be controlled.')
    soilSexSource = SexSource(soilFileName=testFile, classModel=classModel, usecaseModel=usecaseModel,
                              permissionModel=permissionModel)
    assert (soilSexSource.isValid)

    if permissionModel is not None:
        print(str(permissionModel))
    p = ScenarioPrinter(
        soilSexSource.scenario,
        displayEvaluation=True
    )
    print('-'*80)
    print(p.do())
    print('='*80+'\n')
