# coding=utf-8
import os
import logging

from test.pyuseocl import TEST_CASES_DIRECTORY
from pyuseocl.use.sex.parser import SoilSource
from pyuseocl.umlscripts.usecases import UsecasesSource
from pyuseocl.use.use.parser import UseSource


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('test.' + __name__)

test_cases_dir = os.path.join(
    TEST_CASES_DIRECTORY,
    'soil',
    'employee')

test_files = [
    os.path.join(test_cases_dir,f)
    for f in os.listdir(test_cases_dir)
    if f.endswith('.soil')]

def _getClassModelAndUsecaseModels(name):
    usefilename = os.path.join(test_cases_dir, '%s.use' % name)
    uf=UseSource(usefilename)
    assert(uf.isValid)
    clm=uf.model
    ucmfilename=os.path.join(test_cases_dir, '%s.ucm' % name)
    ucs=UsecasesSource(ucmfilename)
    assert(ucs.isValid)
    sys=ucs.system
    assert(sys is not None)
    return (clm,sys)

def testGenerator_AllSoilFileWithNoUsecases():
    (clm,sys)=_getClassModelAndUsecaseModels('main')
    for test in test_files:
        yield check_IsValid, test, clm, sys

def testGenerator_WithUseCaseModel():
    (clm,sys)=_getClassModelAndUsecaseModels('main')
    for test in test_files:
        yield check_IsValid, test, clm, sys

def check_IsValid(testFile, classModel, sys=None):
    use_file = SoilSource(
        classModel=classModel,
        soilFileName=testFile,
        system=sys,
    )
    assert(use_file.isValid)
    state=use_file.scenario.execute()
    state=use_file.scenario.executeAfterContext()
    # print(state.status())
