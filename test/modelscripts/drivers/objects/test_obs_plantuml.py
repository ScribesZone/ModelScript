# coding=utf-8

import logging

from nose.plugins.attrib import attr

from modelscripts.interfaces.environment import Environment
from test.modelscripts.framework import TEST_CASES_DIRECTORY

import os
import modelscripts.scripts.objects.parser
from modelscripts.scripts.objects.plantuml import (
    ObjectPlantUMLPrinter
)

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('test.'+__name__)

@attr('slow')
def testGenerator_obs_plantuml():
    test_dir=os.path.join(
        TEST_CASES_DIRECTORY,'obs')

    #--- test all files ----------------------
    files = [
        os.path.join(test_dir, f)
            for f in os.listdir(test_dir)
            if f.endswith('.obs')]

    for filename in files:
        yield doBuildDiagram, filename


def doBuildDiagram(filename):

    #--- parser: .obs -> system -------------------
    source = modelscripts.scripts.objects.parser.ObjectModelSource(
        fileName=filename,
    )
    if not source.isValid:
        print('#'*10+' ignore invalid file  %s' % filename )
    else:
        obm = source.objectModel

        puml_file_path=Environment.getWorkerFileName(
            filename,
            extension='.obs.puml')

        print('TST: '+'='*80)
        print('TST: result in %s' % puml_file_path)
        print('TST: '+'='*80)
        gen = ObjectPlantUMLPrinter(obm)
        gen.generate(puml_file_path, format='png' )
        print('TST: .png generated')
        print('TST: '+'='*80)

