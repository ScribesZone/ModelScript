# coding=utf-8
from abc import ABCMeta, abstractmethod
from typing import Optional, Text

class Location(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def str(self):
        pass


class SourceLocation(Location):

    def __init__(self,
                 sourceFile=None,
                 fileName=None,
                 line=None,
                 column=None):
        super(SourceLocation, self).__init__()

        self.sourceFile = sourceFile
        #type: Optional['SourceFile']

        if sourceFile is not None and fileName is None:
            fn = sourceFile.fileName
        else:
            fn = fileName
        self.fileName = fn  # type: Optional[Text]

        self.line = line  # type Optional[int]
        self.column = column  # type Optional[int]

    def str(self):
        _ = []
        if self.fileName is not None:
            _.append(self.fileName)
        if self.line is not None:
            _.append(unicode(self.line))
        if self.column is not None and self.line is not None:
            _.append(unicode(self.line))
        return ':'.join(_)

    def __str__(self):
        return self.str()
