# coding=utf-8

"""
Model errors in source files either localized or not.
"""
import os
from typing import Optional, List, Text, Union, Callable

class FatalError(Exception):
    def __init__(self, SourceError):
        super(FatalError, self).__init__()
        self.sourceError=SourceError

class Level(object):
    def __init__(self, label, rank):
        self.label=label
        self.rank=rank

    def __le__(self, other):
        return self.rank <= other.rank

    def __ge__(self, other):
        return self.rank >= other.rank

    def __eq__(self, other):
        return self.rank == other.rank

    def cmp(self, other, op='='):
        #type: (Level, Text) -> bool
        if op=='=':
            return self == other
        elif op=='<=':
            return self <= other
        elif op=='>=':
            return self >= other
        else:
            raise NotImplementedError('Operation %s is not allowed'%op)

    def __str__(self):
        return self.label

    def __repr__(self):
        return self.__str__()


class Levels(object):
    Hint=Level('Hint', 10)
    Info=Level('Info', 20)
    Warning=Level('Warning', 30)
    Error=Level('Error', 40)
    Fatal=Level('Fatal error', 50)


class Issue(object):
    """
    An issue in a given entity with issue list (WithIssueList).
    Direct instances of Issue are not localized.
    The class LocalizedIssue must be used if the error line is known.
    """
    def __init__(self, origin, level, message):
        #type: (WithIssueList, Level, 'Text') -> None
        """
        Create a source error and add it to the given SourceFile.
        Raise FatalError if the error is fatal and processing could not
        continue.
        """

        assert message is not None and message!=''

        self.origin = origin
        """ The source file. An instance of SourceFile. """

        self.message = message
        """ The error message. """

        self.level=level  #type:Level

        self.origin.issues._add(self)
        if level==Levels.Fatal:
            raise FatalError(self)



    def str(self, pattern='**** {level}:{message}', showSource=True): #showSource not used, but in subclasses
        """
        Display the error. Since the error is not localized
        direct instances of this class just display the level and
        the error message.
        Subclasses provide more information
        """
        return pattern.format(message=self.message, level=self.level)


    def __str__(self):
        return self.str()


    def __repr__(self):
        return self.__str__()


class LocalizedIssue(Issue):

    def __init__(self, sourceFile, level, message, line, column=None, fileName=None):
        #type: ('SourceFile', Level, Text, int, Optional[int], Optional[Text]) -> None
        """
        Create a localized source file and add it to the given source file.

        :param sourceFile: The Source File
        :param message: The error message.
        :param line: The line number of the error starting at 1. If the
        error is before the first line, 0 is an accepted value though.
        :param column: The column number of the error or None. If the errors
        is between the previous line and before the first column 0 is an
        acceptable value.
        :param fileName: An optional string representing the filename as
        to be output with the error message. If None is given, then this
        value will be taken from the source file.

        """
        super(LocalizedIssue, self).__init__(
            origin=sourceFile,
            level=level,
            message=message)

        self.sourceFile = sourceFile
        """ The source file. An instance of SourceFile. """

        self.fileName = fileName
        self.line = line
        self.column = column #type: Optional[int]


    def str(self,
            pattern='{level}:{file}:{line}:{column}: {message}',
            showSource=True,
            linesBefore=1,
            linesAfter=0,
            filetransfo='basename',
            prefixStd='**   ',
            prefixIssue='**** '):
        #type: (Text, bool, int, int, Union[Text,Callable[[Text],Text]]) -> Text

        def prefix(p, l):
            return [p+s for s in l]

        _ = []
        if filetransfo is None:
            fileexpr=self.fileName
        elif filetransfo=='basename':
            fileexpr=os.path.basename(self.fileName)
        else:
            fileexpr=filetransfo(self.fileName)
        issueline= prefixIssue+pattern.format(
            level=self.level,
            file=fileexpr,
            line=self.line,
            column=self.column,
            message=self.message )
        _.append(issueline)
        if showSource:
            if linesBefore >=1:
                begin = max(0, self.line - linesBefore)
                end = self.line
                _.extend(prefix(prefixStd,self.sourceFile.sourceLines[begin:end]))

            cursor_line = \
                prefixStd \
                + ' '*(self.column - 1) \
                + '^'
                # + ' '*(len(self.sourceFile.sourceLines[
                #                 max(0,self.line-1)])-self.column)
            _.append(cursor_line)

            if linesAfter:
                begin = self.line - 1
                end = max(len(self.sourceFile.sourceLines)-1,self.line+linesAfter-1)
                _.extend(prefix(prefixStd,self.sourceFile.sourceLines[begin:end]))




        return '\n'.join(_)


    def __str__(self):
        return '%s:%s:%s:%s %s' % (
            self.level,
            self.fileName,
            self.line,
            '' if self.column is None else str(self.column)+':',
            self.message)


    def __repr__(self):
        return self.__str__()


class IssueList(object):

    def __init__(self, parent=None):
        #type: (IssueList) -> None
        self._issueList=[] #type: List[Issue]
        self.parent=None #type:Optional[IssueList]

    def _add(self, issue):
        # called by the issue constructor
        self._issueList.append(issue)

    @property
    def all(self):
        return (
            ([] if self.parent is None else self.parent.all)
            + self._issueList
        )

    @property
    def nb(self):
        return len(self.all)

    def select(self, level=None, op='='):
        #type: (Level, Text) -> List[Issue]
        if level is None:
            return self.all
        return [
            i for i in self.all
            if i.level.cmp(level, op) ]

    @property
    def isValid(self):
        # () -> bool
        return len(self.select(Levels.Error, '<='))==0

    @property
    def hasIssues(self):
        return len(self.all) == 0

    def str(self, level=None, op='=', showSource=True):
        return '\n'.join([
            i.str(showSource=showSource)
            for i in self.select(level,op)])

    def __str__(self):
        return self.str()


class WithIssueList(object):
    def __init__(self, parent=None):
        self.issues=IssueList(parent=parent)

    @property
    def isValid(self):
        # () -> bool
        return self.issues.isValid

    @property
    def hasIssues(self):
        return self.issues.hasIssues

    def addIssue(self, sourceError):
        self.issues._add(sourceError)
