# coding=utf-8
from __future__  import print_function

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

F=Levels.Fatal
E=Levels.Error
W=Levels.Warning
I=Levels.Info
H=Levels.Hint

ExpectedIssueDict=Optional[Dict[Level, int]]

from modelscribes.megamodels.metamodels import Metamodel

def assertIssueBox(issueBox, expected=None):
    #type: (IssueBox, ExpectedIssueDict) -> None
    if expected is not None:
        actual=issueBox.summaryMap
        for level in expected:
            assert actual[level] == expected[level], (
                '%i %s found. %i expected' % (
                    actual[level],
                    level.label,
                    expected[level]
                )
            )

def checkValidIssues(metamodel, reltestfile, expectedIssues):
    #type: (Metamodel, Text, ExpectedIssueDict) -> None
    print('='*40, os.path.basename(reltestfile), '='*40)
    source = metamodel.sourceClass(getTestFile(reltestfile))
    metamodel.sourcePrinterClass(source).display()
    if expectedIssues is not None:
        assertIssueBox(source.fullIssueBox, expectedIssues)
        assert source.hasIssues


def checkFileIssues(relDir, extension, expectedIssues):
    # For some reason this function is called twice
    # Does not matter
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