# coding=utf-8

import os.path

from test.pyuseocl import TEST_CASES_DIRECTORY
from  pyuseocl.use.engine.engine import USEEngine

def test_USEEngine_useVersion():
    version = USEEngine.useVersion()
    assert(version.startswith('4.'))

#    assert(version.startswith('3.') or version.startswith('4.'))

def test_USEEngine_analyzeUSEModel_KO():
    file = os.path.join(TEST_CASES_DIRECTORY,
                       'use','errors','reallyEmpty.use')
    USEEngine.analyzeUSEModel(file)
    assert USEEngine.commandExitCode != 0


def test_USEEngine_analyzeUSEModel():
    file = os.path.join(TEST_CASES_DIRECTORY,
                        'use', 'Binary1.use')
    USEEngine.analyzeUSEModel(file)
    assert USEEngine.commandExitCode == 0

