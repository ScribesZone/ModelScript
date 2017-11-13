# coding=utf-8
from __future__  import print_function
import modelscribes.metamodels
import modelscribes.scripts

from typing import Text, Dict, Optional
import os

from modelscribes.base.issues import (
    IssueBox,
    Level,
    Levels,
)

from test.modelscripts import (
    getTestFiles,
    getTestFile
)
from modelscribes.megamodels.megamodels import Megamodel

F=Levels.Fatal
E=Levels.Error
W=Levels.Warning
I=Levels.Info
H=Levels.Hint

ExpectedIssueDict=Optional[Dict[Level, int]]

from modelscribes.megamodels.metamodels import Metamodel

def assertIssueBox(issueBox, expected=None):
    #type: (IssueBox, ExpectedIssueDict) -> None
    unexpected=False
    if expected is not None:
        actual=issueBox.summaryMap
        for level in expected:
            if actual[level] != expected[level]:
                print(
                    '##'*6+ \
                    ' TEST FAILED ##### %i %s found. %i expected ' % (
                    actual[level],
                    level.label,
                    expected[level]
                ))
                unexpected = True
        assert not unexpected, 'Unexpected number of issues'



def checkFileIssues(relDir, extension, expectedIssues):
    # For some reason this function is called twice
    # Does not matter too much.
    test_files=getTestFiles(
        relDir,
        relative=True,
        extension=extension)

    l=[]
    for test_file in test_files:
        basename = os.path.basename(test_file)
        expected_issues=(
            None if basename not in expectedIssues
            else expectedIssues[basename])
        l.append((test_file, expected_issues))
    return l

def checkValidIssues(reltestfile, metamodel, expectedIssues):
    #type: (Text, Metamodel, ExpectedIssueDict) -> None
    file=' %s %s ' % (
        metamodel.label,
        os.path.basename(reltestfile)
    )
    print('\nte:'+'=='*10+' testing '+file+'='*35+'\n' )
    source = metamodel.sourceClass(getTestFile(reltestfile))
    print('\n'+'--' * 10 + ' printing source '+file+'-'*35+'\n')
    metamodel.sourcePrinterClass(source).display()
    if expectedIssues is None:
        expectedIssues={F: 0, E: 0, W: 0, I: 0, H: 0}
    assertIssueBox(source.fullIssueBox, expectedIssues)
    print('te:'+'=='*10+' tested '+file+'='*35+'\n' )

def scriptsIterator(m2id, expectedIssues):
    metamodel=Megamodel.metamodel(id=m2id)
    res = checkFileIssues(
        metamodel.extension[1:],
        [metamodel.extension],
        expectedIssues)
