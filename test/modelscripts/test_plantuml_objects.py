# coding=utf-8

import logging

from nose.plugins.attrib import attr

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('test.'+__name__)

from test.modelscripts import (
    TEST_CASES_DIRECTORY,
    BUILD_DIRECTORY,
)

import os
import modelscripts.use.use.parser
import modelscripts.scripts.objects.plantuml
import modelscripts.diagrams.plantuml.engine
import modelscripts.use.sex.parser

# TODO: add this again
# def test_UseOclModel_Simple():
#     check_isValid('Demo.use')



@attr('slow')
def testGenerator_UseOclModel_full():
    test_dir=os.path.join(
        TEST_CASES_DIRECTORY,'soil','employee')

    #--- get the class model ----------------------
    use_file_name=os.path.join(test_dir,'main.use')
    use_file = modelscripts.use.use.parser.UseSource(
        use_file_name)
    assert(use_file.isValid)
    class_model = use_file.classModel

    #--- test all soil files ----------------------
    soil_files = [
        os.path.join(test_dir, f)
            for f in os.listdir(test_dir)
            if f.endswith('.soil')]

    puml_engine = modelscripts.diagrams.plantuml.engine.PlantUMLEngine()
    for soil_file_name in soil_files:
        yield check_isValid, class_model, soil_file_name, puml_engine


def check_isValid(class_model, soil_file_name, puml_engine):

    #--- parser: .soil -> scenario -------------------
    soil_source = modelscripts.use.sex.parser.SoilSource(
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
    print('\n'*2+'='*80)
    print('Generating '+puml_file_path)
    gen = modelscripts.scripts.objects.plantuml.Generator(state)
    print( gen.do(outputFile=puml_file_path))
    print('\n'*2+'.'*80)

    #--- plantuml: .puml -> .svg ----------------------
    puml_engine.generate(puml_file_path)

