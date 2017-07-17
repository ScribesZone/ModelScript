# coding=utf-8

from __future__ import print_function
import os.path

from test.pyuseocl import TEST_CASES_DIRECTORY
from  pyuseocl.use.engine.engine import USEEngine

def test_USEEngine_withUseOCL():
    assert(USEEngine.withUseOCL)

def test_USEEngine_useVersion():
    version = USEEngine.useVersion()
    assert(version.startswith('4.'))

#    assert(version.startswith('3.') or version.startswith('4.'))

def test_USEEngine_analyzeUSEModel_KO():
    file = os.path.join(TEST_CASES_DIRECTORY,
                       'use','useerrors','empty.use')
    USEEngine.analyzeUSEModel(file)
    assert USEEngine.commandExitCode != 0

def test_USEEngine_analyzeUSEModel():
    file = os.path.join(TEST_CASES_DIRECTORY,
                        'use', 'Demo.use')
    USEEngine.analyzeUSEModel(file)
    assert USEEngine.commandExitCode == 0

def test_USEEngine_executeSoilFile():
    usefile = os.path.join(TEST_CASES_DIRECTORY,
                        'soil', 'employee','main.use')
    for sf in ['Demo0.soil','Demo01.soil', 'Demo1.soil', 'Demo2.soil', 'Demo3.soil',
               'Demo6.soil', 'Demo7.soil']:
        soilfile = os.path.join(TEST_CASES_DIRECTORY,
                            'soil', 'employee',sf)
        USEEngine.executeSoilFile(usefile, soilfile)
        print('= '+sf+'='*60)
        print(USEEngine.outAndErr)
        assert USEEngine.commandExitCode == 0

def test_USEEngine_executeSoilFile_KO():
    usefile = os.path.join(TEST_CASES_DIRECTORY,
                        'soil', 'employee','main.use')
    for sf in ['Demo666.soil','Demo666.1.soil'
        , 'Demo666.2.soil','Demo666.3.soil','Demo666.4.soil']:
        soilfile = os.path.join(TEST_CASES_DIRECTORY,
                            'soil', 'employee', '_negative', sf)
        USEEngine.executeSoilFile(usefile, soilfile)
        print('= '+sf+'='*60)
        print(USEEngine.outAndErr)
        assert USEEngine.commandExitCode == 0
        assert (
            'Error: ' in USEEngine.outAndErr
            or '<input>:1:' in USEEngine.outAndErr )