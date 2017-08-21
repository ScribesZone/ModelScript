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
from modelscripts.use.sex.printer import SoilPrinter, SexPrinter


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('test.' + __name__)


#---------------------------------------------------------------


test_soil_dir = os.path.join(
    TEST_CASES_DIRECTORY,
    'soil',
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
    return (clm,ucm)

def testGenerator_AllSoilFileWithNoUsecases():
    (clm,sys)=_getClassModelAndUsecaseModels('main')
    for test in test_soil_files:
        yield check_IsValid, 'soil', test, clm  # no sys

def testGenerator_WithUsecaseModel():
    (clm,sys)=_getClassModelAndUsecaseModels('main')
    for test in test_soil_files:
        yield check_IsValid, 'soil', test, clm, sys

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


def check_IsValid(parseExecution, testFile, classModel, usecaseModel=None):
    if not parseExecution:
        soilSexSource = SoilSource(
            classModel=classModel,
            soilFileName=testFile,
            usecaseModel=usecaseModel,
        )
        assert (soilSexSource.isValid)
        p = SoilPrinter(
            soilSexSource.scenario
        )
    else:
        soilSexSource = SexSource(
            classModel=classModel,
            soilFileName=testFile,
            usecaseModel=usecaseModel,
        )
        assert (soilSexSource.isValid)
        p = SexPrinter(
            soilSexSource.scenarioEvaluation
        )
    print('='*80)
    print(p.do())
    state=soilSexSource.scenario.execute()
    state=soilSexSource.scenario.executeAfterContext()
    # print(state.status())