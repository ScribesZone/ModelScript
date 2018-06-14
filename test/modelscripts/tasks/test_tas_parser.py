# coding=utf-8
from __future__ import print_function

import modelscripts
from modelscripts.metamodels import tasks
from modelscripts.scripts.megamodels.printer.megamodels import MegamodelPrinter

from test.modelscripts.assertions import (
    checkAllAssertionsForDirectory,
    checkValidIssues,
)


def testGenerator_Assertions():
    res = checkAllAssertionsForDirectory(
        relTestcaseDir='tas',
        extension=['.tas'])

    for (file , expected_issue_map, expected_metrics_map) in res:
        yield (
            checkValidIssues,
            file,
            tasks.METAMODEL,
            expected_issue_map,
            expected_metrics_map)

def testFinalMegamodel():
    MegamodelPrinter().display()