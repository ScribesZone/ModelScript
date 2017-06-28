# coding=utf-8
from typing import List, Optional
import pyuseocl.model
import pyuseocl.utils.sources

class UseOCLModelFile(pyuseocl.utils.sources.SourceFile):

    def __init__(self, useModelSourceFile : str) -> str :
        self.commandExitCode : int
        self.isValid : bool
        self.canonicalLines : Optional(List[str])
        self.canonicalLength : Optional(int)
        self.errors: List[str]
        self.model : Optional[pyuseocl.model.Model]


    def saveCanonicalModelFile(self, fileName : Optional[str]): str
