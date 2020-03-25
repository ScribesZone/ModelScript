# coding=utf-8

"""
Model errors in source files either localized or not.
"""
from abc import ABCMeta, abstractproperty
from collections import OrderedDict
from typing import Optional, List, Text, Dict, Tuple, Any, Union

from modelscript.base.annotations import (
    Annotations
)
from modelscript.base.locations import (
    SourceLocation,
)
# TODO:4 it should be better to remove the printer dependency
from modelscript.base.styles import Styles
#from modelscript.config import Config
from modelscript.base.exceptions import (
    UnexpectedCase,
    MethodToBeDefined)

DEBUG=0


class FatalError(Exception):
    def __init__(self, SourceError):
        super(FatalError, self).__init__()
        self.sourceError=SourceError


class Level(object):
    def __init__(self, label, rank, style):
        self.label=label
        self.rank=rank
        self.style=style

    @property
    def code(self):
        return self.label[0]

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
            raise UnexpectedCase(  #raise:OK
                'Operation %s is not allowed'%op)

    def str(self, styled=False):
        return self.style.do(self.label, styled=styled)

    def __str__(self):
        return self.label

    def __repr__(self):
        return self.__str__()


class Levels(object):
    OK=Level('OK', 00, Styles.smallIssue)
    Hint=Level('HINT', 10, Styles.smallIssue)
    Info=Level('INFO', 20, Styles.smallIssue)
    Warning=Level('WARNING', 30, Styles.mediumIssue)
    Error=Level('ERROR', 40, Styles.bigIssue)
    Fatal=Level('FATAL', 50, Styles.bigIssue)
    System=Level('SYSTEM ERROR', 60, Styles.bigIssue)

    Levels=[System, Fatal, Error, Warning, Info, Hint]

    @classmethod
    def fromCode(cls, code):
        """
        Return the level corresponding to a code
        or None if the code is not a label.
        """
        for level in Levels.Levels:
            if level.code==code:
                return level
        return None


class Issue(object):
    """
    An issue in a given entity with issue list (WithIssueList).
    Direct instances of Issue are not localized.
    The class LocalizedSourceIssue must be used instead
    if the error line is known.
    """
    def __init__(self,
                 origin,
                 level,
                 message,
                 code=None):
        #type: (WithIssueList, Level, 'Text', Optional['Text']) -> None
        """
        Create a source error and add it to the given OldSourceFile.
        Raise FatalError if the error is fatal and processing could not
        continue.
        """
        assert message is not None and message!=''

        self.code=code

        self.origin = origin  #type: WithIssueList
        """ A source file or a model or a context. """

        self.message = message
        """ The issue message. """

        self.level=level  #type:Level

        self.origin._issueBox._add(self)

        if DEBUG>=1:
            print('ISS: ****NEW %s%s IN %s **** -> %s'  % (
                type(self).__name__,
                '' if self.code is None else ':'+self.code,
                self.origin._issueBox.label,
                unicode(self)
            ))

        if level==Levels.Fatal:
            # Raise a real exception for Fatal issue so that
            # the execution stop immediatly
            raise FatalError(self) #raise:OK

    @property
    def fromModel(self):
        """
        Indicates if the issue comes from a model.
        """
        # Since importing the model type generate a cycle,
        # the trick below should be good enough.
        return type(self.origin).__name__.endswith('Model')

    @property
    def kind(self):
        """M for Model, S for source"""
        return 'M' if self.fromModel else 'S'

    @property
    def originLabel(self):
        if hasattr(self.origin, 'source'):
            src=self.origin.source
            if src is not None:
                return src.basename
            else:
                return '-'
        else:
            if hasattr(self.origin, 'basename'):
                return self.origin.basename
            else:
                return '-'


    def str(self,
            pattern=None,
            styled=False,
            prefix=''): # not used, but in subclasses

        """
        Display the issue.
        Since the issue is not localized
        direct instances of this class just display
        the level and the error message.
        Subclasses provide more information
        """
        # l=self.level.style.do(self.level.str(styled=styled))
        # return pattern.format(
        #     message=self.message,
        #     level=l)
        if pattern is None:
            pattern=(
                Annotations.prefix
                + u'{kind}:{level}:{origin}:{message}')
        text=pattern.format(
            origin=self.originLabel,
            level=self.level.str(),
            kind=self.kind,
            location=u'-',
            line='-',
            message=self.message
        )
        return self.level.style.do(
            prefix+text,
            styled=styled)

    def __str__(self):
        return self.str()


    def __repr__(self):
        return self.__str__()


