# coding=utf-8
from typing import Text, List, Any, Optional
from abc import ABCMeta

from modelscripts.base.issues import (
    Issue,
    LocalizedSourceIssue,
    Level,
    WithIssueList,
    IssueBox
)
import re
from modelscripts.base.annotations import (
    Annotations
)
DEBUG=0

#TODO:2 The type ModelElement should be better defined
#       Currently classes inherits from SourceElements which
#       is not really appropriate.



class ModelElementIssue(Issue):

    def __init__(self,
                 modelElement,
                 level,
                 message,
                 code=None,
                 locationElement=None):
        #type: ('ModelElement', Level, Text, 'ModelElement') -> None
        self.modelElement=modelElement #type: 'ModelElement'
        self.locationElement=(
            locationElement if locationElement is not None
            else modelElement)
        if DEBUG>=2:
            print('ISM: %s ' % self.locationElement)
        #type: 'ModelElement'
        if hasattr(self.locationElement, 'lineNo'):
            line_no=self.locationElement.lineNo
        else:
            line_no=None
        if line_no is None:
            if DEBUG>=1:
                print('ISM: Unlocated Model Issue %s' % message)
            issue=Issue(
                origin=modelElement.model,
                code=code,
                level=level,
                message=message)
        else:
            if DEBUG>=1:
                print('ISM: Localized Model Issue at %s %s' % (
                    line_no,
                    message))
            issue=LocalizedSourceIssue(
                code=code,
                sourceFile=self.locationElement.model.source,
                level=level,
                message=message,
                line=line_no,
            )
        self.actualIssue=issue

    @property
    def origin(self):
        return self.actualIssue.origin

    @property
    def message(self):
        return self.actualIssue.message

    @property
    def level(self):
        return self.actualIssue.level

    @property
    def origin(self):
        return self.actualIssue.level


    def str(self,
            pattern=None,
            styled=False):  # not used, but in subclasses
        return self.actualIssue.str(
            pattern=pattern,
            styled=styled)

    # def str(self,
    #         pattern=None,
    #         displayOrigin=False,
    #         displayLocation=True,
    #         styled=False):
    #     if pattern is None:
    #         pattern=(   Annotations.prefix
    #                     +'{origin}:{kind}:{level}:{location}:{message}')
    #     text= pattern.format(
    #         origin=self.origin.label,
    #         message=self.message,
    #         kind=self.kind,
    #         level=self.level.str(),
    #         location='?')
    #     return self.level.style.do(
    #         text,
    #         styled=styled,
    #     )


class WithIssueModel(WithIssueList):
    __metaclass__ = ABCMeta

    def __init__(self, parents=()):
        #type: (List[IssueBox]) -> None
        super(WithIssueModel, self).__init__(parents=parents)
        from modelscripts.megamodels import Megamodel
        Megamodel.registerIssueBox(self._issueBox)