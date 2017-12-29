# coding=utf-8
from typing import Text, List, Any, Optional
from abc import ABCMeta

from modelscripts.base.issues import (
    Issue,
    Level,
    WithIssueList,
    IssueBox
)
from modelscripts.base.annotations import (
    Annotations
)


#TODO:2 The type ModelElement should be better defined
#       Currently classes inherits from SourceElements which
#       is not really appropriate.


class ModelElementIssue(Issue):

    def __init__(self, modelElement, level, message):
        #type: ('Model', 'ModelElement', Level, Text) -> None
        self.modelElement=modelElement
        super(ModelElementIssue, self).__init__(
            origin=modelElement.model,
            level=level,
            message=message)

    def str(self,
            pattern=None,
            displayOrigin=False,
            displayLocation=True,
            styled=False):
        if pattern is None:
            pattern=(   Annotations.prefix
                        +'{origin}:{kind}:{level}:{location}:{message}')
        text= pattern.format(
            origin=self.origin.label,
            message=self.message,
            kind=self.kind,
            level=self.level.str(),
            location='?')
        return self.level.style.do(
            text,
            styled=styled,
        )


class WithIssueModel(WithIssueList):
    __metaclass__ = ABCMeta

    def __init__(self, parents=()):
        #type: (List[IssueBox]) -> None
        super(WithIssueModel, self).__init__(parents=parents)
        from modelscripts.megamodels import Megamodel
        Megamodel.registerIssueBox(self._issueBox)