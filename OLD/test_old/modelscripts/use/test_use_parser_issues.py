# coding=utf-8
from __future__ import print_function

import logging

import modelscripts.scripts.use_classes.parser
import modelscripts.scripts.use_classes.printer

from modelscripts.base.modelprinters import (
    ModelSourcePrinter
)
from modelscripts.metamodels import (
    classes
)
from modelscripts.use.use.parser import (
    UseModelSource
)
from test.modelscripts import (
    assertIssueBox,
    F, E, W, I, H,
    checkAllAssertionsForDirectory,
    checkValidIssues
)
from test.modelscripts import (
    getTestFile
)

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('test.'+__name__)

EXPECTED_ISSUES={
    'card1.use':        {F: 0, E: 1, W: 0, I: 0, H: 0},
    'card2.use':        {F: 0, E: 3, W: 0, I: 0, H: 0},
    'card3.use':        {F: 0, E: 0, W: 1, I: 0, H: 0},
    'empty.use':        {F: 0, E: 1, W: 1, I: 0, H: 0},
    'enum1.use':        {F: 0, E: 0, W: 1, I: 0, H: 0},
    'enum1.clm':        {F: 0, E: 0, W: 2, I: 0, H: 0},
    'enum2.use':        {F: 0, E: 1, W: 0, I: 0, H: 0},
    'inheritance1.use': {F: 0, E: 1, W: 0, I: 0, H: 0},
    'inheritance2.use': {F: 0, E: 1, W: 0, I: 0, H: 0},
    'nomodel.use':      {F: 0, E: 1, W: 1, I: 0, H: 0},
    #TODO:  ignored. why?'nofile.use':       {F: 1, E: 1, W: 1, I: 0, H: 0},
}


def testGenerator_Issues():
    res = checkAllAssertionsForDirectory(
        'use/issues/frozen',
        ['.use', '.clm'],
        EXPECTED_ISSUES)
    for (file , ex) in res:
        yield (checkValidIssues, file, classes.METAMODEL, ex)


def testNoFile():
    use_source=UseModelSource('nofile.use')
    ModelSourcePrinter(use_source).display()
    assertIssueBox(use_source.fullIssueBox,
                   {F: 2, E: 0, W: 1, I: 0, H: 0})
    assert use_source.hasIssues
    assert not use_source.isValid


import modelscripts.use.engine

def testBrokenUSEEngine():
    tmp_USE_OCL_COMMAND = \
        modelscripts.use.engine.USE_OCL_COMMAND
    try:
        print('Change to useabc to broken use engine')
        modelscripts.use.engine.USE_OCL_COMMAND = 'useabc'
        an_existing_file=getTestFile(
            'use/issues/frozen/card1.use')
        use_source = UseModelSource(an_existing_file)
        print('Model parsed.')
        ModelSourcePrinter(use_source).display()
        assertIssueBox(use_source.fullIssueBox,
                       {F: 0, E: 1, W: 0, I: 0, H: 0})
        assert use_source.hasIssues
        assert not use_source.isValid
    except:
        raise
    finally:
        modelscripts.use.engine.USE_OCL_COMMAND = \
            tmp_USE_OCL_COMMAND





