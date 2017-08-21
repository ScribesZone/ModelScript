# coding=utf-8

from __future__ import print_function

from modelscripts.use.use.parser import UseSource


class ClassModelSource(UseSource):

    def __init__(self, classModelSourceFile):
        super(ClassModelSource, self).__init__(classModelSourceFile)