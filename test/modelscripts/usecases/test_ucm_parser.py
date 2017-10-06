# coding=utf-8
from __future__ import print_function
import os
import logging

from test.modelscripts import TEST_CASES_DIRECTORY
from modelscribes.scripts.usecases.parser import UsecaseModelSource
from modelscribes.base.printers import (
    AnnotatedSourcePrinter
)
from modelscribes.scripts.megamodels.printer import (
    ImportBoxPrinter
)
# TODO: create a UsecaseSourcePrinter
# from modelscribes.scripts.usecases.printer import UsecaseSourcePrinter
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('test.' + __name__)

test_cases_dir = os.path.join(
    TEST_CASES_DIRECTORY,
    'ucm')

test_files = [
    os.path.join(test_cases_dir,f)
    for f in os.listdir(test_cases_dir)
    if f.endswith('.ucm')]

def testGenerator_AllSoilFile():
    for test in test_files:
        yield check_IsValid, test

def check_IsValid(testFile):
    ucs = UsecaseModelSource(testFile)
    print('='*40,os.path.basename(testFile),'='*40)
    ImportBoxPrinter(ucs.importBox).display()
    print('-'*90)
    AnnotatedSourcePrinter(ucs).display()
    # TODO: add printer
    # UsecaseSourcePrinter(ucs).display()
    assert ucs.isValid