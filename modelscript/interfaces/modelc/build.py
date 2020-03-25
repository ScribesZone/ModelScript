# coding=utf-8
import argparse
import os
import sys
import traceback
from typing import List, Text, Dict, Optional
from collections import OrderedDict

# initialize the megamodel with metamodels and scripts

from modelscript.base.files import filesInTree
from modelscript.libs.termcolor import cprint
from modelscript.base.modelprinters import ModelPrinterConfig
from modelscript.interfaces.modelc.options import getOptions
from modelscript.megamodels import Megamodel
from modelscript.base.issues import WithIssueList, OrderedIssueBoxList


class BuildContext(WithIssueList):

    def __init__(self, args):
        super(BuildContext, self).__init__()

        self.args=args
        # The list of command line arguments

        self.options=getOptions(args)
        # The options derived from args

        # self.hasManySourceFiles=len(self.options.sources)>=2

        self.sourceMap=OrderedDict()
        #type: Dict[Text, Optional['SourceFile']]
        # For each source file name, the corresponding SourceFile
        # or None if there was an error

        self._build()

        self.issueBoxList=OrderedIssueBoxList(
            self.allSourceFileList
            +[self])

    def _displayVersion(self):
        print(('ModelScript - version %s' % Megamodel.model.version))

    def _processSource(self, path):
        if os.path.isdir(path):
            extensions=Megamodel.model.metamodelExtensions()
            filenames=filesInTree(path, suffix=extensions)
            if self.options.verbose:
                print(('%s/  %i model files found.'
                      % (path, len(filenames))))
                print(('    '+'\n    '.join(filenames)))
            for filename in filenames:
                self._processSource(filename)
        else:
            source = Megamodel.loadFile(path, self)
            self.sourceMap[path]=source

    def _build(self):

        #--- deal with --version ------------------------------------------
        if self.options.version:
            self._displayVersion()

        #--- deal with --mode ---------------------------------------------
        print((
            {'justAST':'Checking syntax',
             'justASTDep':'Checking syntax and dependencies',
             'full':'Checking models'}
            [self.options.mode] ))
        Megamodel.analysisLevel=self.options.mode

        #--- deal with source files or source dir
        for path in self.options.sources:
            self._processSource(path)

    @property
    def validSourceFiles(self):
        return (
            s for s in list(self.sourceMap.values())
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
        print((self.issueBoxList.str(styled=styled)))
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
