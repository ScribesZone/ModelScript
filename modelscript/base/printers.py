# coding=utf-8
"""
Base classes for printers and string/color utilities.
"""


from abc import ABCMeta, abstractmethod

from typing import Text, Optional
import codecs

from modelscript.base.styles import Styles
from modelscript.base.exceptions import (
    MethodToBeDefined,
    UnexpectedCase)
#----------------------------------------------------------------------------
#    Strings
#----------------------------------------------------------------------------


def indent(prefix, s, suffix='', firstPrefix=None):
    """
    Indent a possibily multiline string (s) with a
    given "prefix". If "firstPrefix" is specified then
    it is used for the first line.
    A "suffix" can also be provided.
    """
    #type: (Text, Text, Text, Optional[Text]) -> Text
    prefix1=prefix if firstPrefix is None else firstPrefix
    lines=s.split('\n')
    outLines=[prefix1+lines[0]+suffix]
    outLines.extend([prefix+l+suffix for l in lines[1:]])
    return '\n'.join(outLines)

# TODO:4 add support for multines
# TODO:4 improve with surronding lines with padding
def box(s,
        length=80, hline='N',
        fill='*', padding='', around=' ',
        align='C',   ):
    """
    Add a box or a line around a given string.
    """
    if align=='C':
        body=(around+s+around).center(length, fill)
    elif align=='R':
        body=(s+around).ljust(length, fill)
    elif align=='L':
        body=(around+s).rjust(length, fill)
    else:
        raise UnexpectedCase( #raise:OK
            'no alignment mode: "%s"' % align)
    mainline=padding+body+padding
    borderline=padding+fill*length+padding
    if hline=='N':
        return mainline
    elif hline=='T':
        return borderline+'\n'+mainline
    elif hline=='D':
        return borderline+'\n'+mainline
    elif hline=='B':
        return borderline+'\n'+mainline+'\n'+borderline
    return padding+body+padding


#----------------------------------------------------------------------------
#    Abstract printers
#----------------------------------------------------------------------------

class AbstractPrinterConfig(object):
    def __init__(self,
                 styled=True,
                 width=120,
                 baseIndent=0,
                 displayLineNos=True,
                 lineNoPadding=' ',
                 verbose=0,
                 quiet=True,
                ):
        self.styled=styled
        self.width=width
        self.baseIndent=baseIndent
        self.displayLineNos=displayLineNos
        self.lineNoPadding=lineNoPadding
        self.verbose=verbose
        self.quiet=quiet


class AbstractPrinterConfigs(object):
    default=AbstractPrinterConfig()
    

