# coding=utf-8
from __future__  import print_function

from typing import Text, Dict, Optional
import os
import re

from modelscripts.base.issues import (
    IssueBox,
    Level,
    Levels,
)

from test.modelscripts.framework import getTestFile, patternFromArgV, \
    getTestFiles
from modelscripts.megamodels import Megamodel

#------------------------------------------------------------------------
# This package allows to check assertions against test case.
# The test can be written like that.

        # EXPECTED_ISSUES={
        #     # 'gl-mega01.gls':    {
        #     #     #'mgm.sem.Import.Allowed':1,
        #     #     E:2,
        #     #       level:'*',
        #     #       'else':0
        #     # },
        # }
        # EXPECTED_METRICS={
        #     #     'myFile.gls': {
        #     #         'myIssueLabel' : 3
        #     #     }
        # }
        #
        # def testGenerator_Assertions():
        #     res = checkAllAssertionsForDirectory(
        #         relTestcaseDir='gls',
        #         extension=['.gls'],
        #         expectedIssuesFileMap=EXPECTED_ISSUES,
        #         expectedMetricsFileMap=EXPECTED_METRICS)
        #
        #     for (file , expected_issue_map, expected_metrics_map) in res:
        #         yield (
        #             checkValidIssues,
        #             file,
        #             glossaries.METAMODEL,
        #             expected_issue_map,
        #             expected_metrics_map)


# If no assertions are provided in code then it is
# assertions can be written in directly in files.
#------------------------------------------------------------------------


F=Levels.Fatal
E=Levels.Error
W=Levels.Warning
I=Levels.Info
H=Levels.Hint

ExpectedIssueDict=Optional[Dict[Level, int]]
ExpectedMetricDict=Optional[Dict[Level, int]]

from modelscripts.megamodels.metamodels import Metamodel

def assertIssueBox(
        issueBox,
        expectedSummaryMap=None):
    #type: (IssueBox, ExpectedIssueDict) -> None

    # Assert that an issuebox match an expected map.
    #
    # A map is like this
    #
    # {F: 0, E:1, 'mgm.sem.Import.Allowed':1 'else': 0},
    # {F: 0, E:1, 'mgm.sem.Import.Allowed':2 'else': '*'},

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

        assert not unexpected, 'Unexpected number of issues'

def assertMetrics(
        metrics,
        expectedMetricsMap=None):


    # Assert that an issuebox match an expected map.
    #
    # A map is like this
    #
    # {F: 0, E:1, 'mgm.sem.Import.Allowed':1 'else': 0},
    # {F: 0, E:1, 'mgm.sem.Import.Allowed':2 'else': '*'},


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

    assert not unexpected, 'Unexpected metrics'

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

def extractExpectedIssuesMapFromFile(fileName):

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

def extractExpectedMetricsMapFromFile(fileName):

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
            issuemap=extractExpectedIssuesMapFromFile(full_filename)
        if basename in expectedMetricsFileMap:
            # first look in the map provided as code
            metricsmap = expectedMetricsFileMap[basename]
        else:
            full_filename = getTestFile(test_file)
            # extract issues map from file, could be None
            metricsmap = extractExpectedMetricsMapFromFile(full_filename)
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

# def extractExpectedIssueMapFromFile(fileName):



def checkValidIssues(
        reltestfile,
        metamodel,
        expectedIssues=None,
        expectedMetrics=None ):
    #type: (Text, Metamodel, ExpectedIssueDict, ExpectedMetricDict) -> None
    """
    :param reltestfile: the file to test
    :param metamodel: the metamodel of the file
    :param expectedIssues: the map of issue expected
    :param expectedMetrics: the map of metric expected
    :return:
    """
    file=' %s %s ' % (
        metamodel.label,
        os.path.basename(reltestfile)
    )
    print('\nTST:'+'=='*10+' testing '+file+'='*35+'\n' )
    source = metamodel.sourceClass(getTestFile(reltestfile))

    print('\n'+'TST:'+'==' * 10 + ' printing source '+file+'='*35+'\n')
    metamodel.sourcePrinterClass(source).display()

    print('\n'+'TST:'+'==' *10 + ' printing model '+'='*40+'\n')
    metamodel.modelPrinterClass(source.model).display()

    if expectedIssues is None:
        expectedIssues={F: 0, E: 0, W: 0, I: 0, H: 0}

    assertIssueBox(source.fullIssueBox, expectedIssues)
    assertMetrics(source.fullMetrics, expectedMetrics)

    print('\n'+'TST:'+'==' *10 + ' printing model '+'='*40+'\n')
    print(source.fullMetrics)
    print('TST:'+'=='*10+' tested '+file+'='*35+'\n' )



# def scriptsIterator(m2id, expectedIssues):
#     metamodel=Megamodel.theMetamodel(id=m2id)
#     res = checkAllAssertionsForDirectory(
#         metamodel.extension[1:],
#         [metamodel.extension],
#         expectedIssues)

def simpleTestDeneratorAssertions(metamodel):
    extension=metamodel.extension
    test_rel_dir=extension[1:]
    print('RR'*10, extension)
    res = checkAllAssertionsForDirectory(
        relTestcaseDir=test_rel_dir,
        extension=[extension],
        pattern=patternFromArgV(),
        expectedIssuesFileMap={},
        expectedMetricsFileMap={})

    for (file , expected_issue_map, expected_metrics_map) in res:
        yield (
            checkValidIssues,
            file,
            metamodel,
            expected_issue_map,
            expected_metrics_map)
