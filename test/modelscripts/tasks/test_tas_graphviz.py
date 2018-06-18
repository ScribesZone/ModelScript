# coding=utf-8

import logging

from nose.plugins.attrib import attr

from modelscripts.interfaces.environment import Environment
from test.modelscripts import (
    TEST_CASES_DIRECTORY
)

import os
import modelscripts.scripts.tasks.parser
from modelscripts.scripts.tasks.graphviz import (
    TaskGraphvizPrinter
)


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('test.'+__name__)

@attr('slow')
def testGenerator_UseOclModel_full():
    test_dir=os.path.join(
        TEST_CASES_DIRECTORY,'tas')

    #--- test all files ----------------------
    files = [
        os.path.join(test_dir, f)
            for f in os.listdir(test_dir)
            if f.endswith('.tas')]

    for filename in files:
        yield doBuildDiagram, filename


def doBuildDiagram(filename):

    source = modelscripts.scripts.tasks.parser.TaskModelSource(
        taskFileName=filename,
    )
    if not source.isValid:
        print('#'*10+' ignore invalid file  %s' % filename )
    else:
        model = source.model
        graphviz_file_path=Environment.getWorkerFileName(
            filename,
            extension='.tas.gv')
        print('TST: '+'='*80)
        print('TST: result in %s' % graphviz_file_path)
        print('TST: '+'='*80)
        gen = TaskGraphvizPrinter(model)
        # print(gen.do(outputFile=puml_file_path))
        # #--- plantuml: .puml -> .svg ----------------------
        # puml_engine.generate(puml_file_path)
        gen.generate(graphviz_file_path, format='png')
        # gen.generate(puml_file_path, format='svg' )
        print('TST: generated')
        print('TST: '+'='*80)