class AbstractPrinter(object, metaclass=ABCMeta):
    def __init__(self, config=None):
        #type: (Optional[AbstractPrinterConfig]) -> None
        if config is None:
            config=AbstractPrinterConfigs.default
        self.config=config
        self._baseIndent=config.baseIndent
        self.currentLineNoDisplay=True
        self.output = ''
        # self.eolAtEOF=eolAtEOF

    @property
    def currentLineNo(self):
        return self.output.count('\n')+1

    def kwd(self, text):
        if text=='':  # necessary, otherwise style go to next string
            return ''
        else:
            return Styles.keyword.do(
                text,
                styled=self.config.styled
            )

    def cmt(self, text):
        if text=='':  # necessary, otherwise style go to next string
            return ''
        else:
            return Styles.comment.do(
                text,
                styled=self.config.styled
            )

    def ann(self, text):
        if text=='':  # necessary, otherwise style go to next string
            return ''
        else:
            return Styles.annotate.do(
                text,
                styled=self.config.styled
            )

    def indent(self, n=1):
        self._baseIndent+=n

    def out(self, s, indent=0, style=None):
        if self.config.styled and style is not None:
            s=style.do(s)
        self.output += '%s%s' % (self._indentPrefix(indent), s)
        return self.output

    def outLine(self,
                s,
                lineNo=None,
                suffix='\n',
                prefix='',
                linesBefore=0,
                linesAfter=0,
                indent=0,
                increaseLineNo=False,
                style=Styles.no,
                ):
        if linesBefore >= 1:
            for i in range(linesBefore):
                self.outLine('', style=style)
        # string with multilines should be processed line by line
        lines = s.split('\n')
        current_line_no=lineNo
        for (index, line) in enumerate(lines):
            if lineNo is not None:
                if increaseLineNo:
                    current_line_no += lineNo+index
            self.out(self.lineNoString(lineNo=current_line_no))
            if self.config.styled:
                self.out('%s%s%s' % (
                    self._indentPrefix(indent),
                    prefix,
                    style.do(line)) )
            else:
                self.out('%s%s%s' % (
                    self._indentPrefix(indent),
                    prefix,
                    line) )

            if suffix is not None:
                self.out(suffix)

        if linesAfter >= 1:
            for i in range(linesAfter):
                self.outLine('')
        return self.output

    def _indentPrefix(self, indent=0):
        return ' '*4*(self._baseIndent+indent)

    def lineNoString(self, lineNo=None):
        """
        Can be overloaded
        """
        if (not self.currentLineNoDisplay
            or not self.config.displayLineNos):
            return ''
        if lineNo is not None:
            s='% 4i|' % lineNo
        else:
            s=(self.config.lineNoPadding * 4) + '|'
        return self.cmt(s)
    
    @abstractmethod
    def do(self):
        raise MethodToBeDefined() #raise:OK

    def display(self, removeLastEOL=False, addLastEOL=True):
        text=self.do()
        endsWithEOL=text.endswith('\n')
        if removeLastEOL and endsWithEOL:
            text=text[:-1]
        if addLastEOL and not endsWithEOL:
            text=text+'\n'
        print(text, end='')

    def save(self, output):
        with codecs.open(output, "w", "utf-8") as f:
            f.write(self.output)


class StructuredPrinterConfig(AbstractPrinterConfig):
    def __init__(self,
                 styled=True,
                 width=120,
                 baseIndent=0,
                 displayLineNos=True,
                 lineNoPadding=' ',
                 verbose=0,
                 quiet=False,
                 #------------------------
                 title=None,
                 issuesMode='top'
                ):
        super(StructuredPrinterConfig, self).__init__(
            styled=styled,
            width=width,
            baseIndent=baseIndent,
            displayLineNos=displayLineNos,
            lineNoPadding=lineNoPadding,
            verbose=verbose,
            quiet=quiet)
        self.title = title
        self.issuesMode = issuesMode


class StructuredPrinterConfigs(object):
    default=StructuredPrinterConfig()


