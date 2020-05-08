# coding=utf-8
"""Assertions checking testcases against issues, metrics and content.
This module allows to compare the result of a test <ith
* issues expected,
* metrics expected,
* output expected.

The expected issues and metrics can be specified as special comments
in the source file. Expected output can be specified as a file in
a "output-generated" and "output-verified" directories. See the
modules issues, metrics, and output for more detail.

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

                Issuebox can be tested with a set of pairs like

"""

__all__=(
    "checkAllAssertionsForDirectory",
    "simpleTestDeneratorAssertions"
)

from typing import Dict, Optional
import os
import re

from modelscript.base.styles import (
    Style,
    Styles)

from modelscript.base.issues import (
    Level,
    Levels)

from modelscript.test.framework import (
    getTestFile,
    patternFromArgV,
    getTestFiles)
from modelscript.test.framework.issues import (
    assertIssueBox,
    extractExpectedIssuesMapFromFile)
from modelscript.test.framework.metrics import (
    assertMetrics,
    extractExpectedMetricsMapFromFile)
from modelscript.test.framework.output import manageAndAssertOutput
from modelscript.megamodels.metamodels import Metamodel
from modelscript.base.modelprinters import ModelPrinterConfig


def checkAllAssertionsForDirectory(
        relTestcaseDir: str,
        extension,
        pattern: str = '',
        expectedIssuesFileMap={},
        expectedMetricsFileMap={}):
    """Check assertions for all files in a given directory.
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
    test_files = getTestFiles(
        relTestcaseDir,
        relative=True,
        extension=extension,
        pattern=pattern,
        )

    l = []
    for test_file in test_files:
        basename = os.path.basename(test_file)
        if basename in expectedIssuesFileMap:
            # first look in the map provided as code
            issue_map = expectedIssuesFileMap[basename]
        else:
            full_filename = getTestFile(test_file)
            # extract issues map from file, could be None
            issue_map = extractExpectedIssuesMapFromFile(full_filename)
        if basename in expectedMetricsFileMap:
            # first look in the map provided as code
            metrics_map = expectedMetricsFileMap[basename]
        else:
            full_filename = getTestFile(test_file)
            # extract issues map from file, could be None
            metrics_map = extractExpectedMetricsMapFromFile(full_filename)
        l.append((test_file, issue_map, metrics_map))
    return l


ExpectedIssueDict = Optional[Dict[Level, int]]
ExpectedMetricDict = Optional[Dict[Level, int]]


def checkIssuesMetricsAndOutput(
        reltestfile: str,
        metamodel: Metamodel,
        expectedIssues: ExpectedIssueDict = None,
        expectedMetrics: ExpectedMetricDict = None)\
        -> None:
    """Check issues/metrics/content assertions for a given test file.
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
    print('\nTST:'+'=='*10 + ' testing '+file_info+'='*35+'\n' )

    # ---- Create the model
    # Create the model source file from the given file.
    # This do parsing and eventually creates the model
    source = metamodel.sourceClass(getTestFile(reltestfile))

    # ---- Get access tp the model
    model = source.model

    # ---- print the model
    print('\n'*2)
    print(Styles.blue.do('TST: printing model'))
    print(Styles.blue.do('TST:'+'##'*50+'\n'))
    printer = metamodel.modelPrinterClass
    styled_config = ModelPrinterConfig(styled=True)
    printer(source.model, config=styled_config).display()
    print(Styles.blue.do('TST:'+'##'*50+'\n'))

    # ---- deal with output assertion
    actual_output = printer(source.model).string()
    manageAndAssertOutput(
        reltestfile=reltestfile,
        stream='output',
        actualOutput=actual_output)

    # ---- deal with issue assertions
    if expectedIssues is None:
        expectedIssues={F: 0, E: 0, W: 0, I: 0, H: 0}
    assertIssueBox(source.fullIssueBox, expectedIssues)

    # ---- deal with metrics assertions
    assertMetrics(source.fullMetrics, expectedMetrics)

    # print('\n'+'TST:'+'==' * 10 + ' printing source '+file_info+'='*35+'\n')
    # metamodel.sourcePrinterClass(source).display()

    # ---- print metrics
    if False:
        print('\n'+'TST:'+'==' *10 + ' printing metrics '+'='*40+'\n')
        print(source.fullMetrics)
        print('TST:'+'=='*10+' tested '+file_info+'='*35+'\n' )


def simpleTestDeneratorAssertions(metamodel):
    """Check issues/metrics/output assertions for all testcases corresponding
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
