# coding=utf-8
from __future__ import print_function

from modelscripts.metamodels import usecases
from modelscripts.scripts.megamodels.printer.megamodels import \
    MegamodelPrinter
from test.modelscripts.drivers.assertions import (
    checkAllAssertionsForDirectory,
    checkValidIssues,
)

EXPECTED_ISSUES={
}

def testGenerator_Assertions():
    res = checkAllAssertionsForDirectory(
        relTestcaseDir='uss',
        extension=['.uss'])

    for (file , expected_issue_map, expected_metrics_map) in res:
        yield (
            checkValidIssues,
            file,
            usecases.METAMODEL,
            expected_issue_map,
            expected_metrics_map)

# def testGenerator_Issues():
#     res = checkAllAssertionsForDirectory(
#         'uss',
#         ['.uss'],
#         EXPECTED_ISSUES)
#     for (file , ex) in res:
#         yield (checkValidIssues, file, usecases.METAMODEL, ex)

def testFinalMegamodel():
    MegamodelPrinter().display()