class StructuredPrinter(AbstractPrinter, metaclass=ABCMeta):
    """
    A printer with different predefined zones
    (top, body, bottom) with predefined nested zone
    for issues. Each zone corresponds to a method doXXX()
    
        doTop
            doTopTitle
            doIssueSummary
            doIssues         if issueMode='top'
            doTopInner

        doBody

        doBottom
            doBottomInner
            doIssues         if issueMode='bottom'
            doIssueSummary
            doBottomTitle
    """

    def __init__(self,
                 config=None):
        #type: (Optional[StructuredPrinterConfig]) -> None
        if config is None:
            config=StructuredPrinterConfigs.default
        super(StructuredPrinter, self).__init__(
            config=config
        )
        self.config=config #type: StructuredPrinterConfig
        self.issueBox=self.getIssueBox()


    @abstractmethod
    def getIssueBox(self):
        #type: () -> 'IssueBox'
        """
        This method must be implemented.
        """
        pass


    def do(self):
        """
        Can be overloaded
        """
        self.doTop()
        self.doBody()
        self.doBottom()
        return self.output

    #---- top ---------------------------------------------------

    def doTop(self):
        """
        Can be overloaded
        """
        self.currentLineNoDisplay=False
        if self.config.title is not None:
            self.doTopTitle()
        if self.hasIssues and not self.config.quiet:
            self.doIssuesSummary()
        if self.config.issuesMode=='top':
            self.doIssues()
        self.doTopInner()
        return self.output

    def doTopInner(self):
        pass


    def doTopTitle(self):
        """
        Can be overloaded
        """
        if not self.config.quiet:
            self.outLine(box(self.config.title))
        return self.output

    #---- body ---------------------------------------------------

    @abstractmethod
    def doBody(self):
        self.currentLineNoDisplay=True
        return self.output

    # def doSummary(self):
    #     return self.output


    #---- bottom --------------------------------------------------

    def doBottom(self):
        """
        Can be overloaded
        """
        self.currentLineNoDisplay=False
        self.doBottomInner()
        if self.config.issuesMode=='bottom':
            self.doIssues()
        self.doIssuesSummary()
        if self.config.title is not None:
            self.doBottomTitle()
        return self.output

    def doBottomInner(self):
        """
        Can be overloaded
        """
        pass

    def doBottomTitle(self):
        if not self.config.quiet:
            self.outLine(box('end of '+self.config.title))
        return self.output

    #---- bottom --------------------------------------------------

    @property
    def hasIssues(self):
        return (
            self.issueBox is not None
            and self.issueBox.hasIssues)

    # def doIssuesTop(self):
    #     """
    #     Can be overloaded
    #     """
    #     self.doIssuesSummary()
    #     unlocalized_issues = self.issueBox.at(0)
    #     self.doUnlocalizedIssues(unlocalized_issues)
    #     return self.output

    def doIssuesSummary(self):
        """
        Can be overloaded
        """
        s = self.issueBox.summaryLine
        if s != '':
            if self.config.styled:
                if self.issueBox.hasBigIssues:
                    s = Styles.bigIssue.do(
                        s,
                        styled=self.config.styled)
                else:
                    s = Styles.mediumIssue.do(
                        s,
                        styled=self.config.styled)
            self.outLine(s)
        return self.output

    def doIssues(self, line=None,
                 pattern=None): # '{level}: {message}'):
        if line is None:
            issues=self.issueBox.all
        else:
            issues=self.issueBox.at(line)
        for i in issues:
            self.outLine(
                i.str(
                    # pattern=pattern,
                    styled=self.config.styled))
        return self.output


class ContentPrinterConfig(StructuredPrinterConfig):
    def __init__(self,
                 styled=True,
                 width=120,
                 baseIndent=0,
                 displayLineNos=True,
                 lineNoPadding=' ',
                 verbose=0,
                 quiet=False,
                 #------------------------
                 title=None,
                 issuesMode='top',
                 #------------------------
                 contentMode='self', # self|source|model|no
                 summaryMode='top', # top | down | no
                ):
        super(ContentPrinterConfig, self).__init__(
            styled=styled,
            width=width,
            baseIndent=baseIndent,
            displayLineNos=displayLineNos,
            lineNoPadding=lineNoPadding,
            verbose=verbose,
            quiet=quiet,
            title=title,
            issuesMode=issuesMode)
        self.contentMode = contentMode
        self.summaryMode = summaryMode


class ContentPrinterConfigs(object):
    default=ContentPrinterConfig()


class ContentPrinter(StructuredPrinter, metaclass=ABCMeta):
    def __init__(self,
                 config=None):
        #type: (Optional[ContentPrinterConfig]) -> None
        if config is None:
            config=ContentPrinterConfigs.default
        super(ContentPrinter, self).__init__(
            config=config
        )
        self.config=config #type: ContentPrinterConfig
        # self.displayContent=displayContent
        # self.preferStructuredContent=preferStructuredContent
        # self.displaySummary=displaySummary
        # self.summaryFirst=summaryFirst

    def doBody(self):
        super(ContentPrinter,self).doBody()
        if self.config.summaryMode=='top':
            self.doSummaryZone()
        if self.config.contentMode!='no':
            self.doContent()
        if  self.config.summaryMode=='bottom':
            self.doSummaryZone()
        return self.output

    def doSummaryZone(self):
        self.currentLineNoDisplay=False
        sep_line= Styles.comment.do(
                    # '---- Summary '+'-'*67,
                    '-'*80,
                    styled=self.config.styled)
        if self.config.summaryMode=='bottom' and self.config.contentMode!='no':
            self.outLine(sep_line)
        self.doSummary()
        if self.config.summaryMode=='top' and self.config.contentMode!='no':
            self.outLine(sep_line)
        return self.output

    def doSummary(self):
        return self.output

    def doContent(self,):
        self.currentLineNoDisplay=True
        return self.output