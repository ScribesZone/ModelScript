# coding=utf-8
import os
import logging

from test.pyuseocl import TEST_CASES_DIRECTORY
from pyuseocl.umlscripts.usecases import UsecasesSource

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('test.' + __name__)

test_cases_dir = os.path.join(
    TEST_CASES_DIRECTORY,
    'ucm')

test_files = [
    os.path.join(test_cases_dir,f)
    for f in os.listdir(test_cases_dir)
    if f.endswith('.ucm')]

def testGenerator_AllSoilFile():
    for test in test_files:
        yield check_IsValid, test

def check_IsValid(testFile):
    ucs = UsecasesSource(testFile)
    assert(ucs.isValid)

