# coding=utf-8
from __future__ import print_function

from modelscribes.metamodels import (
    usecases
)

from test.modelscripts.issues import (
    F, E, W, I, H,
    checkFileIssues,
    checkValidIssues,
)

import modelscribes.scripts.parsers
import modelscribes.scripts.printers



EXPECTED_ISSUES={
    'uc1.uss': {F: 1, E: 0, W: 1, I: 0, H: 0},
    'uc3.uss': {F: 0, E: 0, W: 2, I: 0, H: 0},
    'uc4.uss': {F: 1, E: 0, W: 0, I: 0, H: 0},
    'uc9.uss': {F: 0, E: 0, W: 3, I: 0, H: 0},
}

def testGenerator_Issues():
    res = checkFileIssues(
        'uss',
        ['.uss'],
        EXPECTED_ISSUES)
    for (file , ex) in res:
        yield (checkValidIssues, file, usecases.METAMODEL, ex)

