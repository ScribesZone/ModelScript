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
import pyuseocl.use.use.parser
import pyuseocl.plantuml.objects
import pyuseocl.plantuml.engine
import pyuseocl.use.soil.parser

# TODO: add this again
# def test_UseOclModel_Simple():
#     check_isValid('Demo.use')



@attr('slow')
def testGenerator_UseOclModel_full():
    test_dir=os.path.join(
        TEST_CASES_DIRECTORY,'soil','employee')

    #--- get the class model ----------------------
    use_file_name=os.path.join(test_dir,'main.use')
    use_file = pyuseocl.use.use.parser.UseFile(
        use_file_name)
    assert(use_file.isValid)
    class_model = use_file.model

    #--- test all soil files ----------------------
    soil_files = [
        os.path.join(test_dir, f)
            for f in os.listdir(test_dir)
            if f.endswith('.soil')]

    puml_engine = pyuseocl.plantuml.engine.PlantUMLEngine()
    for soil_file_name in soil_files:
        yield check_isValid, class_model, soil_file_name, puml_engine


def check_isValid(class_model, soil_file_name, puml_engine):

    #--- parser: .soil -> scenario -------------------
    soil_source = pyuseocl.use.soil.parser.SoilSource(
        classModel=class_model,
        soilFileName=soil_file_name,
    )
    if not soil_source.isValid:
        soil_source.printStatus()
    assert soil_source.isValid
    scn = soil_source.scenario

    #--- abstract execution: scenario -> state -------
    state = scn.execute()

    #--- diag generation: state -> .puml --------------

    puml_file_path = os.path.join(
        BUILD_DIRECTORY,
        'odg',
        os.path.splitext(
            os.path.basename(soil_file_name)) [0]+'.odg.puml'
    )
    print '\n'*2+'='*80
    print 'Generating '+puml_file_path
    gen = pyuseocl.plantuml.objects.Generator(state)
    print gen.do(outputFile=puml_file_path)
    print '\n'*2+'.'*80

    #--- plantuml: .puml -> .svg ----------------------
    puml_engine.generate(puml_file_path)

