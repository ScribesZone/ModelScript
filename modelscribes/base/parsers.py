# coding=utf-8
from typing import Text, List, Optional
class DocCommentLines(object):
    def __init__(self):
        self.lines = []

    def add(self, line):
        #type: (Text) -> None
        assert line is not None
        self.lines.append(line)

    def consume(self):
        #type: () -> Optional[List[Text]]
        if len(self.lines)==[]:
            return None
        else:
            _ = self.lines
            self.lines=[]
            return _

    def clean(self):
        self.lines=[]