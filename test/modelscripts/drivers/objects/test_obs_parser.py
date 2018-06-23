# coding=utf-8
from __future__ import print_function

from modelscripts.metamodels import (
    objects
)
from modelscripts.scripts.megamodels.printer.megamodels import \
    MegamodelPrinter
from test.modelscripts.drivers.assertions import (
    checkAllAssertionsForDirectory,
    checkValidIssues
)


def testGenerator_Assertions():
    res = checkAllAssertionsForDirectory(
        relTestcaseDir='obs',
        extension=['.obs'],
        expectedIssuesFileMap={},
        expectedMetricsFileMap={})

    for (file , expected_issue_map, expected_metrics_map) in res:
        yield (
            checkValidIssues,
            file,
            objects.METAMODEL,
            expected_issue_map,
            expected_metrics_map)

def testFinalMegamodel():
    MegamodelPrinter().display()