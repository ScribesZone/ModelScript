# coding=utf-8

from __future__ import print_function
import os.path

from test.modelscripts import TEST_CASES_DIRECTORY
from  modelscribes.use.engine import (
    USEEngine,
)
import modelscribes.use.engine

def test_USEEngine_withUseOCL():
    assert USEEngine.withUseOCL()

def test_USEEngine_withoutUseOCL():
    tmp_USE_OCL_COMMAND= modelscribes.use.engine.USE_OCL_COMMAND
    modelscribes.use.engine.USE_OCL_COMMAND = 'xyz'
    try:
        assert not USEEngine.withUseOCL()
    finally:
        modelscribes.use.engine.USE_OCL_COMMAND=tmp_USE_OCL_COMMAND

def test_USEEngine_useVersion():
    version = USEEngine.useVersion()
    assert(version.startswith('4.'))

#    assert(version.startswith('3.') or version.startswith('4.'))

def test_USEEngine_analyzeUSEModel_KO():
    file = os.path.join(TEST_CASES_DIRECTORY,
                       'use','issues','empty.use')
    USEEngine.analyzeUSEModel(file)
    assert USEEngine.commandExitCode != 0

def test_USEEngine_analyzeUSEModel():
    file = os.path.join(TEST_CASES_DIRECTORY,
                        'use', 'Demo.use')
    USEEngine.analyzeUSEModel(file)
    assert USEEngine.commandExitCode == 0

def test_USEEngine_executeSoilFile():
    usefile = os.path.join(TEST_CASES_DIRECTORY,
                        'useengine', 'main.cls')
    for sf in [
        'Demo0.soil','Demo01.soil', 'Demo5.soil',
        'Demo2.soil', 'Demo3.soil', 'Demo6.soil']:
        soilfile = os.path.join(TEST_CASES_DIRECTORY,
                            'useengine', sf)

        print('=== asTrace %s '%soilfile)
        USEEngine.executeSoilFileAsTrace(usefile, soilfile)
        print('= '+sf+'='*60)
        print(USEEngine.outAndErr)
        assert USEEngine.commandExitCode == 0

        print('=== asSex %s '%soilfile)
        USEEngine.executeSoilFileAsSex(usefile, soilfile)
        print('= '+sf+'='*60)
        print(USEEngine.outAndErr)
        assert USEEngine.commandExitCode == 0

def test_USEEngine_executeSoilFileAsTrace_KO():
    usefile = os.path.join(TEST_CASES_DIRECTORY,
                        'useengine', 'main.cls')
    for sf in ['Demo666.soil','Demo666.1.soil'
        , 'Demo666.2.soil','Demo666.3.soil','Demo666.4.soil']:
        soilfile = os.path.join(TEST_CASES_DIRECTORY,
                            'useengine', '_negative', sf)
        USEEngine.executeSoilFileAsTrace(usefile, soilfile)
        print('= '+sf+'='*60)
        print(USEEngine.outAndErr)
        assert USEEngine.commandExitCode == 0
        assert (
            'Error: ' in USEEngine.outAndErr
            or '<input>:1:' in USEEngine.outAndErr )

def test_USEEngine_noUSEBinary():
    tmp_USE_OCL_COMMAND= modelscribes.use.engine.USE_OCL_COMMAND
    modelscribes.use.engine.USE_OCL_COMMAND= 'useabc'
    anyusefile = os.path.join(TEST_CASES_DIRECTORY,
                        'soil','main.cls')
    print(modelscribes.use.engine.USE_OCL_COMMAND)
    USEEngine._execute(
        useSource=anyusefile,
        soilFile=USEEngine._soilHelper('infoModelAndQuit.soil'))
    try:
        assert USEEngine.commandExitCode != 0
    finally:
        modelscribes.use.engine.USE_OCL_COMMAND=tmp_USE_OCL_COMMAND