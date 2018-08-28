# coding=utf-8

import logging

from nose.plugins.attrib import attr

from modelscripts.interfaces.environment import Environment
from test.modelscripts.framework import TEST_CASES_DIRECTORY

import os
import modelscripts.scripts.usecases.parser
from modelscripts.scripts.usecases.plantuml import (
    UsecasePlantUMLPrinter
)

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('test.'+__name__)

@attr('slow')
def testGenerator_UseOclModel_full():
    test_dir=os.path.join(
        TEST_CASES_DIRECTORY,'uss')

    #--- test all files ----------------------
    files = [
        os.path.join(test_dir, f)
            for f in os.listdir(test_dir)
            if f.endswith('.uss')]

    for filename in files:
        yield doBuildDiagram, filename


def doBuildDiagram(filename):

    #--- parser: .uss -> system -------------------
    source = modelscripts.scripts.usecases.parser.UsecaseModelSource(
        usecaseFileName=filename,
    )
    if not source.isValid:
        print('#'*10+' ignore invalid file  %s' % filename )
    else:
        usm = source.usecaseModel

        #--- diag generation: system -> .puml --------------

        # puml_file_path = os.path.join(
        #     USD_DIR,
        #     os.path.splitext(
        #         os.path.basename(filename)) [0]+'.usd.puml'
        # )
        puml_file_path=Environment.getWorkerFileName(
            filename,
            extension='.usd.puml')

        print('TST: '+'='*80)
        print('TST: result in %s' % puml_file_path)
        print('TST: '+'='*80)
        gen = UsecasePlantUMLPrinter(usm)
        # print(gen.do(outputFile=puml_file_path))
        # #--- plantuml: .puml -> .svg ----------------------
        # puml_engine.generate(puml_file_path)
        gen.generate(puml_file_path, format='png' )
        print('TST: .png generated')
        print('TST: '+'='*80)

