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

    def __init__(self, summary=False, displayLineNos=True, baseIndent=0):
        #type: (bool) -> None
        self._baseIndent=baseIndent
        self.output = ''
        self.displayLineNos=displayLineNos
        self.summary=summary

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

    def display(self):
        print(self.do())

# class ErrorsPrinter(object):
#     __metaclass__ = ABCMeta
#
#     def _errors(self):



class ModelPrinter(AbstractPrinter):
    __metaclass__ = ABCMeta

    def __init__(self,
                 theModel,
                 summary=False,
                 displayLineNos=True):
        assert theModel is not None
        super(ModelPrinter, self).__init__(
            summary=summary,
            displayLineNos=displayLineNos,
        )
        self.theModel=theModel

    def _issues(self):
        self.out(str(self.theModel.issues))

# Not used
class SourcePrinter(AbstractPrinter):
    __metaclass__ = ABCMeta

    def __init__(self,
                 theSource,
                 summary=False,
                 displayLineNos=True):
        assert theSource is not None
        super(SourcePrinter, self).__init__(
            summary=summary,
            displayLineNos=displayLineNos
        )
        self.theSource=theSource

    # def _do(self):
    #     self.output=''
    #     Model
    #
    def _issues(self):
        self.out(str(self.theSource.allIssues))



