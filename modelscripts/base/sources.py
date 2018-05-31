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
                 description=None):
        self.name = name
        self.astnode=astNode
        self.lineNo = lineNo
        self.description = description



class SourceFile(WithIssueModel):  # TODO: should be WithIssueList
    """
    A source file seen as as sequence of lines.
    Subclasses may add more elements such as a Model.
    The source file may contains some list of errors.
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, fileName):
        #type: (Text) -> None

        assert fileName is not None

        self.fileName=fileName #type: Text
        """ The filename as given when creating the source file"""

        # This should be after the definition of filenames
        super(SourceFile, self).__init__(parents=[])

        self.sourceLines=[]  #type: List[Text]
        """
        The source lines of the file.
        """
        self.sourceLines=readFileLines(
            file=self.fileName,
            issueOrigin=self,
            message='Cannot read source file %s')

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
