# coding=utf-8

"""
Source files and annotated source files.
"""

import abc
import io
import os
from abc import ABCMeta

from typing import Text, List, Optional

import fragments
from modelscribes.base.issues import (
    Issue,
    Levels,
    WithIssueList
)


class SourceElement(object):
    """
    Element of a source file.
    """
    __metaclass__ = ABCMeta
    def __init__(self, name=None, code=None, lineNo=None, docComment=None, eolComment=None):
        self.name = name
        self.code=code
        self.lineNo = lineNo
        self.docComment = docComment
        self.eolComment = eolComment



class SourceFile(WithIssueList):
    """
    A source file seen as as sequence of lines.
    The source file may contains some list of errors.
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self,
                 fileName,
                 realFileName=None,
                 preErrorMessages=(),
                 doNotReadFile=False):
        #type: (Text, Optional[Text]) -> None
        """
        Create a source by parsing a given file. It is possible
        to have a 'logical' file that is what the user see, and
        actually parse a 'real' file that is what the parser see.
        This could be useful for instance if one want to parse
        a annotated source generated from the source.

        Args:
            fileName:
                The logical name of the file.
                This is not necessarily the file parsed.
            realFileName:
                The real file to be read. If the reading
                has to be postponed, then the parameter
                should be set to None. The doRealFileRead()
                will set this parameter
            preErrorMessages:
                The errors in this list will be added.
            doNotReadFile:
                If False the file is read directly.
                Otherwise the method doReadFile must be called!
        """

        assert fileName is not None

        WithIssueList.__init__(self, parents=[])

        self.fileName=fileName #type: Text
        """ The filename as given when creating the source file"""

        self.realFileName=(
            None if doNotReadFile  # filled later
            else (
                fileName if realFileName is None
                else realFileName))
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

        self.sourceLines=[]  #type: List[Text]
        """
        The source lines of the 'logical' file.
        It will be the same as realSourceLines 
        if not isBasedInHiddenFile. 
        Filled by doReadFile but if doReadFile raise 
        an exception, the sourceLines will still be of the
        appropriate type (no lines)
        The caller must call doReadFile explictely
        if doNotReadFile.
        """

        self.realSourceLines=[]  #type: List[Text]
        """
        The source lines of the 'real' file.
        It will be the same as sourceLines 
        if not isBasedInHiddenFile.  
        Filled by doReadFile but if doReadFile raise 
        an exception, the sourceLines will still be of the
        appropriate type (no lines)
        The caller must call doReadFile explictely
        if doNotReadFile.
        """

        if not doNotReadFile:
            self.doReadFile(self.realFileName)


    @property
    def isBasedInHiddenFile(self):
        #type: () -> Optional[bool]
        """
        None before doReadFile if postponed.
        Otherwise indicated if the real file is the same
        is different from the logical one.
        """
        return (
            None if self.realFileName is None  #if before
            else self.realFileName != self.fileName
        )

    def doReadFile(self, realFileToRead):
        #type: (Text)->List(Text)
        """
        Read a file as a list of line and file self.sourceLines
        """
        def _read_lines(file):
            try:
                with io.open(file,
                             'rU',
                             encoding='utf8') as f:
                    lines = list(
                        line.rstrip() for line in f.readlines())
                return lines
            except :
                Issue(
                    origin=self,
                    level=Levels.Fatal,
                    message=('Cannot read file "%s"' %
                             file)
                )


        self.realFileName=realFileToRead

        # read the actual file
        self.realSourceLines= _read_lines(self.realFileName)

        if self.fileName==self.realFileName:
            self.sourceLines=self.realSourceLines
        else:
            # read the 'logical' source file
            self.sourceLines=_read_lines(self.fileName)
        return


    @property
    def name(self):
        #type: ()->Text
        """
        The name of the source.
        By default the filename without extension. Subclasses
        can override this method.
        This is the case in modelSource where the name is
        extracted from source.
        """
        return (
            os.path.splitext(os.path.basename(self.fileName))[0])

    @property
    def extension(self):
        #type: ()->Text
        """
        Extension of the file including '.'
        For instance '.clm'
        """
        return os.path.splitext(os.path.basename(self.fileName))[1]

    @property
    def basename(self):
        #type: ()->Text
        return os.path.basename(self.fileName)

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

