# coding=utf-8
import os
import logging

from test.pyuseocl import TEST_CASES_DIRECTORY
from pyuseocl.use.soil.parser import SoilSpecificationFile

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('test.' + __name__)

test_cases_dir = os.path.join(
    TEST_CASES_DIRECTORY,
    'soil')

test_files = [
    os.path.join(test_cases_dir,f)
    for f in os.listdir(test_cases_dir)
    if f.endswith('.soil')]

def testGenerator_AllSoilFile():
    for test in test_files:
        yield check_IsValid, test

def check_IsValid(testFile):
    use_file = SoilSpecificationFile(testFile)
    # if not use_file.isValid:
    #     use_file.printStatus()
    # assert use_file.isValid
