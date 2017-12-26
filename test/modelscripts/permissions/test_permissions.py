# coding=utf-8
from __future__ import print_function
from nose.plugins.attrib import attr

import modelscripts
from modelscripts.scripts.megamodels.printer.megamodels import MegamodelPrinter
from modelscripts.metamodels import (
    permissions
)
from test.modelscripts.issues import (
    F, E, W, I, H,
    checkFileIssues,
    checkValidIssues
)



EXPECTED_ISSUES={
    'a1.pes':        {F: 0, E: 0, W: 0, I: 0, H: 0},
    'a5.pes':        {F: 0, E: 0, W: 0, I: 0, H: 0},
    'a6.pes':        {F: 0, E: 0, W: 0, I: 0, H: 0},

    'a2.pes':        {F: 1, E: 0, W: 0, I: 0, H: 0},
    'a3.pes':        {F: 1, E: 0, W: 0, I: 0, H: 0},
    'a4.pes':        {F: 0, E: 1, W: 0, I: 0, H: 0},
    'a7.pes':        {F: 1, E: 0, W: 0, I: 0, H: 0},
    'a8.pes':        {F: 1, E: 0, W: 0, I: 0, H: 0},
    'a9.pes':        {F: 1, E: 3, W: 0, I: 0, H: 0},
    'a10.pes':       {F: 1, E: 3, W: 0, I: 0, H: 0},
    'a11.pes':       {F: 1, E: 3, W: 0, I: 0, H: 0},
}


def testGenerator_Issues():
    res = checkFileIssues(
        'pes',
        ['.pes'],
        EXPECTED_ISSUES)
    for (file , ex) in res:
        yield (checkValidIssues, file, permissions.METAMODEL,  ex)


def testFinalMegamodel():
    MegamodelPrinter().display()

