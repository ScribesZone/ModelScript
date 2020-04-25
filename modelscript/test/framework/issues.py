# coding=utf-8
"""Helper functions to create assertion based on issues.
This module is used by the assertions module.

Assertions on issues can be specified like this :

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

"""

import re

from modelscript.base.issues import Level, Levels

F=Levels.Fatal
E=Levels.Error
W=Levels.Warning
I=Levels.Info
H=Levels.Hint


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


RE_ISSUE_HEADER=r'^ *// *@ *Issue'
RE_ISSUE_LABEL=r'(?P<label>[\w.]+)'
RE_ISSUE_COUNT=r'(?P<count>([\d]+|\*))'
RE_ISSUE_SPEC='%s +%s +%s' % (
    RE_ISSUE_HEADER, RE_ISSUE_LABEL, RE_ISSUE_COUNT)


def extractExpectedIssuesMapFromFile(fileName):
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