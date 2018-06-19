# coding=utf-8
from __future__ import print_function

from modelscripts.metamodels import (
    glossaries
)
from modelscripts.scripts.megamodels.printer.megamodels import \
    MegamodelPrinter
from test.modelscripts import (
    checkAllAssertionsForDirectory,
    checkValidIssues
)

# EXPECTED_ISSUES={
#     'err1.gls':         {F: 0, E: 0, W: 1, I: 0, H: 0},
#     'err2.gls':         {F: 0, E: 1, W: 1, I: 0, H: 0},
#     'err3.gls':         {F: 0, E: 1, W: 0, I: 0, H: 0},
#     'err4.gls':         {F: 0, E: 2, W: 0, I: 0, H: 0},
#     'err5.gls':         {F: 0, E: 1, W: 0, I: 0, H: 0},
#     'err6.gls':         {F: 0, E: 1, W: 0, I: 0, H: 0},
# }

EXPECTED_ISSUES={
    # 'gl-mega01.gls':    {
    #     #'mgm.sem.Import.Allowed':1,
    #     E:2,
    #     'else':0
    # },
    # 'err2.gls':         {F: 0, E: 1, W: 1, I: 0, H: 0},
    # 'err3.gls':         {F: 0, E: 1, W: 0, I: 0, H: 0},
    # 'err4.gls':         {F: 0, E: 2, W: 0, I: 0, H: 0},
    # 'err5.gls':         {F: 0, E: 1, W: 0, I: 0, H: 0},
    # 'err6.gls':         {F: 0, E: 1, W: 0, I: 0, H: 0},
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