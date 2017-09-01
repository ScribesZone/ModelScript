# coding=utf-8

from abc import (
    abstractproperty,
    ABCMeta
)
from typing import Optional, Text
from modelscripts.sources.sources import (
    SourceElement,
    SourceFile,
    IssueList,
    WithIssueList
)

class Model(SourceElement, WithIssueList):
    __metaclass__ = ABCMeta

    def __init__(self,
                 source=None,
                 name=None,
                 code=None,
                 lineNo=None,
                 docComment=None,
                 eolComment=None):
        #type: (Optional[SourceFile], Optional[Text], Optional[Text], Optional[int], Optional[Text], Optional[Text]) -> None
        SourceElement.__init__(self,
            name=name, code=code, lineNo=lineNo,
            docComment=docComment, eolComment=eolComment)
        WithIssueList.__init__(
            self,
            parent=(None if source is None else source))
        self.source=source  #type: Optional[SourceFile]
        self.issues=IssueList() #type: IssueList
