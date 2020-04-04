# coding=utf-8

from abc import ABCMeta, abstractmethod
from modelscript.base.exceptions import (
    MethodToBeDefined)



MegamodelElement='MegamodelElement'
class Dependency(object, metaclass=ABCMeta):
    @property
    @abstractmethod
    def source(self):
        #type: () -> MegamodelElement
        raise MethodToBeDefined( #raise:OK
            'property .source is not implemented')

    @property
    @abstractmethod
    def target(self):
        #type: () -> MegamodelElement
        raise MethodToBeDefined( #raise:OK
            'property .target is not implemented')

