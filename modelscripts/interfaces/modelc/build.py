# coding=utf-8
import argparse
import os
import sys
import traceback
from typing import List, Text, Dict, Optional
from collections import OrderedDict

# initialize the megamodel with metamodels and scripts

from modelscripts.libs.termcolor import cprint
from modelscripts.base.modelprinters import ModelPrinterConfig
from modelscripts.interfaces.modelc.options import getOptions
from modelscripts.megamodels import Megamodel
from modelscripts.base.issues import WithIssueList, OrderedIssueBoxList


class BuildContext(WithIssueList):

    def __init__(self, args):
        super(BuildContext, self).__init__()
        self.args=args
        self.options=getOptions(args)
        self.hasManySourceFiles=len(self.options.sources)>=2
        self.sourceMap=OrderedDict()
        self._build()
        self.issueBoxList=OrderedIssueBoxList(
            self.allSourceFileList
            +[self])
        #type: Dict[Text, Optional['SourceFile']]
        # for each source file name, the corresponding SourceFile
        # or None if there was an error

    def _build(self):
        for filename in self.options.sources:
            source = Megamodel.loadFile(filename, self)
            self.sourceMap[filename]=source


    @property
    def validSourceFiles(self):
        return (
            s for s in self.sourceMap.values()
            if s is not None)

    @property
    def nbIssues(self):
        return self.issueBoxList.nbIssues

    @property
    def allSourceFileList(self):
        """
        The list of all source files involved in this build,
        directly or not. The list is in a topological order.
        """
        return Megamodel.sourceFileList(
            origins=self.validSourceFiles)

    def label(self):
        return('buildContext')


    def display(self, styled=True):
        # print(self.issueBoxList.nbIssues)
        print(self.issueBoxList.str(styled=styled))
        # displayIssueBoxContainers(
        #     self.allSourceFileList+[self]
        # )
        # for source in self.allSourceFileList:
        #     print(source.issues.str(
        #         summary=False,
        #         styled=True,
        #         pattern='{origin}:{level}:{line}:{message}'))
        # if self.hasIssues:
        #     print(self.issues.str(
        #         summary=False,
        #         styled=True,
        #         pattern='{origin}:{level}:{line}:{message}'
        #     ))

# # TODO:3 move this to issue.py
# def displayIssueBoxContainers(containerList):
#     for container in containerList:
#         if container.hasIssues:
#             print(container.issues.str(
#                 summary=False,
#                 styled=True,
#                 pattern='{origin}:{level}:{line}:{message}'))
#         else:
#             if not isinstance(container, BuildContext):
#                 cprint(container.label+':'+'OK', 'green')
