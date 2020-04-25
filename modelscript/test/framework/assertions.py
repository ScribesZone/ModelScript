# coding=utf-8
"""Assertions checking testcases against expected issues and metrics.

Issuebox can be tested with a set of pairs like
* (1) cl.syn.Association.AttRole 3
* (2) else *
* (3) level *

The first line checks that there a 3 issues for the given issue code.
The second line means that there can be any other issues.
The third line means that any issues of any levels can exist.

NOTE: the usage of "level" is not clear. This documentation should be
improved.

If not specified the "else" value is 0 meaning that no others issues
could exist. Otherwise the "else" value must be "*" meaning that some
other issues may exist.

The specification of expected issues/metrics can be either :

*   comment-based: expected results are embedded in testcases as comments.

*   code-based: expected results are represented as
    datastructures in the test drivers.

comment-based assertions
------------------------

Assertions are represented as comments in testcases as following :

    //@Issue cl.syn.Association.AttRole 1
    //@Issue else *

    //@Metric "class" 6
    //@Metric "plain class" 5
    //@Metric "association" 1

code-based assertions
---------------------

This package allows to check assertions against test case.
Tests can be written as following ::

    EXPECTED_ISSUES={
        'gl-mega01.gls':    {
            #'mgm.sem.Import.Allowed':1,
            E:2,
              level:'*',
              'else':0
        },
    }
    EXPECTED_METRICS={
        'myFile.gls': {
            'myIssueLabel' : 3
        }
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

"""

__all__=(
    "checkAllAssertionsForDirectory",
    "simpleTestDeneratorAssertions"
)

from typing_extensions import Literal
from typing import Text, Dict, Optional
import os
import re

from modelscript.base.issues import (
    IssueBox,
    Level,
    Levels,
)

from modelscript.test.framework import getTestFile, patternFromArgV, \
    getTestFiles
from modelscript.test.framework.output import ManageAndCompareOutput
from modelscript.megamodels import Megamodel


F=Levels.Fatal
E=Levels.Error
W=Levels.Warning
I=Levels.Info
H=Levels.Hint

ExpectedIssueDict=Optional[Dict[Level, int]]
ExpectedMetricDict=Optional[Dict[Level, int]]

from modelscript.megamodels.metamodels import Metamodel

def assertIssueBox(
        issueBox,
        expectedSummaryMap=None):
    #type: (IssueBox, ExpectedIssueDict) -> None
    """Assert that an issuebox match an expected map.
    A map is as following::
        {F: 0, E:1, 'mgm.sem.Import.Allowed':1 'else': 0},
        {F: 0, E:1, 'mgm.sem.Import.Allowed':2 'else': '*'},
    :param issueBox:
    :param expectedSummaryMap:
    """

    def printError(nbFound, label, nbExpected):
        print(
            'TST: ' + '####' + \
            ' ISSUE ASSERTION FAILED #### %i %s found. %i expected ' % (
                nbFound,
                label,
                nbExpected))

    def printActualSummaries():
        if issueBox.hasIssues:
            print('TST: ACTUAL ISSUE SUMMARY:')
            for code in issueBox.summaryCodeMap:
                print('    //@Issue %s %i' % (
                    code, issueBox.summaryCodeMap[code]))
            print('    //@Issue else *')
            print('')
            for level in issueBox.summaryLevelMap:
                print('    //@Issue %s %i' % (
                    level.code, issueBox.summaryLevelMap[level]))

    # if not specified the "else" value is 0
    # otherwise it must be "*"
    if 'else' in expectedSummaryMap:
        else_value=expectedSummaryMap['else']
        if else_value!='*':
            raise ValueError( #raise:OK
                'TST: In issue specification "else" parameter must be "*".'
                '%s found. Mapping is %s' %
                (else_value, expectedSummaryMap))
        del expectedSummaryMap['else']
    else:
        else_value=0

    if 'level' in expectedSummaryMap:
        lval=expectedSummaryMap['level']
        if lval!='*':
            raise ValueError(  #raise:OK
                'In metrics specification "level" parameter must be "*".'
                '%s found. Mapping is %s' %
                (lval, expectedSummaryMap))
        del expectedSummaryMap['level']
        ignore_unspecified_level=True
    else:
        ignore_unspecified_level=False


    levels_checked=[]


    unexpected=False
    if expectedSummaryMap is not None:
        actualLevelMap=issueBox.summaryLevelMap
        actualCodeMap=issueBox.summaryCodeMap
        for key in expectedSummaryMap:

            # check that what is expected is realized
            if isinstance(key, Level):
                levels_checked.append(key)
                # Check Level assertions
                if actualLevelMap[key] != expectedSummaryMap[key]:
                    printError(
                        actualLevelMap[key],
                        key.label,
                        expectedSummaryMap[key])
                    unexpected = True
            else:

                # Check code assertions
                if key not in actualCodeMap:
                    # expected code, no code at all
                    printError(
                        0,
                        key,
                        expectedSummaryMap[key])
                    unexpected = True
                else:
                    # expected code, check counts
                    if actualCodeMap[key] != expectedSummaryMap[key]:
                        printError(
                            actualCodeMap[key],
                            key,
                            expectedSummaryMap[key])
                        unexpected = True


        if else_value==0:
            # Check that what was not specified is 0
            if not ignore_unspecified_level:
                for level in Levels.Levels:
                    if level not in levels_checked:
                        if level in actualLevelMap:
                            if actualLevelMap[level] != 0:
                                printError(
                                    actualLevelMap[level],
                                    level.label,
                                    0)
                                unexpected = True
            # Produce an error for all actual code not expected
            for code in actualCodeMap:
                if code not in expectedSummaryMap:
                    printError(
                        actualCodeMap[code],
                        code,
                        0)
                    unexpected = True


        if unexpected:
            printActualSummaries()

        assert not unexpected, \
            'Unexpected number of issues. See above message for details'


