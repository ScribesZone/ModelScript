# coding=utf-8
import os
import contextlib

import modelscript
from modelscript.scripts.megamodels.printer.megamodels import (
    MegamodelPrinter)
from modelscript.interfaces.modelc.execution import (
    ExecutionContext)

from modelscript.test.framework import TEST_CASES_DIRECTORY


# def f(lang, file):
#     return os.path.join(
#         TEST_CASES_DIRECTORY, lang, file)

# see https://stackoverflow.com/questions/6194499/pushd-through-os-system
@contextlib.contextmanager
def pushDirectory(new_dir):
    previous_dir = os.getcwd()
    os.chdir(new_dir)
    yield
    os.chdir(previous_dir)

class T(object):

    def __init__(self, cmd, issueNb, sourceList):
        self.cmd = cmd
        # arguments of the command separated by spaces

        self.issueNb = issueNb
        # expected nb of issues

        self.sourceListStr = sourceList

        self.executionContext = None
        # set by check

    @property
    def args(self):
        return self.cmd.split()

    def sourceFileList(self):
        return self.sourceListStr.split()

    def checkIssues(self):
        if self.executionContext.nbIssues != self.issueNb:
            print('Nb of issues differs:')
            print(('Found:    %s' % self.executionContext.nbIssues))
            print(('Expected: %s' % self.issueNb))
            assert False

    def checkSourceList(self):
        basenames=[
            f.basename
            for f in self.executionContext.allSourceFileList ]
        if basenames != self.sourceFileList() :
            print('Source list differs :')
            print(('Found:    %s' % basenames))
            print(('Expected: %s' % self.sourceFileList()))
            assert False

    def check(self, executionContext):
        self.executionContext = executionContext
        self.checkSourceList()
        self.checkIssues()


TEST_CASES=[
    T('nothing', 1, ''),

    T('imports/wrong.ext', 1, ''),


    T('imports/imp-0-ko01.cls', 1, 'imp-0-ko01.cls'),
    T('imports/imp-0-ko02.cls', 1, 'imp-0-ko02.cls'),
    T('imports/imp-0-ko03.cls', 1, 'imp-0-ko03.cls'),

    T('imports/imp-0-circular01.gls', 1,
      'imp-0-circular01.gls'),

    T('imports/imp-1-ok01.cls', 0,
            'imp-1-ok01.gls imp-1-ok01.cls'),
    T('imports/imp-1-ok01.cls imports/imp-1-ok01.cls', 0,
            'imp-1-ok01.gls imp-1-ok01.cls'),
    T('imports/imp-1-ok01.gls imports/imp-1-ok01.cls', 0,
            'imp-1-ok01.gls imp-1-ok01.cls'),
    T('imports/imp-1-ok01.cls imports/imp-1-ok01.gls', 0,
            'imp-1-ok01.gls imp-1-ok01.cls'),

    T('imports/imp-1-type01.gls', 1, 'imp-1-type01.gls'),

    T('imports/imp-1-type02.cls', 1, 'imp-1-type02.cls'),

    T('imports/imp-1-twice01.cls', 0, 'empty.gls imp-1-twice01.cls'),

    T('imports/imp-1-okko02.cls', 2,
      'imp-1-okko02.gls imp-1-okko02.cls'),
    T('imports/imp-1-okko02.gls imports/imp-1-okko02.cls', 2,
      'imp-1-okko02.gls imp-1-okko02.cls'),
    T('imports/imp-1-okko02.cls imports/imp-1-okko02.gls', 2,
      'imp-1-okko02.gls imp-1-okko02.cls'),

    T('imports/imp-1-koko02.cls', 1,
      'imp-1-koko02.cls'),
    T('imports/imp-1-koko02.gls imports/imp-1-koko02.cls', 2,
      'imp-1-koko02.gls imp-1-koko02.cls'),

    T('imports/imp-2-ok01.obs', 0,
      'imp-2-ok01.gls imp-2-ok01.cls imp-2-ok01.obs'),
    T('imports/imp-2-ok01.obs imports/imp-2-ok01.cls', 0,
      'imp-2-ok01.gls imp-2-ok01.cls imp-2-ok01.obs'),
    T('imports/imp-2-ok01.obs imports/imp-2-ok01.cls imports/imp-2-ok01.obs ', 0,
      'imp-2-ok01.gls imp-2-ok01.cls imp-2-ok01.obs'),

    T('imports/imp-2-ok02.obs', 0,
      'imp-2-ok02.gls imp-2-ok02.cls imp-2-ok02.obs'),

    # TODO: restore this testcase
    # T('imports/imp-2-oksep01.obs', 666,
    #   'imp-2-oksep01.gls imp-2-oksep01.cls imp-2-oksep01bis.gls imp-2-oksep01.obs'),

    T('imports/imp-3-ok01.scs', 0,
      'imp-3-ok01.gls imp-3-ok01.cls imp-3-ok01.obs imp-3-ok01.scs'),

    T('imports/imp-3-ok02.scs', 0,
      'imp-3-ok02.gls imp-3-ok02.cls imp-3-ok02.obs imp-3-ok02.scs'),

    T('imports/imp-3-okokokko02.scs', 4,
      'imp-3-okokokko02.gls imp-3-okokokko02.cls imp-3-okokokko02.obs imp-3-okokokko02.scs'),

]

"""
imports/imp-1-koko02.cls
imports/imp-1-okko02.cls


uss/us-import03.uss blavla uss/us-import04.uss badext.ext -i
uss/us-import01.uss
uss/us-import04.uss uss/badglossary.gls -i

misc/nometamodel.xxx
a
uss/us-actor02.uss -i
uss/us-actor05.uss a -i
uss/us-actor02.uss b -i
c
"""

def test_modelc():
    for testcase in TEST_CASES:
        yield doModelc, testcase.cmd, testcase

def doModelc(cmd, testCase):
    # reload(modelscript)
    # the cmd arg

    # enter the testcases directory and perform the test
    with pushDirectory(TEST_CASES_DIRECTORY):
        title = ' modelc %s ' % cmd
        print(('='*80))
        print(('='*80))
        if len(title)<=60:
            print((title.center(80, '=')))
        for arg in testCase.args:
            print(('##  %s' % arg))
        print(('='*80))
        print(('='*80))
        print('')
        bc = ExecutionContext(testCase.args)
        bc.display()
        testCase.check(bc)
        from modelscript.megamodels import Megamodel
        m = Megamodel.model
        print(('\n'*4))


def testFinalMegamodel():
    MegamodelPrinter().display()
