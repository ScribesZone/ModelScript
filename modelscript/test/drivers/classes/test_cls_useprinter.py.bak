# coding=utf-8
from typing import Text
import logging
import re
from nose.plugins.attrib import attr

from modelscript.interfaces.environment import Environment
from modelscript.test.framework import TEST_CASES_DIRECTORY
from modelscript.tools.use.engine import (
    USEEngine)
from modelscript.base.printers import AbstractPrinterConfig
import os
import modelscript.scripts.classes.parser
from modelscript.scripts.classes.useprinter import (
    UseClassPrinter
)
from modelscript.base.issues import (
    FatalError
)
from modelscript.base.grammars import (
    AST)

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('test.'+__name__)

def testGenerator_cls_useprinter():
    test_dir=os.path.join(
        TEST_CASES_DIRECTORY,'cls')

    #--- test all files ----------------------
    files = [
        os.path.join(test_dir, f)
            for f in os.listdir(test_dir)
            if f.endswith('.cls')
            and f.endswith('buildings.cls')]

    for filename in files:
        yield doPrintUse, filename





def doPrintUse(filename):

    #--- parser: .obs -> system -------------------
    source = modelscript.scripts.classes.parser.ClassModelSource(
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
        usePrinter = UseClassPrinter(scm)
        usePrinter.do()
        usePrinter.save(use_file_path)
        print('TST: .use generated')
        # print('TST: '+'='*80)
        # getUSEResults(usePrinter, use_file_path)