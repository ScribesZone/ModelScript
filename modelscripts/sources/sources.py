# coding=utf-8

"""
Source files and annotated source files.
"""

import os
import io
from abc import ABCMeta, abstractproperty
from typing import Text, List, Optional
import fragments
import abc
from modelscripts.sources.issues import (
    IssueList,
    Issue,
    Levels,
    WithIssueList,
)


class SourceElement(object):
    """
    Element of a source file.
    """
    __metaclass__ = ABCMeta
    def __init__(self, name=None, code=None, lineNo=None, docComment=None, eolComment=None):
        self.name = name
        self.source = code
        self.lineNo = lineNo
        self.docComment = docComment
        self.eolComment = eolComment

class DocCommentLines(object):
    def __init__(self):
        self.lines = []

    def add(self, line):
        #type: (Text) -> None
        assert line is not None
        self.lines.append(line)

    def consume(self):
        #type: () -> Optional[List[Text]]
        if len(self.lines)==[]:
            return None
        else:
            _ = self.lines
            self.lines=[]
            return _

    def clean(self):
        self.lines=[]

class SourceFile(WithIssueList):
    """
    A source file seen as as sequence of lines.
    The source file may contains some list of errors.
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self,
                 fileName,
                 realFileName=None,
                 preErrorMessages=()):
        #type: (Text, Optional[Text]) -> None

        assert fileName is not None

        WithIssueList.__init__(self, parent=None)

        self.fileName=fileName
        #type: Text
        """ The filename as given when creating the source file"""

        self.realFileName=(
            fileName if realFileName is None
            else realFileName)
        """ 
        The name of the actual file name that is parsed.
        This is almost never used so don't use it unless
        you know what you are doing. 
        """

        if len(preErrorMessages) >= 1:
            for msg in preErrorMessages:
                Issue(
                    origin=self,
                    level=Levels.Error,
                    message=msg
                )
            return

        # print('******************',self.realFileName)
        if not os.path.isfile(self.realFileName):
            Issue(
                origin=self,
                level=Levels.Fatal,
                message='File not found: %s' % self.fileName)
        self.sourceLines=self._doReadFileLines()
        #type: List[Text]



    #
    # def getFileToParse(self):
    #     return self.fileName

    def _doReadFileLines(self):
        #type: (Text)->List(Text)
        """
        Read a file as a list of line.  """
        with io.open(self.realFileName, 'rU', encoding='utf8') as f:
            lines = list(
                line.rstrip() for line in f.readlines())
        f.close()
        return lines

    @property
    def name(self):
        #type: ()->Text
        """
        The name of the source.
        By default the filename without extension. Subclasses
        can override this method
        """
        return (
            os.path.splitext(os.path.basename(self.fileName))[0])


    @property
    def directory(self):
        return os.path.dirname(self.fileName)

    @property
    def length(self):
        return len(self.sourceLines)

    def __repr__(self):
        return ('SourceFile(%s)'%self.fileName)



class AnnotatedSourceFile(SourceFile):
    """
    A source file with annotated fragments. The source can be viewed
    both as a flat sequence of line or as a fragment trees.
    The annotation markers can be defined when building the source file.
    """
    def __init__(self, fileName,
                 openingMark = r'--oo<< *(?P<value>[^ \n]+) *$',
                 closingMark = r'--oo>> *$',
                 hereMark = r'--oo== *(?P<value>[^ \n]+) *$'):
        """
        Create a annotated source file. The mark have to be provided
        in the form of regular expression with sometimes an optional
        named group with the named value. That is a regexp group like
        (?P<value> ... ). This part will be extracted and will
        constitute the name of the mark.
        :param fileName: the file name
        :type fileName: str
        :param openingMark: The opening mark with ?P<value> group
        :type openingMark: str
        :param closingMark: The closing mark
        :type closingMark: str
        :param hereMark: The here mark with ?P<value> group
        :type hereMark: str
        :return: AnnotatedSourceFile
        :rtype: AnnotatedSourceFile
        """

        super(AnnotatedSourceFile,self).__init__(fileName)
        self.openingMark = openingMark
        self.closingMark = closingMark
        self.hereMark = hereMark

        fragmenter = fragments.RegexpFragmenter(
            self.sourceLines,
            openingMark, closingMark, hereMark,
            mainValue = self, firstPosition = 1)

        self.fragment = fragmenter.fragment
        """ The root fragment according to the given mark """

    def __repr__(self):
        return ('AnnotatedSourceFile(%s)'%self.fileName)



class ModelSourceFile(SourceFile):
    def __init__(self,
                 fileName,
                 realFileName=None,
                 preErrorMessages=()):
        #type: (Text, Optional[Text]) -> None
        super(ModelSourceFile, self).__init__(
            fileName=fileName,
            realFileName=realFileName,
            preErrorMessages=preErrorMessages
        )

    @property
    def allIssues(self):
        #type: () -> IssueList
        """
        All issues including model issues if present
        """
        if self.model is not None:
            return self.model.issues
        else:
            return self.issues

    @abstractproperty
    def model(self):
        """ Model resulting from the evaluation """
        #type: () -> Optional['Model']
        return None

    @abstractproperty
    def usedModelByKind(self):
        return {}

    @property
    def usedModels(self):
        return self.usedModelByKind.values()

