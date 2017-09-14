# coding=utf-8

from __future__ import unicode_literals, print_function, absolute_import, division
from modelscribes.metamodels.objects import (
    metamodel
)
from modelscribes.use.sex.parser import (
    SoilSource
)



class ObjectModelSource(SoilSource):  # use sex

    def __init__(self, soilFileName, classModel=None):
        super(ObjectModelSource, self).__init__(
            soilFileName=soilFileName,
            classModel=classModel,
            usecaseModel=None)

    #TODO: implementation to be continued

metamodel.registerSource(ObjectModelSource)
