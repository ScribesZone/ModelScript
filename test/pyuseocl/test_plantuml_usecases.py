# coding=utf-8

from nose.plugins.attrib import attr

import logging
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('test.'+__name__)

from test.pyuseocl import (
    TEST_CASES_DIRECTORY,
    BUILD_DIRECTORY,
)

import os
import pyuseocl.umlscripts.usecases
import pyuseocl.plantuml.usecases
import pyuseocl.plantuml.engine

# TODO: add this again
# def test_UseOclModel_Simple():
#     check_isValid('Demo.use')

@attr('slow')
def testGenerator_UseOclModel_full():
    test_dir=os.path.join(
        TEST_CASES_DIRECTORY,'ucm')

    #--- test all files ----------------------
    files = [
        os.path.join(test_dir, f)
            for f in os.listdir(test_dir)
            if f.endswith('.ucm')]

    puml_engine = pyuseocl.plantuml.engine.PlantUMLEngine()
    for filename in files:
        yield check_isValid, filename, puml_engine


def check_isValid(filename, puml_engine):

    #--- parser: .ucs -> system -------------------
    source = pyuseocl.umlscripts.usecases.UsecasesSource(
        usecaseFileName=filename,
    )
    # if not source.isValid:
    #     source.printStatus()
    assert source.isValid
    system = source.system

    #--- diag generation: system -> .puml --------------

    puml_file_path = os.path.join(
        BUILD_DIRECTORY,
        'ucd',
        os.path.splitext(
            os.path.basename(filename)) [0]+'.ucd.puml'
    )
    print('\n'*2+'='*80)
    print('Generating '+puml_file_path)
    gen = pyuseocl.plantuml.usecases.Generator(system)
    print(gen.do(outputFile=puml_file_path))
    print('\n'*2+'.'*80)

    #--- plantuml: .puml -> .svg ----------------------
    print('====='+puml_file_path)
    puml_engine.generate(puml_file_path)
    print('=====')

