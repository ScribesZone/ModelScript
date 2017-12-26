# coding=utf-8

from __future__ import print_function



from modelscripts.use.use.parser import UseModelSource
from modelscripts.metamodels.classes import METAMODEL
from modelscripts.scripts.classes.preprocessor import (
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