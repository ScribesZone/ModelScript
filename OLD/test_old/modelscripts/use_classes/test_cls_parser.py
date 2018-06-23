# coding=utf-8


from modelscripts.metamodels import (
    classes
)
from modelscripts.scripts.megamodels.printer.megamodels import \
    MegamodelPrinter
from test.modelscripts import (
    F, E, W, I, H,
    checkAllAssertionsForDirectory,
    checkValidIssues
)

EXPECTED_ISSUES={
    'ko-employee.cls':      {F: 0, E: 1, W: 0, I: 0, H: 0},
    'enum1KO.cls':          {F: 0, E: 0, W: 2, I: 0, H: 0}

}


def testGenerator_Issues():
    res = checkAllAssertionsForDirectory(
        'cls',
        ['.cls'],
        EXPECTED_ISSUES)
    for (file , ex) in res:
        yield (checkValidIssues, file, classes.METAMODEL,  ex)

def testFinalMegamodel():
    MegamodelPrinter().display()