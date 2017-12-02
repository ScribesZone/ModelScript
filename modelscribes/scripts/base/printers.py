# coding=utf-8
"""
Base classes for printers and string/color utilities.
"""
from __future__ import unicode_literals, print_function, absolute_import, division
from abc import ABCMeta
from typing import Optional

from modelscribes.base.printers import (
    ContentPrinter,
    ContentPrinterConfig,
    Styles
)

# class AbstractModelOrModelSourcePrinter(AbstractPrinter):
#     def __init__(self,
#                  modelOrModelSource,
#                  fullContent=True,
#                  summary=False,
#                  abstractBody=True,
#                  config=BasicPrinterConfigs.default):
#         assert modelOrModelSource is not None
#         self.modelOrModelSource = modelOrModelSource
#         super(AbstractModelOrModelSourcePrinter, self).__init__(
#             fullContent=fullContent,
#             summary=summary,
#             config=config
#         )
#         self.abstractBody = abstractBody
#
#     @property
#     def isModelSource(self):
#         return isinstance(
#             self.modelOrModelSource,
#             ModelSourceFile)
#
#     @property
#     def theModelSource(self):
#         if self.isModelSource:
#             return self
#
#
#     @property
#     def theModel(self):
#         if model
#
#
#     xxx terminate this
#
#     doBody
#         --> instanciate either de model printer or source printer and call its doBody

class ModelPrinter(ContentPrinter):
    __metaclass__ = ABCMeta

    def __init__(self,
                 theModel,
                 config=None):
        #type: ('Model', Optional[ContentPrinterConfig]) -> None
        assert theModel is not None
        # don't move this line after as getIssueBox
        # is used in __init__
        self.theModel = theModel

        # TODO: use abstractView parameter
        super(ModelPrinter, self).__init__(
            config=config,
        )

    def getIssueBox(self):
        return self.theModel.issues


    def doContent(self):
        if (not self.config.contentMode=='model'
            and self.theModel.source is not None):
            self.doSourceContent()
        else:
            self.doModelContent()
        return self.output

    def doSourceContent(self):
        #FIXME: the called method is not defined

        self.out(self.theModel.source.str(
            method='doSourceContent',
            displayContent=True,
            preferStructuredContent=False,
            displaySummary=self.config.summaryMode!='no',
            summaryFirst=self.config.summaryMode=='top',
            config=self.config
        ))
        return self.output

    def doModelContent(self):
        return self.output


class ModelSourcePrinter(ContentPrinter):
    __metaclass__ = ABCMeta

    def __init__(self,
                 theSource,
                 config=None):
        #type: ('ModelSourceFile', Optional[ContentPrinterConfig]) -> None
        assert theSource is not None

        # don't move this line after as getIssueBox
        # is used in __init__
        self.theSource = theSource  # don't move
        super(ModelSourcePrinter, self).__init__(
            config=config,
        )

    def getIssueBox(self):
        return self.theSource.fullIssueBox


    def doContent(self):
        if (self.config.contentMode=='model'
            and self.theSource.model is not None):
            self.doModelContent()
        else:
            self.doSourceContent()
        return self.output

    def doModelContent(self):
        # call the str method of the model
        self.out(self.theSource.model.str(
            method='doModelContent',
            displayContent=True,
            preferStructuredContent=True,
            displaySummary=self.config.summaryMode!='no',
            summaryFirst=self.config.summaryMode=='top',
            config=self.config
        ))
        return self.output

    def doSourceContent(self):
        # display issues with no location included
        self.currentLineNoDisplay=False
        if self.config.issuesMode == 'inline':
            self.doIssues(line=0)
        # display each line of the source
        for (index, line) in enumerate(self.theSource.sourceLines):
            line_no = index + 1
            self.currentLineNoDisplay = True
            self.outLine(line, lineNo=line_no)
            if self.config.issuesMode=='inline':
                self.currentLineNoDisplay = False
                self.doIssues(line=line_no)
        if self.config.issuesMode == 'inline':
            self.currentLineNoDisplay = False
            self.doIssues(
                line=len(self.theSource.sourceLines)+1)
        return self.output

    def doSummary(self):
        super(ModelSourcePrinter, self).doSummary()
        self.out(
            Styles.comment.do(
                str(self.theSource.fullMetrics),
                self.config.styled)
        )
        return self.output

# class AnnotatedSourcePrinter(SourcePrinter):
#     def __init__(self,
#                  theSource):
#         # type: ('Source') -> None
#
#         assert theSource is not None
#         super(AnnotatedSourcePrinter, self).__init__(
#             theSource=theSource,
#             summary=False,
#             displayLineNos=False,
#         )
#
#     def do(self):
#         self.output = ''
#
#         self._issueHeader()
#
#         for (index, line) in enumerate(self.theSource.sourceLines):
#             line_no = index + 1
#             # self.out(str(line_no))
#             self.out(line_no, line)
#             localized_issues = self.theSource.fullIssueBox.at(line_no)
#             if localized_issues:
#                 self._localizedIssues(localized_issues)
#         return self.output
#
#         # def _issueHeader(self):
#         #     self._issuesSummary(self.theSource.fullIssueBox)
#         #     unlocalized_issues=self.theSource.fullIssueBox.at(0)
#         #     self._unlocalizedIssues(unlocalized_issues)
#         #
#         # def _line(self, line_no, line):
#         #     self.outLine(line)
#         #
#         # def _issuesSummary(self, issues):
#         #     s=issues.summaryLine
#         #     if s!='':
#         #         self.outLine(issues.summaryLine)
#         #
#         # def _unlocalizedIssues(self, issues, pattern='{level}: {message}'):
#         #     for i in issues:
#         #         self.outLine(
#         #             i.str(pattern=pattern))
#         #
#         # def _localizedIssues(self, issues, pattern='{level}: {message}'):
#         #     for i in issues:
#         #         self.outLine(
#         #             i.str(pattern=pattern,
