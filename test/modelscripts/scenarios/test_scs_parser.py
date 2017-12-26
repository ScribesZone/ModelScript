# coding=utf-8


import modelscripts
from modelscripts.metamodels import (
    scenarios
)
from test.modelscripts.issues import (
    F, E, W, I, H,
    checkFileIssues,
    checkValidIssues
)
from modelscripts.scripts.megamodels.printer.megamodels import MegamodelPrinter

EXPECTED_ISSUES={
    'koquery01.scs':{F: 0, E: 2, W: 0, I: 0, H: 0},
    'us28.scs':         {F: 0, E: 0, W: 11, I: 0, H: 0},
    'us90.scs':         {F: 0, E: 0, W: 9, I: 0, H: 0},
    'empty01.scs':      {F: 1, E: 0, W: 1, I: 0, H: 0},
    'empty02.scs':      {F: 1, E: 0, W: 1, I: 0, H: 0},
    'ko01.scs':         {F: 1, E: 0, W: 1, I: 0, H: 0},
    'ko02.scs':         {F: 1, E: 0, W: 1, I: 0, H: 0},
    'ko03.scs':         {F: 1, E: 0, W: 1, I: 0, H: 0},
    'ko04.scs':         {F: 1, E: 0, W: 1, I: 0, H: 0},
    'ko05.scs':         {F: 1, E: 0, W: 1, I: 0, H: 0},
    'ko06.scs':         {F: 1, E: 0, W: 1, I: 0, H: 0},
}


def testGenerator_Issues():
    res = checkFileIssues(
        'scs/employee',
        ['.scs'],
        EXPECTED_ISSUES)
    for (file , ex) in res:
        if file.endswith('.scs'):
            yield (
                checkValidIssues,
                file,
                scenarios.METAMODEL,
                ex)

def testFinalMegamodel():
    MegamodelPrinter().display()