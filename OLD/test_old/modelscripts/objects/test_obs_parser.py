# coding=utf-8


from modelscripts.metamodels import (
    objects
)
from modelscripts.scripts.megamodels.printer.megamodels import \
    MegamodelPrinter
from test.modelscripts import (
    checkAllAssertionsForDirectory,
    checkValidIssues
)

EXPECTED_ISSUES={
    # 'us28.scs':         {F: 0, E: 0, W: 11, I: 0, H: 0},
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
    res = checkAllAssertionsForDirectory(
        'obs',
        ['.obs'],
        EXPECTED_ISSUES)
    for (file , ex) in res:
        yield (checkValidIssues, file, objects.METAMODEL,  ex)

def testFinalMegamodel():
    MegamodelPrinter().display()