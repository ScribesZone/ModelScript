# coding=utf-8


import modelscribes.all
from modelscribes.scripts.megamodels.printer.megamodels import MegamodelPrinter
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