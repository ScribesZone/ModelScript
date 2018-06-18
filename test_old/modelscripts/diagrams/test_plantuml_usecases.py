# coding=utf-8

import logging

from nose.plugins.attrib import attr


from test.modelscripts import (
    TEST_CASES_DIRECTORY,
    getBuildDir,
)

import os
import modelscripts.scripts.usecases.parser
import modelscripts.scripts.usecases.plantuml
import modelscripts.tools.plantuml.engine

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('test.'+__name__)

USD_DIR=getBuildDir('gen/tools/usecases')

@attr('slow')
def testGenerator_UseOclModel_full():
    test_dir=os.path.join(
        TEST_CASES_DIRECTORY,'uss')

    #--- test all files ----------------------
    files = [
        os.path.join(test_dir, f)
            for f in os.listdir(test_dir)
            if f.endswith('.uss')]

    puml_engine = modelscripts.tools.plantuml.engine.PlantUMLEngine()
    for filename in files:
        yield doGraph, filename, puml_engine


def doGraph(filename, puml_engine):

    #--- parser: .uss -> system -------------------
    source = modelscripts.scripts.usecases.parser.UsecaseModelSource(
        usecaseFileName=filename,
    )
    if not source.isValid:
        print('#'*10+' ignore invalid file  %s' % filename )
    else:
        usm = source.usecaseModel

        #--- diag generation: system -> .puml --------------

        puml_file_path = os.path.join(
            USD_DIR,
            os.path.splitext(
                os.path.basename(filename)) [0]+'.usd.puml'
        )
        print('\n'*2+'='*80)
        print('Generating '+puml_file_path)
        gen = modelscripts.scripts.usecases.plantuml.UsecasePlantUMLPrinter(usm)
        print(gen.do(outputFile=puml_file_path))
        print('\n'*2+'.'*80)

        #--- plantuml: .puml -> .svg ----------------------
        print('====='+puml_file_path)
        puml_engine.generate(puml_file_path)
        print('=====')

