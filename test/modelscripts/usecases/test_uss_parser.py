# coding=utf-8
from __future__ import print_function

import modelscripts
from modelscripts.metamodels import usecases
from modelscripts.scripts.megamodels.printer.megamodels import MegamodelPrinter

from test.modelscripts.issues import (
    F, E, W, I, H,
    checkFileIssues,
    checkValidIssues,
)



EXPECTED_ISSUES={
    'us1.uss': {F: 1, E: 0, W: 1, I: 0, H: 0},
    'us2.uss': {F: 0, E: 0, W: 1, I: 0, H: 0},
    'us3.uss': {F: 0, E: 0, W: 3, I: 0, H: 0},
    'us4.uss': {F: 1, E: 0, W: 0, I: 0, H: 0},
    'us5.uss': {F: 0, E: 0, W: 3, I: 0, H: 0},
    'us8.uss': {F: 0, E: 0, W: 1, I: 0, H: 0},
    'us9.uss': {F: 0, E: 0, W: 7, I: 0, H: 0},
    'us10.uss': {F: 0, E: 0, W: 4, I: 0, H: 0},
    'us20.uss': {F: 0, E: 0, W: 2, I: 0, H: 0},
}

def testGenerator_Issues():
    res = checkFileIssues(
        'uss',
        ['.uss'],
        EXPECTED_ISSUES)
    for (file , ex) in res:
        yield (checkValidIssues, file, usecases.METAMODEL, ex)

def testFinalMegamodel():
    MegamodelPrinter().display()