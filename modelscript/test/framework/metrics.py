# coding=utf-8
"""Helper functions to create assertion based on model metrics.
This module is used by the assertions module.
"""

import re

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


RE_METRIC_HEADER=r'^ *// *@ *Metric'
RE_METRIC_LABEL=r'"(?P<label>[^"]+)"'
RE_METRIC_COUNT=r'(?P<count>([\d]+|\*))'
RE_METRIC_SPEC='%s +%s +%s' % (
    RE_METRIC_HEADER, RE_METRIC_LABEL, RE_METRIC_COUNT)


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
