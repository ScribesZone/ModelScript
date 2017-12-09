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
            displayOrigin=False,
            displayLocation=True,
            styled=False):
        if pattern is None:
            pattern=(   Annotations.prefix
                        +'{origin}:{kind}:{level}:{location}:{message}')
        text= pattern.format(
            origin='ORIGIN',
            message=self.message,
            kind=self.kind,
            level=self.level.str(),
            location='LOCAITON')
        return self.level.style.do(
            text,
            styled=styled,
        )
