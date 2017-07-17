# coding=utf-8
from typing import List, Optional
import pyuseocl.metamodel.model
import pyuseocl.source.sources

class UseSource(pyuseocl.source.sources.SourceFile):

    def __init__(self, useModelSourceFile : str) -> str :
        self.commandExitCode : int
        self.isValid : bool
        self.canonicalLines : Optional(List[str])
        self.canonicalLength : Optional(int)
        self.errors: List[str]
        self.model : Optional[pyuseocl.metamodel.model.Model]


    def saveCanonicalModelFile(self, fileName : Optional[str]): str
