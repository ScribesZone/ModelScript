# coding=utf-8

from nose.plugins.attrib import attr
import logging
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('test.'+__name__)


import os
from modelscribes.use.use.parser import (
    UseSource
)
from modelscribes.use.use.printer import (
    UseSourcePrinter
)

from test.modelscripts import (
    getTestFiles,
    getTestFile,
    assertIssueBox,
    F,
    E,
    W,
    I,
    H,
)



EXPECTED_ISSUES={
    'card1.use':        {F: 0, E: 1, W: 0, I: 0, H: 0},
    'card2.use':        {F: 0, E: 3, W: 0, I: 0, H: 0},
    'card3.use':        {F: 0, E: 0, W: 1, I: 0, H: 0},
    'empty.use':        {F: 0, E: 1, W: 0, I: 0, H: 0},
    'enum1.use':        {F: 0, E: 0, W: 2, I: 0, H: 0},
    'enum2.use':        {F: 0, E: 1, W: 0, I: 0, H: 0},
    'inheritance1.use': {F: 0, E: 1, W: 0, I: 0, H: 0},
    'inheritance2.use': {F: 0, E: 1, W: 0, I: 0, H: 0},
    'nomodel.use':      {F: 0, E: 1, W: 0, I: 0, H: 0},

}

def testGenerator_UseOclModel_full():
    files=getTestFiles(
        'use/issues/frozen',
        relative=True,
        extension=['.use', '.clm'])

    for test_file in files:
        basename = os.path.basename(test_file)
        expected_issues=(
            None if basename not in EXPECTED_ISSUES
            else EXPECTED_ISSUES[basename])
        yield (
            check_isInvalid,
            test_file,
            expected_issues )

def check_isInvalid(reltestfile, expectedIssues):
    use_source = UseSource(getTestFile(reltestfile))
    UseSourcePrinter(use_source).display()
    if expectedIssues is not None:
        assertIssueBox(use_source.fullIssueBox, expectedIssues)
    assert use_source.hasIssues

def testNoFile():
    use_source=UseSource('nofile.use')
    UseSourcePrinter(use_source).display()
    assertIssueBox(use_source.fullIssueBox, {F: 1, E: 0, W: 0, I: 0, H: 0})
    assert use_source.hasIssues
    assert not use_source.isValid

import modelscribes.use.engine

def testBrokenUSEEngine():
    tmp_USE_OCL_COMMAND = modelscribes.use.engine.USE_OCL_COMMAND
    try:
        modelscribes.use.engine.USE_OCL_COMMAND = 'useabc'
        an_existing_file=getTestFile('use/issues/frozen/card1.use')

        use_source = UseSource(an_existing_file)
        UseSourcePrinter(use_source).display()
        assertIssueBox(use_source.fullIssueBox, {F: 0, E: 1, W: 0, I: 0, H: 0})
        assert use_source.hasIssues
        assert not use_source.isValid
    except:
        raise
    finally:
        modelscribes.use.engine.USE_OCL_COMMAND = tmp_USE_OCL_COMMAND





