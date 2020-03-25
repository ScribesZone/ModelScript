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
import modelscript.scripts.objects.parser
from modelscript.scripts.stories.useprinter import (
    UseStoryPrinter)
from modelscript.base.issues import (
    FatalError)
from modelscript.base.grammars import (
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
    source = modelscript.scripts.objects.parser.ObjectModelSource(
        fileName=filename,)

    if not source.isValid:
        print((('##'*40+'\n')*10))
        print('==> IGNORING INVALID MODEL')
        print((('##'*40+'\n')*10))
        return

    obm = source.objectModel
    if not obm.hasClassModel:
        print((('##'*40+'\n')*10))
        print('==> OBJECTY MODEL HAS NO CLASS MODEL : IGNORED')
        print((('##'*40+'\n')*10))
        return

    #------------ generate .soil ----------------------
    soil_file_path=Environment.getWorkerFileName(
        filename,
        extension='.soil',
        workerSpace='inline')
    story=obm.storyEvaluation.step
    usePrinter = UseStoryPrinter(story)
    usePrinter.do()
    usePrinter.save(soil_file_path)
    print(('TST: '+'='*80))
    print(('TST: result in %s' % soil_file_path))
    print(('TST: '+'='*80))

    clm = obm.classModel
    class_ocl_checker=clm.classOCLChecker
    print(('TST:', class_ocl_checker.withUSE, not obm.hasBigIssues))
    if class_ocl_checker.withUSE and not obm.hasBigIssues:
        use_file_path=class_ocl_checker.useFileName
        engine=USEEngine
        engine.executeSoilFileAsTrace(
            useFile=use_file_path,
            soilFile=soil_file_path,
            workerSpace='self')

