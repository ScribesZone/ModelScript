# coding=utf-8
from __future__ import print_function
from nose.plugins.attrib import attr

import modelscripts
from modelscripts.scripts.megamodels.printer.megamodels import MegamodelPrinter
from modelscripts.metamodels import (
    glossaries
)
from test.modelscripts.assertions import (
    F, E, W, I, H,
    checkAllAssertionsForDirectory,
    checkValidIssues
)




EXPECTED_ISSUES={
    # 'gl-mega01.gls':    {
    #     #'mgm.sem.Import.Allowed':1,
    #     E:2,
    #       level:'*',
    #       'else':0
    # },
}
EXPECTED_METRICS={
    #     'myFile.gls': {
    #         'myIssueLabel' : 3
    #     }
}

def testGenerator_Assertions():
    res = checkAllAssertionsForDirectory(
        relTestcaseDir='gls',
        extension=['.gls'],
        expectedIssuesFileMap=EXPECTED_ISSUES,
        expectedMetricsFileMap=EXPECTED_METRICS)

    for (file , expected_issue_map, expected_metrics_map) in res:
        yield (
            checkValidIssues,
            file,
            glossaries.METAMODEL,
            expected_issue_map,
            expected_metrics_map)

def testFinalMegamodel():
    MegamodelPrinter().display()