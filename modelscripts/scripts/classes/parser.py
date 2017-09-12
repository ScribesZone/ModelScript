# coding=utf-8

from __future__ import print_function

from modelscripts.use.use.parser import UseSource
from modelscripts.metamodels.classes import metamodel


class ClassModelSource(UseSource):

    def __init__(self, classModelSourceFile):
        super(ClassModelSource, self).__init__(classModelSourceFile)

metamodel.registerSource(ClassModelSource)