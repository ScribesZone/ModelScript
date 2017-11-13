# coding=utf-8


from __future__ import unicode_literals, print_function, absolute_import, division

from abc import abstractmethod, ABCMeta
from typing import Text, Optional, List
import re

from modelscribes.config import Config
from modelscribes.base.files import (
    readFileLines,
    writeTmpFileLines
)

#-----------------------------------------------------
#  Line transfos
#-----------------------------------------------------

class Transfo(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def do(self, line):
        #type: (Text) -> Optional[Text]
        pass


class RegexpTransfo(object):
    def __init__(self, regexp, result):
        self.regexp=regexp
        self.result=result

    def do(self, line):
        #type: (Text) -> Optional[Text]
        m=re.match(self.regexp, line )
        if m:
            return self.result.format(**m.groupdict())
        else:
            return None

class PrefixToCommentTransfo(object):
    def __init__(self, prefixes):
        self.prefixes = prefixes
        re_prefix = ( '(%s)' %
                         ('|'.join(prefixes)) )
        self.regexp=('^(?P<all> *%s.*)'
                     % re_prefix)

    def do(self, line):
        #type: (Text) -> Optional[Text]
        m=re.match(self.regexp, line)
        if m:
            return '--@%s' % m.group('all')
        else:
            return None


#-----------------------------------------------------
#  File preprocessor
#-----------------------------------------------------

class Preprocessor(object):
    def __init__(self,
                 sourceText,
                 targetText,
                 targetExtension):
        #type: (Text, Text, Text) -> None
        self.sourceText=sourceText #type: Text
        self.targetText=targetText #type: Text
        self.targetExtension=targetExtension
        self.transfos=[] #type: List[Transfo]

    def addTransfo(self, transfo):
        self.transfos.append(transfo)

    def transformLine(self, line):
        for t in self.transfos:
            new=t.do(line)
            if new is not None:
                return new
        return line

    def preprocessLine(self, line):
        newLine=self.transformLine(line)
        if Config.preprocessorPrint>=1:
            if line==newLine:
                print('pp:       ', line)
            else:
                print('pp: xxxxx ', line)
                print('pp: >>>>> ', newLine)
        return newLine

    def do(self, issueOrigin, filename):
        if Config.preprocessorPrint>=1:
            print('\npp: '+'='*30+' preprocessing  '+'='*30)
        lines=readFileLines(
            file=filename,
            issueOrigin=issueOrigin,
            message=
                'Cannot read '+self.sourceText+' %s.')
        new_lines=[
            self.preprocessLine(l) for l in lines ]
        if Config.preprocessorPrint>=1:
            print('pp: '+'='*30+' end preprocessing '+'='*30)

        return writeTmpFileLines(
            lines=new_lines,
            extension=self.targetExtension,
            message=
                'Cannot write '+self.targetText+' %s.')
