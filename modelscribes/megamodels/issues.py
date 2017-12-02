# coding=utf-8
from typing import Text, Any, Optional

from modelscribes.base.issues import (
    Issue,
    Level
)
from modelscribes.base.annotations import (
    Annotations
)

#TODO:2 The type ModelElement should be better defined
#       Currently classes inherits from SourceElements which
#       is not really appropriate.


class ModelElementIssue(Issue):

    def __init__(self, model, modelElement, level, message):
        #type: ('Model', 'ModelElement', Level, Text) -> None
        self.modelElement=modelElement
        super(ModelElementIssue, self).__init__(
            origin=model,
            level=level,
            message=message)

    def str(self,
            pattern=None,
            mode='fragment',
            styled=False):
        if pattern is None:
            pattern=(   Annotations.prefix
                        +'{kind}:{level}:{message}')
        text= pattern.format(
            message=self.message,
            kind=self.kind,
            level=self.level.str())
        return self.level.style.do(
            text,
            styled=styled,
        )
