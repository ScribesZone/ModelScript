# coding=utf-8

"""
Model errors in source files either localized or not.
"""
import os
from collections import OrderedDict
from typing import Optional, List, Text, Union, Callable, Dict

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

    Levels=[Fatal, Error, Warning, Info, Hint]


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

        self.origin = origin  #type: WithIssueList
        """ The source file. An instance of SourceFile. """

        self.message = message
        """ The error message. """

        self.level=level  #type:Level

        self.origin.issueBox._add(self)
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
        self.sourceFile = sourceFile
        """ The source file. An instance of SourceFile. """

        self.fileName = (
            fileName if fileName is not None
            else self.sourceFile.fileName )

        self.line = line
        self.column = column #type: Optional[int]

        super(LocalizedIssue, self).__init__(
            origin=sourceFile,
            level=level,
            message=message)




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
        if self.fileName is not None:
            if filetransfo is None:
                fileexpr=self.fileName
            elif filetransfo=='basename':
                fileexpr=os.path.basename(self.fileName)
            else:
                fileexpr=filetransfo(self.fileName)
        else:
            fileexpr=''

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
            if self.column is not None:
                cursor_line = \
                    prefixStd \
                    + ' '*(self.column - 1) \
                    + '^'
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


class IssueBox(object):

    def __init__(self, parent=None):
        #type: (IssueBox) -> None
        self._issueList=[] #type: List[Issue]
        self.parent=parent #type:Optional[IssueBox]

        self._issuesAtLine=OrderedDict() #type: Dict[Optional[int], List[Issue]]
        """ 
        Store for a given line the issues at this line.
       There is no  entry for lines without issues.
        _issuesAtLine[0] are are not localized issues.
        """

    def _add(self, issue):
        # called by the issue constructor
        # Issue -> None
        self._issueList.append(issue)
        if isinstance(issue, LocalizedIssue):
            index=issue.line
        else:
            index=None
        if index not in self._issuesAtLine:
            self._issuesAtLine[index]=[]
        self._issuesAtLine[index].append(issue)
        # for i in self._issuesAtLine.keys():
        #     print('     ******* %s : %s' % (
        #         i,
        #         self._issuesAtLine[i]
        #     ))
        #
        # print('**** search %s :%s' % (
        #     index,
        #     self.at(index),
        # ))


    def at(self, lineNo):
        """
        Return the list of issues at the specified line.
        If the line is 0 then return non localized issues.
        Return both local and parents issues.
        """
        # int -> List[Issue]
        parent_issues=(
            [] if self.parent is None
            else self.parent.at(lineNo))
        self_issues=(
            [] if lineNo not in self._issuesAtLine
            else self._issuesAtLine[lineNo]
        )
        all=parent_issues+self_issues
        return all

    @property
    def all(self):
        """
        Return both local and parents issues
        """
        return (
            ([] if self.parent is None else self.parent.all)
            + self._issueList
        )

    @property
    def nb(self):
        return len(self.all)

    def select(self,
               level=None, op='=',
               line=None ):
        #type: (Optional[Level], str, Optional[bool], Optional[int]) -> List[Issue]
        if level is None and line is None:
            return list(self.all)
        issues_at=(
            self.all if line is None
            else self.at(line))
        return [
            i for i in issues_at
            if i.level.cmp(level, op) ]

    @property
    def bigIssues(self, level=Levels.Error):
        return self.select(level=level,op='>=')

    @property
    def smallIssues(self, level=Levels.Warning):
        return self.select(level=level,op='<=')

    @property
    def isValid(self):
        # () -> bool
        return len(self.bigIssues)==0

    @property
    def hasIssues(self):
        return len(self.all) != 0

    def summary(self):
        if self.nb==0:
            return ''
        level_msgs=[]
        for l in Levels.Levels:
            n=len(self.select(level=l))
            if n>0:
                level_msgs.append('%i %s%s' % (
                    n,
                    l.label,
                    's' if n>=2 else ''))
        return (
            '**** %i issue%s (%s)' % (
                self.nb,
                's' if self.nb>=2 else '',
                ','.join(level_msgs)
            )
        )



    def str(self, level=None, op='=', showSource=True):
        return '\n'.join([
            i.str(showSource=showSource)
            for i in self.select(level,op)])

    def __str__(self):
        return self.str()


class WithIssueList(object):
    def __init__(self, parent=None):
        self.issueBox=IssueBox(parent=parent)

    @property
    def isValid(self):
        # () -> bool
        return self.issueBox.isValid

    @property
    def hasIssues(self):
        return self.issueBox.hasIssues

    def addIssue(self, sourceError):
        self.issueBox._add(sourceError)
