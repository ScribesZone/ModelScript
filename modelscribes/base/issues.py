# coding=utf-8

"""
Model errors in source files either localized or not.
"""
import os
from collections import OrderedDict
from typing import Optional, List, Text, Union, Callable, Dict
from modelscribes.base.annotations import (
    Annotations
)

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
    The class LocalizedIssue must be used if the error line
    is known.
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



    def str(self,
            pattern=Annotations.prefix+'{level}:{message}',
            mode='fragment'): #showSource not used, but in subclasses
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
        :param line: The line number of the error
            starting at 1. If the error is before
            the first line, it is moved to (1,0)
            If the error is after the end
            of the file (typically the last line)
            the line recorded is assumed to be
            the last character of the last line.
        :param column: The column number of the
            error or None. If the errors is between
            the previous line and before the
            first column 0 is an acceptable value.
        :param fileName: An optional string
            representing the filename to be output
            with the error message. If None is
            given, then this alue will be taken
            from the source file.
        """


        self.sourceFile = sourceFile
        """ The source file. An instance of SourceFile. """

        self.fileName = (
            fileName if fileName is not None
            else self.sourceFile.fileName )

        #------ ajust line,col if necessary
        lines=sourceFile.sourceLines
        nblines=len(lines)
        if line==0:
            # move error before first line to first
            l=1
            c=0
        elif nblines==0:
            l=1
            c=0
        elif line>nblines:
            # move error after last line to last line
            l=nblines
            c=len(lines[nblines-1])
        else:
            # regular location for a line
            l=line
            c=column

        self.line = l #type: int
        """
        The line number between 1 and the nb of lines.
        This values may have been adjusted
        """

        self.column = c #type: Optional[int]
        """
        The column number or None. If defined
        it could be 0 or 1 more than the length 
        of the line
        """

        super(LocalizedIssue, self).__init__(
            origin=sourceFile,
            level=level,
            message=message)




    def str(self,
            pattern='{level}:{file}:{line}:{column}: {message}',
            mode='fragment', # source, annotation, simple
            linesBefore=1,
            linesAfter=0,
            filetransfo='basename',
            prefixStd=Annotations.cont,
            prefixIssue=Annotations.prefix):
        #type: (Text, Text, int, int, Union[Text,Callable[[Text],Text]]) -> Text

        assert mode in ['fragment', 'annotation', 'simple']

        def prefix(p, l):
            return [p+s for s in l]

        def issue_lines():
            # type: () -> List[Text]
            if self.fileName is not None:
                if filetransfo is None:
                    fileexpr = self.fileName
                elif filetransfo == 'basename':
                    fileexpr = os.path.basename(self.fileName)
                else:
                    fileexpr = filetransfo(self.fileName)
            else:
                fileexpr = ''
            line= prefixIssue + pattern.format(
                level=self.level,
                file=fileexpr,
                line=self.line,
                column=self.column,
                message=self.message)
            # remove the col number if None
            line=line.replace('None:','')
            return [line]

        def cursor_lines():
            #type: () -> List[Text]
            if self.column is None:
                return []
            else:
                line=(
                    prefixStd
                    + ' '*(self.column) #-len(prefixStd))
                    + '^' )
                return [line]

        def before_lines():
            #type: () -> List[Text]
            if linesBefore==0:
                return []
            else:
                begin=max(0, self.line - linesBefore)
                end=self.line
                lines=prefix(
                    prefixStd,
                    self.sourceFile.sourceLines[begin:end])
                return lines

        def after_lines():
            if linesAfter==0:
                return []
            else:
                begin = self.line - 1
                end = max(
                    len(self.sourceFile.sourceLines) - 1,
                    self.line + linesAfter - 1)
                lines=prefix(
                    prefixStd,
                    self.sourceFile.sourceLines[begin:end])
                return lines

        if mode=='annotation':
            lines=(
                cursor_lines()
                + issue_lines() )
        elif mode=='fragment':
            lines=(
                before_lines()
                +cursor_lines()
                +issue_lines()
                +after_lines()
            )
        elif mode=='simple':
            lines=(
                issue_lines()
            )
        else:
            raise NotImplementedError('mode %s does not exist' % mode)
        return '\n'.join(lines)


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

    def __init__(self, parents=()):
        #type: (List[IssueBox]) -> None
        self._issueList=[] #type: List[Issue]
        self.parents=list(parents) #type:List[IssueBox]

        self._issuesAtLine=OrderedDict() #type: Dict[Optional[int], List[Issue]]
        """ 
        Store for a given line the issues at this line.
        There is no  entry for lines without issues.
        _issuesAtLine[0] are are not localized issues.
        """

    def _add(self, issue):
        #type: (Issue) -> None
        # called by the issue constructor
        # Issue -> None
        self._issueList.append(issue)
        if isinstance(issue, LocalizedIssue):
            index=issue.line
        else:
            index=0
        if index not in self._issuesAtLine:
            self._issuesAtLine[index]=[]
        self._issuesAtLine[index].append(issue)

    def addParent(self, issueBox):
        #type: (IssueBox) -> None
        """
        Add the issue box as the last parents.
        If it is already in the list, do nothing.
        """
        if not issueBox in self.parents:
            self.parents.append(issueBox)



    def at(self, lineNo, parentsFirst=True):
        """
        Return the list of issues at the specified line.
        If the line is 0 then return non localized issues.
        Return both local and parents issues.
        """
        # int -> List[Issue]
        parent_issues=[
            i for p in self.parents
                for i in p.at(lineNo, parentsFirst=parentsFirst) ]
        self_issues=(
            [] if lineNo not in self._issuesAtLine
            else self._issuesAtLine[lineNo]
        )
        if parentsFirst:
            return parent_issues+self_issues
        else:
            return self_issues+parent_issues

    @property
    def all(self):
        """
        Return both local and parents issues
        """
        return (
            [ i for p in self.parents
                    for i in p._issueList ]
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

    @property
    def summaryMap(self):
        #type: () -> Dict[Level, int]
        """
        A map that give for each level the
        number of corresponding issues at that level.
        This include levels with 0 issues.
        """
        map=OrderedDict()
        for l in Levels.Levels:
            n=len(self.select(level=l))
            map[l]=n
        return map


    @property
    def summaryLine(self):

        def times(n, word, pattern='%i %s'):
            if n==0:
                return ''
            else:
                return (pattern % (
                    n,
                    word + ('s' if n>=2 else '')
                ))

        if self.nb==0:
            return ''
        level_msgs=[]
        m=self.summaryMap
        for l in m:
            n=m[l]
            if n>0:
                level_msgs.append(
                    times(n, l.label))
        if len(level_msgs)==1:
            return Annotations.prefix+level_msgs[0]
        else:
            return (
                Annotations.prefix+'%s (%s)' % (
                    times(self.nb, 'Issue'),
                    ', '.join(level_msgs)
                )
            )



    def str(self, level=None, op='=', mode='fragment',
            summary=True):
        header=self.summaryLine if summary else ''
        return '\n'.join(
            [header]
            + [
                i.str(mode=mode)
                for i in self.select(level,op)])

    def __str__(self):
        return self.str()


class WithIssueList(object):
    def __init__(self, parents=()):
        #type: (List[IssueBox]) -> None
        assert(isinstance(parents, list))
        self.issueBox=IssueBox(parents=parents)

    @property
    def isValid(self):
        # () -> bool
        return self.issueBox.isValid

    @property
    def hasIssues(self):
        return self.issueBox.hasIssues

    def addIssue(self, sourceError):
        self.issueBox._add(sourceError)
