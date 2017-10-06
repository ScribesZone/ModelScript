# coding=utf-8
from __future__  import print_function
import logging
import modelscribes.scripts.classes.parser
import modelscribes.scripts.classes.printer
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('test.'+__name__)


from modelscribes.use.use.parser import (
    UseModelSource
)
from modelscribes.use.use.printer import (
    UseSourcePrinter
)

from modelscribes.metamodels.classes import (
    METAMODEL
)

from test.modelscripts import (
    getTestFile
)

from test.modelscripts.issues import (
    assertIssueBox,
    F, E, W, I, H,
    checkFileIssues,
    checkValidIssues
)


EXPECTED_ISSUES={
    'card1.use':        {F: 0, E: 1, W: 0, I: 0, H: 0},
    'card2.use':        {F: 0, E: 3, W: 0, I: 0, H: 0},
    'card3.use':        {F: 0, E: 0, W: 1, I: 0, H: 0},
    'empty.use':        {F: 0, E: 1, W: 1, I: 0, H: 0},
    # 'enum1.use':        {F: 0, E: 0, W: 0, I: 0, H: 0},
    'enum1.clm':        {F: 0, E: 0, W: 2, I: 0, H: 0},
    'enum2.use':        {F: 0, E: 1, W: 0, I: 0, H: 0},
    'inheritance1.use': {F: 0, E: 1, W: 0, I: 0, H: 0},
    'inheritance2.use': {F: 0, E: 1, W: 0, I: 0, H: 0},
    'nomodel.use':      {F: 0, E: 1, W: 1, I: 0, H: 0},
    #TODO:  ignored. why?'nofile.use':       {F: 1, E: 1, W: 1, I: 0, H: 0},
}


def testGenerator_Issues():
    res = checkFileIssues(
        'use/issues/frozen',
        ['.use', '.clm'],
        EXPECTED_ISSUES)
    for (file , ex) in res:
        yield (checkValidIssues, METAMODEL, file, ex)




# def testGenerator_UseOclModel_full():
#     files=getTestFiles(
#         'use/issues/frozen',
#         relative=True,
#         extension=['.use', '.clm'])
#
#     for test_file in files:
#         basename = os.path.basename(test_file)
#         expected_issues=(
#             None if basename not in EXPECTED_ISSUES
#             else EXPECTED_ISSUES[basename])
#         yield (
#             check_isInvalid,
#             test_file,
#             expected_issues )



def testNoFile():
    use_source=UseModelSource('nofile.use')
    UseSourcePrinter(use_source).display()
    assertIssueBox(use_source.fullIssueBox, {F: 1, E: 1, W: 1, I: 0, H: 0})
    assert use_source.hasIssues
    assert not use_source.isValid





import modelscribes.use.engine

def testBrokenUSEEngine():
    tmp_USE_OCL_COMMAND = modelscribes.use.engine.USE_OCL_COMMAND
    try:
        print('Change to useabc to broken use engine')
        modelscribes.use.engine.USE_OCL_COMMAND = 'useabc'
        an_existing_file=getTestFile('use/issues/frozen/card1.use')
        use_source = UseModelSource(an_existing_file)
        print('Model parsed.')
        UseSourcePrinter(use_source).display()
        assertIssueBox(use_source.fullIssueBox, {F: 0, E: 1, W: 0, I: 0, H: 0})
        assert use_source.hasIssues
        assert not use_source.isValid
    except:
        raise
    finally:
        modelscribes.use.engine.USE_OCL_COMMAND = tmp_USE_OCL_COMMAND





