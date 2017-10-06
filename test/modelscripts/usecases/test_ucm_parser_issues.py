# coding=utf-8
from __future__  import print_function
import logging
import modelscribes.scripts.classes.parser
import modelscribes.scripts.classes.printer
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('test.'+__name__)



from modelscribes.metamodels.classes import (
    METAMODEL
)

from test.modelscripts.issues import (
    F, E, W, I, H,
    checkFileIssues,
    checkValidIssues
)


EXPECTED_ISSUES={
    'uc1.ucm':        {F: 0, E: 1, W: 1, I: 0, H: 0},

    'uc3.ucm':        {F: 0, E: 2, W: 1, I: 0, H: 0},
    # check last error

    'uc9.ucm':        {F: 1, E: 0, W: 0, I: 0, H: 0},

}


def testGenerator_Issues():
    res = checkFileIssues(
        'ucm/issues/frozen',
        '.ucm',
        EXPECTED_ISSUES)
    for (file , ex) in res:
        yield (checkValidIssues, METAMODEL, file, ex)







