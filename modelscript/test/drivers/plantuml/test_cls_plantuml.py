# coding=utf-8

import logging

from nose.plugins.attrib import attr

from modelscript.interfaces.environment import Environment
from modelscript.test.framework import TEST_CASES_DIRECTORY

import os
import modelscript.scripts.classes.parser
from modelscript.scripts.classes.plantuml import (
    ClassPlantUMLPrinter
)

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('test.'+__name__)

@attr('slow')
def testGenerator_cls_plantuml():
    test_dir=os.path.join(
        TEST_CASES_DIRECTORY,'cls')

    #--- test all files ----------------------
    files = [
        os.path.join(test_dir, f)
            for f in os.listdir(test_dir)
            if f.endswith('.cls')]

    for filename in files:
        yield doBuildDiagram, filename


def doBuildDiagram(filename):

    #--- parser: .obs -> system -------------------
    source = modelscript.scripts.classes.parser.ClassModelSource(
        fileName=filename,)
    if not source.isValid:
        print((('##'*40+'\n')*10))
        print('==> IGNORING INVALID MODEL')
        print((('##'*40+'\n')*10))
    else:
        obm = source.classModel

        puml_file_path=Environment.getWorkerFileName(
            filename,
            extension='.cls.puml')

        print(('TST: '+'='*80))
        print(('TST: result in %s' % puml_file_path))
        print(('TST: '+'='*80))
        gen = ClassPlantUMLPrinter(obm)
        gen.generate(puml_file_path, format='png' )
        print('TST: .png generated')
        print(('TST: '+'='*80))

