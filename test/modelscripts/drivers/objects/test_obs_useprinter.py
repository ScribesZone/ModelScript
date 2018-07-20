# coding=utf-8
from typing import Text
import logging
import re
from nose.plugins.attrib import attr

from modelscripts.interfaces.environment import Environment
from test.modelscripts.drivers import (
    TEST_CASES_DIRECTORY,
)
from modelscripts.tools.use.engine import (
    USEEngine)
from modelscripts.base.printers import AbstractPrinterConfig
import os
import modelscripts.scripts.objects.parser
from modelscripts.scripts.stories.useprinter import (
    UseStoryPrinter
)
from modelscripts.base.issues import (
    FatalError
)
from modelscripts.base.grammars import (
    AST)

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('test.'+__name__)

def testGenerator_cls_obsprinter():
    test_dir=os.path.join(
        TEST_CASES_DIRECTORY,'obs')

    #--- test all files ----------------------
    files = [
        os.path.join(test_dir, f)
            for f in os.listdir(test_dir)
            if f.endswith('.obs')
            # and f.endswith('buildings.cls')
    ]

    for filename in files:
        yield doPrintUse, filename


def doPrintUse(filename):

    #--- parser: .obs -> system -------------------
    source = modelscripts.scripts.objects.parser.ObjectModelSource(
        fileName=filename,)
    if not source.isValid:
        print(('##'*40+'\n')*10)
        print('==> IGNORING INVALID MODEL')
        print(('##'*40+'\n')*10)
    else:
        obm = source.objectModel

        soil_file_path=Environment.getWorkerFileName(
            filename,
            extension='.soil')
        obm. XXX
        print('TST: '+'='*80)
        print('TST: result in %s' % soil_file_path)
        print('TST: '+'='*80)
        story=obm.storyEvaluation.step
        usePrinter = UseStoryPrinter(story)
        usePrinter.do()
        usePrinter.save(soil_file_path)
        print('TST: .soil generated')


        engine=USEEngine
        engine.executeSoilFileAsTrace(
            useFile=
            soilFile=soil_file_path)

        XXX
