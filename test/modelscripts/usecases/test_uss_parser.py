# coding=utf-8
from __future__ import print_function

import modelscripts
from modelscripts.metamodels import usecases
from modelscripts.scripts.megamodels.printer.megamodels import MegamodelPrinter

from test.modelscripts.assertions import (
    F, E, W, I, H,
    checkAllAssertionsForDirectory,
    checkValidIssues,
)



EXPECTED_ISSUES={
    # 'us-doc01.uss':     {F: 0, E: 0, W: 3, I: 0, H: 0},
    # 'us-doc02.uss':     {F: 0, E: 0, W: 3, I: 0, H: 0},
    # 'us-doc03.uss':     {F: 0, E: 0, W: 4, I: 0, H: 0},
    # 'us-actor02.uss':   {F: 0, E: 0, W: 4, I: 0, H: 0},
    # 'us-actor03.uss':   {F: 0, E: 0, W: 5, I: 0, H: 0},
    # 'us-actor04.uss':   {F: 0, E: 0, W: 6, I: 0, H: 0},
    # 'us-interactions01.uss':   {F: 0, E: 0, W: 2, I: 0, H: 0},
    # 'us-interactions02.uss':   {F: 0, E: 0, W: 1, I: 0, H: 0},
    # 'us-interactions03.uss':   {F: 0, E: 0, W: 3, I: 0, H: 0},
    # 'us-interactions04.uss':   {F: 0, E: 0, W: 1, I: 0, H: 0},
    # 'us-ko-actors01.uss':   {F: 0, E: 1, W: 4, I: 0, H: 0},
    # 'us-ko-actors02.uss':   {F: 0, E: 1, W: 4, I: 0, H: 0},
    # 'us-ko-usecase01.uss':   {F: 0, E: 1, W: 5, I: 0, H: 0},
    # 'us-usecase01.uss':   {F: 0, E: 0, W: 5, I: 0, H: 0},
    # 'us-comment01.uss': {F: 0, E: 0, W: 4, I: 0, H: 0},
    # 'us-model01.uss': {F: 0, E: 0, W: 3, I: 0, H: 0},

    # 'a.uss':   {F: 0, E: 0, W: 1, I: 0, H: 0},
    # 'us1.uss': {F: 1, E: 0, W: 1, I: 0, H: 0},
    # 'us2.uss': {F: 0, E: 0, W: 2, I: 0, H: 0},
    # 'us3.uss': {F: 0, E: 0, W: 4, I: 0, H: 0},
    # 'us4.uss': {F: 1, E: 0, W: 0, I: 0, H: 0},
    # 'us5.uss': {F: 0, E: 0, W: 3, I: 0, H: 0},
    # 'us8.uss': {F: 0, E: 0, W: 4, I: 0, H: 0},
    # 'us9.uss': {F: 0, E: 0, W: 8, I: 0, H: 0},
    # 'us10.uss': {F: 0, E: 0, W: 5, I: 0, H: 0},
    # 'us20.uss': {F: 0, E: 0, W: 2, I: 0, H: 0},
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