class LocalizedSourceIssue(Issue):

    def __init__(self,
                 sourceFile,
                 level,
                 message,
                 line,
                 code=None,
                 column=None,
                 fileName=None):
        #type: ('SourceFile', Level, Text, int, Optional[Text], Optional[int], Optional[Text]) -> None
        """
        Create a localized source file and add it to
        the given source file.

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
            given, then this value will be taken
            from the source file.
        """

        def __adjust(sourceFile, line, column):
            #type: ('SourceFile', int,int) -> Tuple[int,int]
            lines = sourceFile.sourceLines
            nblines = len(lines)
            if line == 0:
                # move error before first line to first line
                # this could be after the last line if empty
                l = 1
                c = 0
            elif nblines == 0:
                # if no line on the file, line will be 1
                # that is, after the last line
                l = 1
                c = 0
            elif line > nblines:
                # move error after last line to end
                # of last line
                l = nblines
                c = len(lines[nblines - 1])
            else:
                # regular location for a line
                l = line
                c = column
            return(l,c)

        (l, c) = __adjust(sourceFile, line, column)

        self.location=SourceLocation(
            sourceFile=sourceFile,
            fileName=fileName,
            line=l,
            column=c
        )

        # self.sourceFile = sourceFile
        # """ The source file. An instance oOldSourceFilele. """
        #
        # self.fileName = (
        #     fileName if fileName is not None
        #     else self.sourceFile.fileName )
        #
        # #------ ajust line,col if necessary
        # (l,c)=__adjust(self.sourceFile, line, column)
        # lines=sourceFile.sourceLines
        #
        # self.line = l #type: int
        # """
        # The line number between 1 and the nb of lines.
        # This values may have been adjusted
        # """
        #
        # self.column = c #type: Optional[int]
        # """
        # The column number or None. If defined
        # it could be 0 or 1 more than the length
        # of the line
        # """

        super(LocalizedSourceIssue, self).__init__(
            code=code,
            origin=sourceFile,
            level=level,
            message=message)

    @property
    def line(self):
        return self.location.line

    @property
    def column(self):
        return self.location.column

    def str(self,
            pattern=None,
            styled=False,
            prefix = ''):
        if pattern is None:
            pattern=(
                Annotations.prefix
                + u'{kind}:{level}:{origin}:{line}:{message}')
        text=pattern.format(
            origin=self.location.sourceFile.basename,
            level=self.level.str(),
            kind=self.kind,
            line=unicode(self.location.line),
            message=self.message
        )
        return self.level.style.do(
            prefix+text,
            styled=styled)

    def __str__(self):
        return self.str()

    def __repr__(self):
        return self.__str__()


