# coding=utf-8
from __future__ import print_function
from nose.plugins.attrib import attr

import modelscribes
from modelscribes.scripts.megamodels.printer.megamodels import MegamodelPrinter
from modelscribes.metamodels import (
    glossaries
)
from test.modelscripts.issues import (
    F, E, W, I, H,
    checkFileIssues,
    checkValidIssues
)



EXPECTED_ISSUES={
    'err1.gls':         {F: 0, E: 0, W: 1, I: 0, H: 0},
    'err2.gls':         {F: 0, E: 1, W: 1, I: 0, H: 0},
    'err3.gls':         {F: 0, E: 1, W: 0, I: 0, H: 0},
    'err4.gls':         {F: 0, E: 2, W: 0, I: 0, H: 0},
    'err5.gls':         {F: 0, E: 1, W: 0, I: 0, H: 0},
    'err6.gls':         {F: 0, E: 1, W: 0, I: 0, H: 0},
}


def testGenerator_Issues():
    res = checkFileIssues(
        'gls',
        ['.gls'],
        EXPECTED_ISSUES)
    for (file , ex) in res:
        yield (checkValidIssues, file, glossaries.METAMODEL,  ex)

def testFinalMegamodel():
    MegamodelPrinter().display()