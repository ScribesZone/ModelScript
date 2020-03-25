# coding=utf-8

from abc import ABCMeta, abstractproperty
from modelscript.base.exceptions import (
    MethodToBeDefined)



MegamodelElement='MegamodelElement'
class Dependency(object):
    __metaclass__ = ABCMeta

    @abstractproperty
    def source(self):
        #type: () -> MegamodelElement
        raise MethodToBeDefined( #raise:OK
            'property .source is not implemented')

    @abstractproperty
    def target(self):
        #type: () -> MegamodelElement
        raise MethodToBeDefined( #raise:OK
            'property .target is not implemented')