class IssueBox(object):
    """
    A collection of issues for a 'WithIssueList'
    element (so far a Model, a SourceFile or a BuildContext).
    IssueBoxes can be nested following the import graphs.
    Issue boxes also provide some query mechanisms.
    """

    def __init__(self, origin, parents=()):
        #type: (Any, List[IssueBox]) -> None


        self.origin=origin
        #type: Union['SourceFile', 'Model', 'BuildContext']
        """
        The container of the issue box, typically a 
        source file, a model or a build context. 
        The model can be the megamodel.
        """

        self.label='issuebox<%s>' % self.origin.label
        """
        A label for internal display
        """

        self._issueList=[] #type: List[Issue]
        """ 
        The list of issue directly in this box.
        This list is populated by the 'Issue' class.
        """

        self.parents=list(parents) #type:List[IssueBox]
        """
        List of parent issue boxes. These issue of these boxes 
        will appear in this one.
        """

        self._issuesAtLine=OrderedDict()
        #type: Dict[Optional[int], List[Issue]]
        """ 
        Store for a given line the issues at this line.
        There is no  entry for lines without issues.
        _issuesAtLine[0] are for unlocalized issues.
        """

        if DEBUG>=1:
            print(u'ISS: New issue box for %s -> %s' % (
                type(self.origin).__name__,
                self.label))

    def _add(self, issue):
        #type: (Issue) -> None
        # Add an issue to the box.
        # This method is called by the issue constructor.
        self._issueList.append(issue)
        if isinstance(issue, LocalizedSourceIssue):
            index=issue.line
        else:
            index=0
        if index not in self._issuesAtLine:
            self._issuesAtLine[index]=[]
        self._issuesAtLine[index].append(issue)

    def addParent(self, issueBox):
        #type: (IssueBox) -> None
        """
        Add the issue box as the last parents in the list.
        If it is already in the list, do nothing.
        """
        if not issueBox in self.parents:
            self.parents.append(issueBox)
            if DEBUG >= 1:
                print(u'ISS: Add parent "%s" -> "%s"' % (
                        self.label,
                        issueBox.label))

    def at(self, lineNo, parentsFirst=True):
        """
        Return the list of issues at the specified line.
        If the line is 0 then return unlocalized issues.
        Return both local and parents issues recursively.
        """
        # int -> List[Issue]
        parent_issues=[
            i for p in self.parents
                for i in p.at(lineNo, parentsFirst=parentsFirst) ]
        self_issues=(
            [] if lineNo not in self._issuesAtLine
            else self._issuesAtLine[lineNo])
        if parentsFirst:
            return parent_issues+self_issues
        else:
            return self_issues+parent_issues

    @property
    def allParents(self):
        #type: () -> List[IssueBox]
        """
        Return all parents recursively.
        """
        return list(
            x
            for p in self.parents
                for x in p.allParents+[p])

    @property
    def all(self):
        """
        Return both local and parents issues recursively
        """
        return list(
            [ i for p in self.allParents
                    for i in p._issueList ]
            + self._issueList)

    @property
    def nb(self):
        """
        Return the nb of all issues (local and parents)
        """
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
    def hasBigIssues(self):
        return len(self.bigIssues) >= 1

    @property
    def hasSmallIssues(self):
        return

    @property
    def summaryLevelMap(self):
        #type: () -> Dict[Level, int]
        """
        A map that give for each level the
        number of corresponding issues at that level.
        This include levels with 0 issues.
        """
        map = OrderedDict()
        for l in Levels.Levels:
            n = len(self.select(level=l))
            map[l] = n
        return map

    @property
    def summaryCodeMap(self):
        # type: () -> Dict[Level, int]
        """
        A map that give for each level the
        number of corresponding issues at that level.
        This include levels with 0 issues.
        """
        map=OrderedDict()
        for i in self.all:
            if i.code in map:
                map[i.code]+=1
            else:
                map[i.code]=1
        return map

    @property
    def summaryLine(self):

        def times(n, word, pattern=u'%i %s'):
            if n==0:
                return ''
            else:
                return (pattern % (
                    n,
                    word + (u's' if n>=2 else u'')
                ))

        if self.nb==0:
            return u''
        level_msgs=[]
        m=self.summaryLevelMap
        for l in m:
            n=m[l]
            if n>0:
                level_msgs.append(
                    times(n, l.label))
        if len(level_msgs)==1:
            text=level_msgs[0]
        else:
            text= u'%s (%s)' % (
                    times(self.nb, u'Issue'),
                    u', '.join(level_msgs)
                )
        return Annotations.fullLine(text)



    def str(self,
            level=None,
            op='=',
            summary=True,
            pattern=None,
            styled=False,
            annotations=False):
        if not self.hasIssues:
            return ''
        header=(
            (Annotations.full if annotations else '')+'\n'
            +self.summaryLine+'\n'
            +(Annotations.full if annotations else '')
                if summary else '')
        return '\n'.join(filter(None,(
            [header]
            + [
                i.str(
                    styled=styled,
                    pattern=pattern,
                    prefix='')
                for i in self.select(level,op)]
            + [Annotations.full+'\n' if annotations else ''])))

    def __str__(self):
        return self.str()

    def __repr__(self):
        return self.__str__()


class OrderedIssueBoxList(object):
    #TODO:4  refactor to reuse code from IssueBox
    # This class originates from the need to have issues in issue boxes
    # displayed in a topological order (see BuildContext)
    # The code for the number of issues and so on should come from
    # the issue box class with a composite pattern or so.
    # In the meantime the code is added here in a ad hoc manner for
    # the profit of BuildContext.

    def __init__(self, containerList):
        self.containerList=containerList
        self.issueBoxes=[
            container.issues for container in containerList]

    def str(self,
            withOK=False,
            pattern='{origin}:{level}:{line}:{message}',
            styled=True):
        outputs=[]
        for issue_box in self.issueBoxes:
            if issue_box.hasIssues:
                outputs.append((
                    issue_box.str(
                        summary=False,
                        styled=styled,
                        pattern=pattern)))
            else:
                issue_box_kind=issue_box.origin.__class__.__name__
                if issue_box_kind!='BuildContext':
                    outputs.append(
                        Styles.smallIssue.do(
                            issue_box.origin.label + ':' + 'OK',
                            styled=styled))
        return '\n'.join(outputs)

    @property
    def nbIssues(self):
        return sum(box.nb for box in self.issueBoxes)


class WithIssueList(object):
    __metaclass__ = ABCMeta

    def __init__(self, parents=()):
        #type: (List[IssueBox]) -> None
        assert(isinstance(parents, (list, tuple)))
        self._issueBox=IssueBox(
            origin=self,
            parents=parents)

    @property
    def issues(self):
        return self._issueBox

    @abstractproperty
    def label(self):
        raise MethodToBeDefined( #raise:OK
            'ISS: originLabel not defined')

    @property
    def isValid(self):
        # () -> bool
        return self._issueBox.isValid

    @property
    def hasIssues(self):
        return self._issueBox.hasIssues

    @property
    def hasBigIssues(self):
        return self._issueBox.hasBigIssues

    def addIssue(self, sourceError):
        self._issueBox._add(sourceError)

