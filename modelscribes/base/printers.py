# coding=utf-8
from __future__ import unicode_literals, print_function, absolute_import, division
from typing import Text, Union, Optional, Dict, List
from abc import ABCMeta, abstractmethod

def indent(prefix, s, suffix='', firstPrefix=None):
    prefix1=prefix if firstPrefix is None else firstPrefix
    lines=s.split('\n')
    outLines=[prefix1+lines[0]+suffix]
    outLines.extend([prefix+l+suffix for l in lines[1:]])
    return '\n'.join(outLines)

class AbstractPrinter(object):
    __metaclass__ = ABCMeta

    def __init__(self,
                 summary=False,
                 displayLineNos=True,
                 baseIndent=0):
        #type: (bool) -> None
        self._baseIndent=baseIndent
        self.output = ''
        self.displayLineNos=displayLineNos
        self.summary=summary
        # self.eolAtEOF=eolAtEOF

    def indent(self, n=1):
        self._baseIndent+=n

    def out(self, s):
        self.output += s

    def lineNoString(self, lineNo=None):
        if not self.displayLineNos:
            return ''
        if lineNo is not None:
            return '% 4i|' % lineNo
        else:
            return ' ' * 4 + '|'

    def outLine(self,
                s,
                lineNo=None,
                suffix='\n',
                prefix='',
                linesBefore=0,
                linesAfter=0,
                indent=0,
                ):
        if linesBefore >= 1:
            for i in range(linesBefore):
                self.outLine('')
        self.out(self.lineNoString(lineNo=lineNo))
        self.out('%s%s%s' % (
            self._indentPrefix(indent)
            ,prefix,
            s) )
        if suffix is not None:
            self.out(suffix)
        if linesAfter >= 1:
            for i in range(linesAfter):
                self.outLine('')

    def _indentPrefix(self, indent=0):
        return ' '*(self._baseIndent+indent)

    @abstractmethod
    def do(self):
        pass

    def display(self, removeLastEOL=False, addLastEOL=True):
        text=self.do()
        endsWithEOL=text.endswith('\n')
        if removeLastEOL and endsWithEOL:
            text=text[:-1]
        if addLastEOL and not endsWithEOL:
            text=text+'\n'
        print(text, end='')

# class ErrorsPrinter(object):
#     __metaclass__ = ABCMeta
#
#     def _errors(self):



class ModelPrinter(AbstractPrinter):
    __metaclass__ = ABCMeta

    def __init__(self,
                 theModel,
                 summary=False,
                 displayLineNos=False):
        assert theModel is not None
        super(ModelPrinter, self).__init__(
            summary=summary,
            displayLineNos=displayLineNos,
        )
        self.theModel=theModel

    def _issues(self):
        self.out(str(self.theModel.issueBox))

# Not used
class SourcePrinter(AbstractPrinter):
    __metaclass__ = ABCMeta

    def __init__(self,
                 theSource,
                 summary=False,
                 displayLineNos=False):
        assert theSource is not None
        super(SourcePrinter, self).__init__(
            summary=summary,
            displayLineNos=displayLineNos
        )
        self.theSource=theSource

    def _issues(self):
        self.out(str(self.theSource.fullIssueBox))



class AnnotatedSourcePrinter(SourcePrinter):

    def __init__(self,
                 theSource):
        #type: ('Source') -> None

        assert theSource is not None
        super(AnnotatedSourcePrinter, self).__init__(
            theSource=theSource,
            summary=False,
            displayLineNos=False,
        )

    def do(self):
        self.output=''

        self._issueHeader()

        for (index, line) in enumerate(self.theSource.sourceLines):
            line_no=index+1
            # self.out(str(line_no))
            self._line(line_no, line)
            localized_issues=self.theSource.fullIssueBox.at(line_no)
            if localized_issues:
                self._localizedIssues(localized_issues)
        return self.output

    def _issueHeader(self):
        self._issuesSummary(self.theSource.fullIssueBox)
        unlocalized_issues=self.theSource.fullIssueBox.at(0)
        self._unlocalizedIssues(unlocalized_issues)

    def _line(self, line_no, line):
        self.outLine(line)

    def _issuesSummary(self, issueBox):
        s=issueBox.summaryLine
        if s!='':
            self.outLine(issueBox.summaryLine)

    def _unlocalizedIssues(self, issues, pattern='{level}: {message}'):
        for i in issues:
            self.outLine(
                i.str(pattern=pattern))

    def _localizedIssues(self, issues, pattern='{level}: {message}'):
        for i in issues:
            self.outLine(
                i.str(pattern=pattern,
                    linesBefore=0))