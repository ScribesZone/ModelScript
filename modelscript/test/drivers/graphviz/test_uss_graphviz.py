# coding=utf-8

import logging

from nose.plugins.attrib import attr

from modelscript.interfaces.environment import Environment
from modelscript.test.framework import TEST_CASES_DIRECTORY

import os
import modelscript.scripts.usecases.parser
from modelscript.scripts.usecases.graphviz import (
    UsecaseGraphvizPrinter
)


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('test.'+__name__)

@attr('slow')
def testGenerator_UssGraphviz():
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
    source = modelscript.scripts.usecases.parser.UsecaseModelSource(
        usecaseFileName=filename,
    )
    if not source.isValid:
        print(('#'*10+' ignore invalid file  %s' % filename ))
    else:
        usm = source.usecaseModel

        #--- diag generation: system -> .gv --------------

        # graphviz_file_path = os.path.join(
        #     USD_DIR,
        #     os.path.splitext(
        #         os.path.basename(filename)) [0]+'.usd.gv'
        # )
        graphviz_file_path=Environment.getWorkerFileName(
            filename,
            extension='.usd.gv')
        print(('TST: '+'='*80))
        print(('TST: result in %s' % graphviz_file_path))
        print(('TST: '+'='*80))
        gen = UsecaseGraphvizPrinter(usm)
        # print(gen.do(outputFile=puml_file_path))
        # #--- plantuml: .puml -> .svg ----------------------
        # puml_engine.generate(puml_file_path)
        gen.generate(graphviz_file_path, format='png')
        # gen.generate(puml_file_path, format='svg' )
        print('TST: generated')
        print(('TST: '+'='*80))

