# coding=utf-8

from __future__ import unicode_literals, print_function, absolute_import, division

from modelscripts.use.sex.parser import (
    SoilSource
)


class ObjectModelSource(SoilSource):

    def __init__(self, filename, classModel):
        super(ObjectModelSource, self).__init__(
            classModel=classModel,
            soilFilename=filename,
            usecaseModel=None,
        )
