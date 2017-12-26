# coding=utf-8

from abc import ABCMeta, abstractproperty

MegamodelElement='MegamodelElement'
class Dependency(object):
    __metaclass__ = ABCMeta

    @abstractproperty
    def source(self):
        #type: () -> MegamodelElement
        raise ValueError()

    @abstractproperty
    def target(self):
        #type: () -> MegamodelElement
        raise ValueError()

