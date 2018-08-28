# coding=utf-8

from abc import ABCMeta, abstractproperty
from modelscripts.base.exceptions import (
    MethodNotDefined)



MegamodelElement='MegamodelElement'
class Dependency(object):
    __metaclass__ = ABCMeta

    @abstractproperty
    def source(self):
        #type: () -> MegamodelElement
        raise MethodNotDefined( #raise:OK
            'property .source is not implemented')

    @abstractproperty
    def target(self):
        #type: () -> MegamodelElement
        raise MethodNotDefined( #raise:OK
            'property .target is not implemented')

