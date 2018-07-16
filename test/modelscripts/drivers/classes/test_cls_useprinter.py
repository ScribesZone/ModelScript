# coding=utf-8

import logging

from nose.plugins.attrib import attr

from modelscripts.interfaces.environment import Environment
from test.modelscripts.drivers import (
    TEST_CASES_DIRECTORY,
)
from modelscripts.base.printers import AbstractPrinterConfig
import os
import modelscripts.scripts.classes.parser
from modelscripts.scripts.classes.useprinter import (
    UsePrinter
)

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('test.'+__name__)

def testGenerator_cls_plantuml():
    test_dir=os.path.join(
        TEST_CASES_DIRECTORY,'cls')

    #--- test all files ----------------------
    files = [
        os.path.join(test_dir, f)
            for f in os.listdir(test_dir)
            if f.endswith('.cls')]

    for filename in files:
        yield doPrintUse, filename



def doPrintUse(filename):

    #--- parser: .obs -> system -------------------
    source = modelscripts.scripts.classes.parser.ClassModelSource(
        fileName=filename,)
    if not source.isValid:
        print(('##'*40+'\n')*10)
        print('==> IGNORING INVALID MODEL')
        print(('##'*40+'\n')*10)
    else:
        scm = source.classModel

        use_file_path=Environment.getWorkerFileName(
            filename,
            extension='.use')

        print('TST: '+'='*80)
        print('TST: result in %s' % use_file_path)
        print('TST: '+'='*80)
        gen = UsePrinter(scm)
        gen.do()
        gen.save(use_file_path)
        print('TST: .use generated')
        print('TST: '+'='*80)

