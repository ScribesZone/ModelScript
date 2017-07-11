# coding=utf-8
import os
import logging

from test.pyuseocl import TEST_CASES_DIRECTORY
from pyuseocl.use.soil.parser import SoilSource
from pyuseocl.use.use.parser import UseFile


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

def testGenerator_AllSoilFile():
    usefilename=os.path.join(test_cases_dir,'main.use')
    uf=UseFile(usefilename)
    assert(uf.isValid)
    clm=uf.model

    for test in test_files:
        yield check_IsValid, test, clm

def check_IsValid(testFile, classModel):
    use_file = SoilSource(
        classModel=classModel,
        soilFileName=testFile,
    )
    assert(use_file.isValid)
    state=use_file.scenario.execute()
    print(state.status())
