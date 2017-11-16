# coding=utf-8


import modelscribes.all
from modelscribes.scripts.megamodels.printer import (
    MegamodelPrinter
)
from modelscribes.metamodels import (
    classes
)
from test.modelscripts.issues import (
    F, E, W, I, H,
    checkFileIssues,
    checkValidIssues
)



EXPECTED_ISSUES={
    'ko-employee.cls':    {F: 0, E: 1, W: 0, I: 0, H: 0},
    # 'us90.scs':         {F: 0, E: 0, W: 9, I: 0, H: 0},
    # 'empty01.scs':      {F: 1, E: 0, W: 1, I: 0, H: 0},
    # 'empty02.scs':      {F: 1, E: 0, W: 1, I: 0, H: 0},
    # 'ko01.scs':         {F: 1, E: 0, W: 1, I: 0, H: 0},
    # 'ko02.scs':         {F: 1, E: 0, W: 1, I: 0, H: 0},
    # 'ko03.scs':         {F: 1, E: 0, W: 1, I: 0, H: 0},
    # 'ko04.scs':         {F: 1, E: 0, W: 1, I: 0, H: 0},
    # 'ko05.scs':         {F: 1, E: 0, W: 1, I: 0, H: 0},
    # 'ko06.scs':         {F: 1, E: 0, W: 1, I: 0, H: 0},
}


def testGenerator_Issues():
    res = checkFileIssues(
        'cls',
        ['.cls'],
        EXPECTED_ISSUES)
    for (file , ex) in res:
        yield (checkValidIssues, file, classes.METAMODEL,  ex)

def testFinalMegamodel():
    MegamodelPrinter().display()