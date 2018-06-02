# coding=utf-8

"""
Source files and annotated source files.
"""

import abc
import os
from abc import ABCMeta

from typing import Text, List, Optional, Any

import modelscripts.base.fragments
from modelscripts.base.files import (
    readFileLines
)
from modelscripts.base.issues import (
    Issue,
    LocalizedSourceIssue,
    Level,
    Levels,
)

#TODO:3 This dependency should be removed
# With inheritance this is not so easy because
# the __init__ method would call WithIssueList wihch
# do not register the issue box in the megamodel
from modelscripts.megamodels.issues import WithIssueModel


class SourceElement(object):
    """
    Element of a source file.
    """
    __metaclass__ = ABCMeta
    def __init__(self,
                 name=None,
                 astNode=None,
                 lineNo=None,
                 code=None,
                 description=None,
                 eolComment=None):
        self.name = name
        self.astNode=astNode
        self.lineNo = lineNo
        self.code=code
        self.description = description
        self.eolComment = eolComment



class OldSourceFile(WithIssueModel):  # TODO: should be WithIssueList
    """
    A source file seen as as sequence of lines.
    The source file may contains some list of errors.
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self,
                 fileName,
                 realFileName=None,
                 prequelFileName=None,
                 preErrorMessages=(), # Type to be checked
                 doNotReadFiles=False,
                 allowedFeatures=()):
        #type: (Text, Optional[Text], Optional[Text], List[Any], bool, List[Text]) -> None
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
            doNotReadFiles:
                If False the file is read directly.
                Otherwise the method doReadFile must be called!
        """

        assert fileName is not None

        self.fileName=fileName #type: Text
        """ The filename as given when creating the source file"""

        self.prequelFileName=(
            fileName if prequelFileName is None
            else prequelFileName
        )
        """ 
        The named of the unprocessed file or the filename.
        This is useful when a preprocessor is used. 
        """

        self.realFileName=(
            None if doNotReadFiles  # filled later
            else (
                fileName if realFileName is None
                else realFileName))
        """ 
        The name of the actual file name that is parsed.
        This is almost never used so don't use it unless
        you know what you are doing. 
        """

        # This should be after the definition of
        # filenames
        super(OldSourceFile, self).__init__(parents=[])


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
        if doNotReadFiles.
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
        if doNotReadFiles.
        """

        self.allowedFeatures=allowedFeatures #type: List[Text]
        """
        A list of feature names that could be issued
        in the parser.
        """




        if not doNotReadFiles:
            self.doReadFiles(
                logicalFileName=self.fileName,
                realFileName=self.realFileName)

    def checkAllowed(
            self,
            feature,
            message,
            lineNo=None,
            level=Levels.Fatal ):
        # type: (Text, Text, int, Level, Text) -> bool
        """
        Check if a feature is allowed.
        If this not the case raise an issue with
        a proper message (see the code).
        """
        is_allowed = feature in self.allowedFeatures
        if not is_allowed:
            if lineNo is None:
                Issue(self, level=level, message=message )
            else:
                LocalizedSourceIssue(
                    sourceFile=self,
                    level=level,
                    message=message,
                    line=lineNo
                )
        return is_allowed

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

    def doReadFiles(self, logicalFileName=None, realFileName=None):
        #type: (Text)->List(Text)
        """
        Read one or two files.
        """
        assert logicalFileName or realFileName
        if logicalFileName is not None:
            self.fileName=logicalFileName
            self.sourceLines=readFileLines(
                file=self.fileName,
                issueOrigin=self,
                message='Cannot read source file %s')
        if realFileName is not None:
            self.realFileName=realFileName
            if logicalFileName==realFileName:
                self.realSourceLines=self.sourceLines
            else:
                self.realFileName = realFileName
                self.realSourceLines = readFileLines(
                    file=self.realFileName,
                    issueOrigin=self,
                    message='Cannot read generated file %s')

    @property
    def path(self):
        return os.path.realpath(self.fileName)

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
        For instance '.cls'
        """
        return os.path.splitext(os.path.basename(self.fileName))[1]

    @property
    def basename(self):
        #type: ()->Text
        return os.path.basename(self.fileName)

    @property
    def label(self):
        #type: ()->Text
        return "'%s'" % self.basename

    @property
    def directory(self):
        return os.path.dirname(self.fileName)

    @property
    def length(self):
        return len(self.sourceLines)

    def __repr__(self):
        return ('OldSourceFile(%s)'%self.fileName)



class AnnotatedOldSourceFile(OldSourceFile):
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
        :return: AnnotatedOldSourceFile
        :rtype: AnnotatedOldSourceFile
        """

        super(AnnotatedOldSourceFile, self).__init__(fileName)
        self.openingMark = openingMark
        self.closingMark = closingMark
        self.hereMark = hereMark

        fragmenter = modelscripts.base.fragments.RegexpFragmenter(
            self.sourceLines,
            openingMark, closingMark, hereMark,
            mainValue = self, firstPosition = 1)

        self.fragment = fragmenter.fragment
        """ The root fragment according to the given mark """

    def __repr__(self):
        return ('AnnotatedOldSourceFile(%s)'%self.fileName)

