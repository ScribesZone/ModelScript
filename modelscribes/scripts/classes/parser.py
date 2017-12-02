# coding=utf-8

from __future__ import print_function



from modelscribes.use.use.parser import UseModelSource
from modelscribes.metamodels.classes import METAMODEL
from modelscribes.scripts.classes.preprocessor import (
    ClsToUsePreprocessor
)



class ClassModelSource(UseModelSource):

    def __init__(self, originalFileName):
        super(ClassModelSource, self).__init__(
            originalFileName,
            preprocessor=ClsToUsePreprocessor())

    @property
    def metamodel(self):
        return METAMODEL

METAMODEL.registerSource(ClassModelSource)