# coding=utf-8
"""
Merge a .soil file with a .stc file and return a .sex file::

* .soil files are command file used by USE OCL tool
* .stc files stands for scenario traces.
* .sex files stands for scenario exeuction.

A .soil file is the file used by USE to create scenarios and
objects.

A .stc file is the direct output of the use engine when the
soil file is interpreted. In contains some errors in soil
commands (in the form of <input:...). It also contains all the
useful information resulting from the execution::

* errors like <>
* results of query evaluation commands ("??" and "?")
* results of "check" commands.

The problem is that the comments in soil files are replaced
by blank lines in trace files. So it is not possible to get
directly the trace from the .soil output.

This merger aims to take execution results from the trace
(.stc) and merge them with the information in the original
(.soil) file.
"""

# TODO: add support for errors as well as corresponding test cases

from __future__ import  print_function
from typing import Text, List, Optional, Union
import re
import os
import tempfile


__all__=(
    'merge'
)

# DEBUG=3
DEBUG=0

class _NumberedFile(object):

    def __init__(self, filename):
        self.lines = list(
            line.rstrip()
            for line in open(filename, 'rU'))

        # for some reason the number of line is not
        # the same when python or java read it. That
        # is, if a file end with a \n, python assume
        # that there is no line after while use assume
        # that there is a blank line. To avoid the
        # problem add a blank line
        self.lines.append('')

        self.lineno=0
        self.length=len(self.lines)

    def nextLine(self):
        self.lineno += 1
        if (self.lineno>self.length):
            return None
        else:
            return self.lines[self.lineno-1]

    def line(self):
        l=self.lines[self.lineno-1]
        return l


class _SexFile(object):

    def __init__(self,
                 soilNumberedFile,
                 traceNumberedFile,
                 sexFileName=None):

        self.soil=soilNumberedFile
        self.trace=traceNumberedFile
        self.sexLines=[]

        if sexFileName is None:
            (f, sexFileName) = tempfile.mkstemp(suffix='.sex', text=True)
            os.close(f)
        self.sexFileName=sexFileName
        self.sexFileHandler=open(self.sexFileName, 'w')


    def out(self, side):
        #type: (Text) -> None
        assert (side in ['soil', 'trace'])
        if side == 'soil':
            self.soil.nextLine()
            out_line = '%05i:%s' % (
                self.soil.lineno,
                self.soil.line()
            )
            # Check that the content of the soil and the trace match
            # This is not the case for comment as they are removed
            # in the trace.
            if not re.match('^ *--.*', self.soil.line()):
                if not self.trace.line().endswith(self.soil.line()):
                    raise ValueError(
                        'Internal error: lines of soil and trace does not match:\n'
                        '%05i:%s\n%05i:%s\n' % (
                            self.soil.lineno,
                            self.soil.line(),
                            self.trace.lineno,
                            self.trace.line()
                        )
                    )
        else:
            out_line = '|||||:%s' % self.trace.line()
        if DEBUG:
            print(out_line)

        self.sexLines.append(out_line)
        self.sexFileHandler.write(out_line + '\n')

    def close(self):
        self.sexFileHandler.close()


def merge(soilFile, traceFile, sexFileName=None):
    #type: (Text, Text, Optional[Text])->Text

    if DEBUG:
        print('\nMerging %s and %s\n' % (
            os.path.basename(soilFile),
            os.path.basename(traceFile)
        ))

    soil=_NumberedFile(soilFile)
    trace=_NumberedFile(traceFile)
    merged=_SexFile(soil, trace, sexFileName)

    prefixSoil=os.path.basename(soilFile)
    in_check_result=False
    in_query_result=False



    while trace.nextLine() is not None:
        line=trace.line()
        if DEBUG:
            print('%5i: %s' % (trace.lineno, line))
        #sex.append(line)

        if re.match('^USE version ',line):
            if DEBUG>=2:
                print(' ' * 10 + 'skip')
            continue

        if re.match('^\w+\.soil> open \'.*\' *$',line):
            if DEBUG>=2:
                print(' ' * 10 + 'skip')
            continue

        #---- message for empty files
        if re.match('^Nothing to do, because file .*contains no data!',line):
            if DEBUG>=2:
                print(' ' * 10 + 'skip')
            continue

        #---- empty line

        if re.match('^'+prefixSoil+'> *$',line):
            if DEBUG>=2:
                print(' '*10+'blank')
            merged.out('soil')
            continue

        #---- operation

        if re.match('^'+prefixSoil+'> *!.*$',line):
            if DEBUG>=2:
                print(' '*10+'operation')
            merged.out('soil')
            continue


        #---- comment or skip

        if (re.match('^ *$',line)
            or re.match('^'+prefixSoil+'> *--.*',line)):
            if not in_check_result and not in_query_result:
                if DEBUG>=2:
                    print(' '*10+'comment')
                merged.out('soil')
                continue
            else:
                if DEBUG>=2:
                    print(' '*10+'skip')
                continue



        #---- query operation and result

        if re.match('^'+prefixSoil+'> *\?\??.*$',line):
            if DEBUG>=2:
                print(' '*10+'query')
            merged.out('soil')
            in_query_result=True
            continue

        if re.match('^Detailed results of subexpressions:$', line):
            if DEBUG>=2:
                print(' ' * 10 + 'skip')
            merged.out('trace')
            in_query_result = True
            continue

        if re.match('^  [^ ].*$', line) and in_query_result:
            if DEBUG>=2:
                print(' '*10+'query result')
            merged.out('trace')
            continue


        if re.match('^-> .* : .*$',line):
            if DEBUG>=2:
                print(' '*10+'query result end')
            in_query_result=False
            merged.out('trace')
            continue



        #---- check operation and result

        if (re.match('^'+prefixSoil+'> check *.*$', line)):
            if DEBUG>=2:
                print(' '*10+'check')
            in_check_result=True
            merged.out('soil')
            continue

        if (re.match('^checking invariant \([0-9]+\) `',line)):
            if DEBUG>=2:
                print(' ' * 10 + 'check result')
            in_check_result=True
            merged.out('trace')
            continue

        if re.match('^checked \d+ invariants in .*$',line):
            if DEBUG>=2:
                print(' '*10+'check result end')
            in_check_result=False
            merged.out('trace')
            continue

        if in_check_result:
            if DEBUG>=2:
                print(' '*10+'check result')
            merged.out('trace')
            continue

        if re.match('^.*\.soil> *quit *$', line):
            if DEBUG>=2:
                print('')
            break

        raise ValueError('Error: cannot parse line #%i of trace:\n"%s"' %(
            trace.lineno,
            trace.line()
        ))

    merged.close()
    return merged.sexFileName
