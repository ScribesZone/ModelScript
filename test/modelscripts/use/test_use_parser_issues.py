# coding=utf-8

from nose.plugins.attrib import attr
import logging
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('test.'+__name__)


import os
from modelscripts.use.use.parser import (
    UseSource
)
from modelscripts.use.use.printer import (
    UseSourcePrinter
)

from test.modelscripts import (
    getTestFiles,
    getTestFile
)


def testGenerator_UseOclModel_full():
    files=getTestFiles(
        'use/issues',
        relative=True,
        extension=['.use', '.clm'])
    for test_file in files:
        yield check_isInvalid, test_file


def check_isInvalid(reltestfile):
    use_source = UseSource(getTestFile(reltestfile))
    assert not use_source.isValid
    UseSourcePrinter(use_source).display()


