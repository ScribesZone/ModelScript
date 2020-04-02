# coding=utf-8
"""
Source files and annotated source files.
"""
__all__=(
    'SourceElement',
    'SourceFile',
)
import abc
import os
from abc import ABCMeta
from typing import List, Optional, Any

from modelscript.base.files import (
    readFileLines
)

# TODO:3 The dependency below should be removed
# With inheritance this is not so easy because
# the __init__ method would call WithIssueList wihch
# do not register the issue box in the megamodel
from modelscript.megamodels.issues import WithIssueModel


class SourceElement(object, metaclass=ABCMeta):
    """Element of a source file.
    """
    name: Optional[str]
    astNode: Optional['TextXNode']
    lineNo: Optional[int]
    description: Optional[str]

    def __init__(self,
                 name=None,
                 astNode=None,
                 lineNo=None,
                 description=None):
        self.name = name
        self.astNode = astNode
        self.lineNo = lineNo
        self.description = description


class SourceFile(WithIssueModel, metaclass=abc.ABCMeta):  # TODO:3 should be WithIssueList
    """A source file seen as as sequence of lines.
    Subclasses may add more elements such as a Model.
    The source file may contains some list of errors.
    """
    filename: str
    """The filename as given when creating the source file"""
    sourceLines: List[str]
    """The source lines of the file."""

    def __init__(self,
                 fileName: str) \
            -> None:

        assert fileName is not None
        self.fileName = fileName
        # This should be after the definition of filenames
        super(SourceFile, self).__init__(parents=[])
        self.sourceLines = []
        self.sourceLines = readFileLines(
            file=self.fileName,
            issueOrigin=self,   #TODO:1 check type
            message='Cannot read source file %s')

    @property
    def path(self) -> str:
        """ The real path of the source."""
        return os.path.realpath(self.fileName)

    @property
    def name(self) -> str:
        """ The name of the source.
        By default the filename without extension. Subclasses
        can override this method.
        This is the case in modelSource where the name is
        extracted from source.
        """
        return (
            os.path.splitext(os.path.basename(self.fileName))[0])

    @property
    def extension(self) -> str:
        """
        Extension of the file including '.'
        For instance '.cls'
        """
        return os.path.splitext(os.path.basename(self.fileName))[1]

    @property
    def basename(self) -> str:
        return os.path.basename(self.fileName)

    @property
    def label(self) -> str:
        return "'%s'" % self.basename

    @property
    def directory(self) -> str:
        return os.path.dirname(self.fileName)

    @property
    def length(self) -> int:
        return len(self.sourceLines)

    def __repr__(self):
        return 'SourceFile(%s)'%self.fileName
