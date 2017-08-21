# coding=utf-8

from modelscripts.source.sources import SourceElement

class Model(SourceElement):

    def __init__(self,
                 source,
                 name=None,
                 code=None,
                 lineNo=None,
                 docComment=None,
                 eolComment=None):
        super(Model, self).__init__(
            name=name, code=code, lineNo=lineNo,
            docComment=docComment, eolComment=eolComment)
        self.source=source