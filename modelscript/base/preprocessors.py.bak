# coding=utf-8


from __future__ import unicode_literals, print_function, absolute_import, division

from abc import abstractmethod, ABCMeta
from typing import Text, Optional, List
import re

from modelscript.config import Config
from modelscript.base.files import (
    readFileLines,
    replaceExtension
)
from modelscript.interfaces.environment import (
    Environment
)

DEBUG=3

#-----------------------------------------------------
#  Line transfos
#-----------------------------------------------------

class Transfo(object):
    __metaclass__ = ABCMeta

    def __init__(self, stop=False):
        self.stop=stop
        """ Indicate if other transformations are applied after this one """

    @abstractmethod
    def do(self, line):
        #type: (Text) -> Optional[Text]
        pass


class RegexpTransfo(Transfo):

    def __init__(self, regexp, result, stop=False):
        super(RegexpTransfo, self).__init__(stop=stop)
        self.regexp=regexp
        self.result=result

    def do(self, line):
        #type: (Text) -> Optional[Text]
        m=re.match(self.regexp, line )
        if m:
            return self.result.format(**m.groupdict())
        else:
            return None

class PrefixToCommentTransfo(Transfo):
    def __init__(self, prefixes, stop=False):
        super(PrefixToCommentTransfo, self).__init__(stop=stop)
        self.prefixes = prefixes
        re_prefix = ( '(%s)' %
                         ('|'.join(prefixes)) )
        self.regexp=('^(?P<before> *)(?P<all> *%s.*)'
                     % re_prefix)

    def do(self, line):
        #type: (Text) -> Optional[Text]
        m=re.match(self.regexp, line)
        if m:
            return '%s--@%s' % (
                m.group('before'),
                m.group('all'))
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
        current=line
        for t in self.transfos:
            replacement=t.do(current)
            if replacement is not None:
                if t.stop:
                    return replacement
                else:
                    current=replacement
        return current

    def preprocessLine(self, line):
        newLine=self.transformLine(line)
        if Config.preprocessorPrint>=1 or DEBUG>=2:
            if line==newLine:
                print('PRE:       ', line)
            else:
                print('PRE: xxxxx ', line)
                print('PRE: >>>>> ', newLine)
        return newLine

    def do(self, issueOrigin, filename):
        if Config.preprocessorPrint>=1 or DEBUG>=1:
            print('\nPRE: '+'='*30+' preprocessing'+'='*30)
        lines=readFileLines(
            file=filename,
            issueOrigin=issueOrigin,
            message=
                'Cannot read '+self.sourceText+' %s.')
        new_lines=[
            self.preprocessLine(l) for l in lines ]

        if Config.preprocessorPrint>=1 or DEBUG>=1:
            print('PRE: ' + '=' * 30 + ' end preprocessing ' + '=' * 30)
        return Environment.writeWorkerFileLines(
            lines=new_lines,
            basicFileName=replaceExtension(filename, self.targetExtension),
            issueOrigin=issueOrigin)