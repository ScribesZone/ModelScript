# coding=utf-8
""""""

__all__ = (
    'ExecutionContext'
)

import os
from typing import List, Any, Dict, Optional, ClassVar
from collections import OrderedDict
import argparse

# initialize the megamodel with metamodels and scripts

from modelscript.base.files import filesInTree
from modelscript.interfaces.modelc.options import getOptions
from modelscript.megamodels import Megamodel
from modelscript.base.issues import WithIssueList, OrderedIssueBoxList


class ExecutionContext(WithIssueList):
    """Execution context of modelscript session."""

    args: ClassVar[List[str]]
    """The list of command line arguments"""

    options: argparse.Namespace
    """The options derived from args."""

    sourceMap: ClassVar[Dict[str, Optional['SourceFile']]]
    """For each source file name, the corresponding SourceFile
    or None if there was an error
    """

    issueBoxList: OrderedIssueBoxList

    def __init__(self, args):
        super(ExecutionContext, self).__init__()

        assert args is not None
        # extract the command options from the command line arguments
        self.args = args
        self.options = getOptions(args)
        # self.hasManySourceFiles=len(self.options.sources)>=2
        self.sourceMap = OrderedDict()
        self._execute()
        self.issueBoxList = OrderedIssueBoxList(
            self.allSourceFileList
            + [self])

    def _displayVersion(self):
        print(('ModelScript - version %s' % Megamodel.model.version))

    def _processSource(self, path):
        """Process a given source file or a given directory.
        If a directory is given, then get all source files in
        this directory recursively."""
        if os.path.isdir(path):
            # A directory is given: process all nested source files.
            extensions = Megamodel.model.metamodelExtensions()
            filenames = filesInTree(path, suffix=extensions)
            if self.options.verbose:
                print(('%s/  %i model files found.'
                      % (path, len(filenames))))
                print(('    '+'\n    '.join(filenames)))
            for filename in filenames:
                self._processSource(filename)
        else:
            # Load a given source file
            source = Megamodel.loadFile(path, self)
            self.sourceMap[path] = source

    def _execute(self):

        # --- deal with --version -----------------------------------------
        if self.options.version:
            self._displayVersion()

        # --- deal with --mode --------------------------------------------
        print((
            {'justAST': 'Checking syntax',
             'justASTDep': 'Checking syntax and dependencies',
             'full': 'Checking models'}
            [self.options.mode]))
        Megamodel.analysisLevel = self.options.mode

        # --- deal with source files or source dir
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
        return 'executionContext'

    def display(self, styled=True):
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
#             if not isinstance(container, ExecutionContext):
#                 cprint(container.label+':'+'OK', 'green')
