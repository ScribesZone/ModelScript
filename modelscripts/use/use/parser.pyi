# coding=utf-8
from typing import List, Optional
import pyuseocl.metamodel.classes
import pyuseocl.source.sources

class UseSource(pyuseocl.source.sources.SourceFile):

    def __init__(self, useModelSourceFile : str) -> str :
        self.commandExitCode : int
        self.isValid : bool
        self.canonicalLines : Optional(List[str])
        self.canonicalLength : Optional(int)
        self.errors: List[str]
        self.classModel : Optional[pyuseocl.metamodel.classes.ClassModel]


    def saveCanonicalModelFile(self, fileName : Optional[str]): str