def assertMetrics(
        metrics,
        expectedMetricsMap=None):
    """Assert that an set of metrics match an expected map.
    :param metrics: modelscript.base.metrics.Metrics
    :param expectedMetricsMap:
    :return:
    """


    def printError(nbFound, label, nbExpected):
        print(
            'TST: ' + '####' + \
            ' TEST FAILED #### %i %s found. %i expected ' % (
                nbFound,
                label,
                nbExpected))

    def printActualSummary():
        print('TST: ACTUAL METRICS:')
        for metric in metrics.all:
            print('    //@Metric "%s" %i' %(
                metric.label,
                metric.n
            ))


    unexpected=False
    if expectedMetricsMap is not None:
        for label in expectedMetricsMap:
            found=metrics.metricNamed[label].n
            expected=expectedMetricsMap[label]
            if found!=expected:
                printError(found, label, expected)
                unexpected=True

    printActualSummary()

    assert not unexpected, \
        'Unexpected metrics. Check message above for moore details'

RE_ISSUE_HEADER=r'^ *// *@ *Issue'
RE_ISSUE_LABEL=r'(?P<label>[\w.]+)'
RE_ISSUE_COUNT=r'(?P<count>([\d]+|\*))'
RE_ISSUE_SPEC='%s +%s +%s' % (
    RE_ISSUE_HEADER, RE_ISSUE_LABEL, RE_ISSUE_COUNT)

RE_METRIC_HEADER=r'^ *// *@ *Metric'
RE_METRIC_LABEL=r'"(?P<label>[^"]+)"'
RE_METRIC_COUNT=r'(?P<count>([\d]+|\*))'
RE_METRIC_SPEC='%s +%s +%s' % (
    RE_METRIC_HEADER, RE_METRIC_LABEL, RE_METRIC_COUNT)


def _extractExpectedIssuesMapFromFile(fileName):
    """Parse a source file and extract the issue specification.
    """

    def error(lineNo, message):
        text='%s:%i. Error: %s' % (fileName, lineNo, message)
        print('TST: '+text)
        raise SyntaxError( #raise:OK
            text)

    expectedIssuesMap={}
    with open(fileName) as f:
        lines = f.readlines()
    lines = [x.strip() for x in lines]
    for line_index, line in enumerate(lines):
        m=re.match(RE_ISSUE_HEADER, line)
        if m:
            m=re.match(RE_ISSUE_SPEC, line)
            if m:
                label=m.group('label')
                if m.group('count')!='*':
                    count=int(m.group('count'))
                else:
                    count='*'
                if label in expectedIssuesMap:
                    error(line_index+1, '%s defined again.'%label)
                else:
                    issueLevel=Levels.fromCode(label)
                    if issueLevel is not None:
                        expectedIssuesMap[issueLevel]=count
                    else:
                        expectedIssuesMap[label]=count
            else:
                error(line_index+1,'Pattern do not match')
    return expectedIssuesMap

def _extractExpectedMetricsMapFromFile(fileName):

    def error(lineNo, message):
        print('TST: %s:%i. Error: %s' % (fileName, lineNo, message))

    expectedMetricsMap={}
    with open(fileName) as f:
        lines = f.readlines()
    lines = [x.strip() for x in lines]
    for line_no, line in enumerate(lines):
        m=re.match(RE_METRIC_HEADER, line)
        if m:
            m=re.match(RE_METRIC_SPEC, line)
            if m:
                label=m.group('label')
                count=int(m.group('count'))
                if label in expectedMetricsMap:
                    error(line_no, '%s defined again.'%label)
                else:
                    expectedMetricsMap[label]=count
    return expectedMetricsMap

