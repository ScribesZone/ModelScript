# coding=utf-8

from abc import ABCMeta
from modelscribes.base.sources import SourceElement

__all__=(
    'ModelElement',
    'SourceModelElement'
)

class ModelElement(object):

    def __init__(self):
        self.stereotypes=[]
        self.tags=[]
        from modelscribes.metamodels.textblocks import (
            TextBlock
        )
        self.description=TextBlock(
            container=self)


class SourceModelElement(ModelElement, SourceElement):
    __metaclass__ = ABCMeta

    def __init__(self,
                 name=None,
                 code=None,
                 lineNo=None,
                 docComment=None,
                 eolComment=None):
        SourceElement.__init__(self,
            name = name,
            code = code,
            lineNo = lineNo,
            docComment = docComment,
            eolComment = eolComment)
        ModelElement.__init__(self)

