# coding=utf-8

import logging

from nose.plugins.attrib import attr


from test.modelscripts import (
    TEST_CASES_DIRECTORY,
    getBuildDir,
)

import os
import modelscripts.scripts.usecases.parser
from modelscripts.scripts.usecases.graphviz import (
    UsecaseGraphvizPrinter
)


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('test.'+__name__)

USD_DIR=getBuildDir('gen/tools/usecases')

# TODO: add this again
# def test_UseOclModel_Simple():
#     check_isValid('Demo.use')

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

        #--- diag generation: system -> .gv --------------

        graphviz_file_path = os.path.join(
            USD_DIR,
            os.path.splitext(
                os.path.basename(filename)) [0]+'.usd.gv'
        )
        print('TST: '+'='*80)
        print('TST: result in %s' % graphviz_file_path)
        print('TST: '+'='*80)
        gen = UsecaseGraphvizPrinter(usm)
        # print(gen.do(outputFile=puml_file_path))
        # #--- plantuml: .puml -> .svg ----------------------
        # puml_engine.generate(puml_file_path)
        gen.do()
        # gen.generate(puml_file_path, format='svg' )
        print('TST: generated')
        print('TST: '+'='*80)