def checkAllAssertionsForDirectory(
        relTestcaseDir,
        extension,
        pattern='',
        expectedIssuesFileMap={},
        expectedMetricsFileMap={}):
    """
    Check assertions for all files in a given directory.
    If the expected map are given, search first in this
    map for assertion otherwise the assertion will be extracted
    from each file.
    This function is called by simpleTestDeneratorAssertions.
    :param relTestcaseDir: directory relative to testcases
    :param extension: the extension of the files to check
    :param pattern: a pattern to select files via re.search
    :param expectedIssuesFileMap: see examples in test files
    :param expectedMetricsFileMap: see examples in test files
    :return: a pair (file,issue map) for all file in directory
    """
    # For some reason this function is called twice
    # Does not matter too much.
    test_files=getTestFiles(
        relTestcaseDir,
        relative=True,
        extension=extension,
        pattern=pattern,
        )

    l=[]
    for test_file in test_files:
        basename = os.path.basename(test_file)
        if basename in expectedIssuesFileMap:
            # first look in the map provided as code
            issuemap=expectedIssuesFileMap[basename]
        else:
            full_filename=getTestFile(test_file)
            # extract issues map from file, could be None
            issuemap=_extractExpectedIssuesMapFromFile(full_filename)
        if basename in expectedMetricsFileMap:
            # first look in the map provided as code
            metricsmap = expectedMetricsFileMap[basename]
        else:
            full_filename = getTestFile(test_file)
            # extract issues map from file, could be None
            metricsmap = _extractExpectedMetricsMapFromFile(full_filename)
        l.append((test_file, issuemap, metricsmap))
    return l
#
# def checkAllAssertionsForDirectory(relTestcaseDir, extension, expectedIssuesMap):
#     """
#     :param relTestcaseDir: directory relative to testcases
#     :param extension: the extension of the files to check
#     :param expectedIssuesMap: see examples in test files
#     :return: a pair (file,issue map) for all file in directory
#     """
#     # For some reason this function is called twice
#     # Does not matter too much.
#     test_files=getTestFiles(
#         relTestcaseDir,
#         relative=True,
#         extension=extension)
#
#     l=[]
#     for test_file in test_files:
#         basename = os.path.basename(test_file)
#         expected_issues=(
#             None if basename not in expectedIssuesMap
#             else expectedIssuesMap[basename])
#         l.append((test_file, expected_issues))
#     return l

# def exractExpectedIssueMapFromFile(fileName):



def checkIssuesMetricsAndOutput(
        reltestfile: str,
        metamodel: Metamodel,
        expectedIssues: ExpectedIssueDict = None,
        expectedMetrics: ExpectedMetricDict = None)\
        -> None:
    """
    Check issues/metrics assertion for a given file.
    This function is called by the simpleTestDeneratorAssertions
    generator.

    Args:
        reltestfile: The relative location of the file to test.
            Something like "des/de-ko01.des"
        metamodel: The metamodel of the file.
        expectedIssues: The map of expected issues.
        expectedMetrics: The map of expected metric.
    """

    file_info = ' %s %s ' % (
        metamodel.label,
        os.path.basename(reltestfile)
    )
    print(reltestfile)
    print('\nTST:'+'=='*10+' testing '+file_info+'='*35+'\n' )
    # Create a model source file from the given file.
    # This do parsing and eventually creates the model
    source = metamodel.sourceClass(getTestFile(reltestfile))

    # Get access tp the model
    model = source.model

    print('\n'+'TST:'+'==' *10 + ' printing model '+'='*40+'\n')
    printer = metamodel.modelPrinterClass
    printer(source.model).display()

    actual_ouput = printer(source.model).string()
    ManageAndCompareOutput(
        reltestfile=reltestfile,
        actualOutput=actual_ouput)


    if expectedIssues is None:
        expectedIssues={F: 0, E: 0, W: 0, I: 0, H: 0}

    assertIssueBox(source.fullIssueBox, expectedIssues)
    assertMetrics(source.fullMetrics, expectedMetrics)

    print('\n'+'TST:'+'==' * 10 + ' printing source '+file_info+'='*35+'\n')
    metamodel.sourcePrinterClass(source).display()

    print('\n'+'TST:'+'==' *10 + ' printing metrics '+'='*40+'\n')
    print(source.fullMetrics)
    print('TST:'+'=='*10+' tested '+file_info+'='*35+'\n' )



# def scriptsIterator(m2id, expectedIssues):
#     metamodel=Megamodel.theMetamodel(id=m2id)
#     res = checkAllAssertionsForDirectory(
#         metamodel.extension[1:],
#         [metamodel.extension],
#         expectedIssues)

def simpleTestDeneratorAssertions(metamodel):
    """Check issues/metrics assertions for all testcases corresponding
    to a given metamodel.
    To be more precise this method returns a generator used for tests.
    The test generator can be used as following :

        from modelscript.test.framework.assertions import (
            simpleTestDeneratorAssertions)
        from modelscript.metamodels.aui import METAMODEL

        def testGenerator_Assertions():
            for (v,f,m,eim, emm) in \
                    simpleTestDeneratorAssertions(METAMODEL):
                yield (v,f,m,eim, emm)

    Args:
        metamodel: the metamodel of interest. The metamodel is used
            to select the testcase directory.
    """
    extension = metamodel.extension
    test_rel_dir = extension[1:]
    res = checkAllAssertionsForDirectory(
        relTestcaseDir=test_rel_dir,
        extension=[extension],
        pattern=patternFromArgV(),
        expectedIssuesFileMap={},
        expectedMetricsFileMap={})

    for (file , expected_issue_map, expected_metrics_map) in res:
        yield (
            checkIssuesMetricsAndOutput,
            file,
            metamodel,
            expected_issue_map,
            expected_metrics_map)
