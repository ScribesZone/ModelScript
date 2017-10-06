# coding=utf-8

from __future__ import print_function

from modelscribes.use.use.parser import UseModelSource
from modelscribes.metamodels.classes import METAMODEL


class ClassModelSource(UseModelSource):

    def __init__(self, classModelSourceFile):
        super(ClassModelSource, self).__init__(classModelSourceFile)

    @property
    def metamodel(self):
        return METAMODEL

METAMODEL.registerSource(ClassModelSource)