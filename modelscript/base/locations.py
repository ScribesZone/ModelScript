# coding=utf-8
"""Location in a SourceFile"""

__all__ = (
    'Location',
    'SourceLocation'
)

from abc import ABCMeta, abstractmethod
from typing import Optional, Text


class Location(object, metaclass=ABCMeta):
    """Abstract location."""
    def __init__(self):
        pass

    @abstractmethod
    def str(self):
        pass


class SourceLocation(Location):

    sourceFile: Optional['SourceFile']  # from modelscript.base.sources
    filename: Optional[str]
    line: Optional[int]
    column: Optional[int]

    def __init__(self,
                 sourceFile=None,
                 fileName=None,
                 line=None,
                 column=None):
        super(SourceLocation, self).__init__()
        self.sourceFile = sourceFile
        if sourceFile is not None and fileName is None:
            fn = sourceFile.fileName
        else:
            fn = fileName
        self.fileName = fn
        self.line = line
        self.column = column

    def str(self):
        _ = []
        if self.fileName is not None:
            _.append(self.fileName)
        if self.line is not None:
            _.append(str(self.line))
        if self.column is not None and self.line is not None:
            _.append(str(self.line))
        return ':'.join(_)

    def __str__(self):
        return self.str()
