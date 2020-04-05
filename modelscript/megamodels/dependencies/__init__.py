# coding=utf-8
"""Dependencies.
This module provides only one abstract class "Dependency",
the root of all concrete dependencies defined in separated modules.
"""

from abc import ABCMeta, abstractmethod
from modelscript.base.exceptions import (
    MethodToBeDefined)


MegamodelElement = 'MegamodelElement'


class Dependency(object, metaclass=ABCMeta):
    @property
    @abstractmethod
    def source(self) -> MegamodelElement:
        raise MethodToBeDefined(  # raise:OK
            'property .source is not implemented')

    @property
    @abstractmethod
    def target(self) -> MegamodelElement:
        raise MethodToBeDefined(  # raise:OK
            'property .target is not implemented')

