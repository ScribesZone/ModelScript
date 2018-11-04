# coding=utf-8
from __future__ import print_function
import logging

from modelscripts.interfaces.environment import Environment
from modelscripts.test.framework import TEST_CASES_DIRECTORY
from modelscripts.tools.use.engine import (
    USEEngine)
import os
import modelscripts.scripts.objects.parser
from modelscripts.scripts.stories.useprinter import (
    UseStoryPrinter)
from modelscripts.tools.use.checkparser import (
    UseCheckOutputsParser)

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('test.'+__name__)

def testGenerator_obs_useprinter():
    test_dir=os.path.join(
        TEST_CASES_DIRECTORY,'obs')

    #--- test all files ----------------------
    files = [
        os.path.join(test_dir, f)
            for f in os.listdir(test_dir)
            if f.endswith('.obs')
            and 'building' in f ###############################
    ]

    for filename in files:
        yield doPrintUse, filename


def doPrintUse(filename):

    #--- parser: .obs -> system -------------------
    source = modelscripts.scripts.objects.parser.ObjectModelSource(
        fileName=filename)
    if not source.isValid:
        print(('##'*40+'\n')*10)
        print('==> IGNORING INVALID MODEL')
        print(('##'*40+'\n')*10)
    else:
        obm = source.objectModel

        #------------ generate .soil ----------------------
        soil_file_path=Environment.getWorkerFileName(
            filename,
            extension='.soil',
            workerSpace='inline')
        story=obm.storyEvaluation.step
        usePrinter = UseStoryPrinter(story)
        usePrinter.do()
        usePrinter.save(soil_file_path)
        print('TST: '+'='*80)
        print('TST: generated .soil in %s' % soil_file_path)
        print('TST: '+'='*80)

        clm = obm.classModel
        class_ocl_checker=clm.classOCLChecker
        print('TST:', class_ocl_checker.withUSE, not obm.hasBigIssues)
        if class_ocl_checker.withUSE and not obm.hasBigIssues:
            use_file_path=class_ocl_checker.useFileName
            engine=USEEngine
            trace_filename=\
                engine.executeSoilFileAsTrace(
                    useFile=use_file_path,
                    soilFile=soil_file_path,
                    workerSpace='self')
            print('TST: ' + '=' * 80)
            print('TST: use output in %s' % trace_filename)
            print('TST: ' + '=' * 80)

            parser=UseCheckOutputsParser(trace_filename)
            parser.parse()
            print('TST:', parser.useOutput)
            for checkPoint in parser.useOutput.checkPoints:
                print('TST: ------ check point')
                for inv_output in checkPoint.invariantOutputs:
                    print(inv_output.className
                          +'.'+inv_output.invariantName
                          +' '+unicode(inv_output.hasFailed))
                    # if inv_output.hasFailed:
                    #     print('TST:    ',inv_output.violatingObjectNames)
                    #     print('TST:    ',inv_output.violatingObjectType)
                    #     print('TST:    ',inv_output.resultValue)
                    #     print('TST:    ',inv_output.resultType)
                    #     for expr in inv_output.subexpressions:
                    #         print('TST: >>>', expr)

