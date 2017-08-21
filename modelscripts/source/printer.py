# coding=utf-8
from __future__ import unicode_literals, print_function, absolute_import, division
from typing import Text, Union, Optional, Dict, List
from abc import ABCMeta, abstractmethod

def indent(prefix,s):
    return '\n'.join([ prefix+l for l in s.split('\n') ])


class AbstractPrinter(object):
    __metaclass__ = ABCMeta

    def __init__(self, displayLineNos=True):
        #type: (bool) -> None
        self.output = ''
        self.displayLineNos=displayLineNos

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
                ):
        if linesBefore >= 1:
            for i in range(linesBefore):
                self.outLine('')
        self.out(self.lineNoString(lineNo=lineNo))
        self.out('%s%s' % (prefix,s) )
        if suffix is not None:
            self.out(suffix)
        if linesAfter >= 1:
            for i in range(linesAfter):
                self.outLine('')

    @abstractmethod
    def do(self):
        self.output = ''



