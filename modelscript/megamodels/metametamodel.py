# coding=utf-8
"""Metametamodel.

It is not clear whether this module is used or not. It seems that
it is competing with the modelscript.megamodels.py module.
To be checked.
"""

import collections
import types
import abc
import importlib
from typing import List, Dict, Any, Optional

from modelscript.megamodels import Megamodel

__all__ = (
    'MetaModelElement',
    'MetaPackage',
    'MetaCheckerPackage',
    'MetaClass',
    'MetaFeature',
    'MetaAttribute',
    'MetaReference',
)

DEBUG = 0

#TODO:4 merge metamodelelements in the megamodel


class MetaModelElement(object):

    qname: str
    name: str
    qualifier: str

    def __init__(self, qname):
        self.qname = qname
        self.name = qname.split('.')[-1:]
        self.qualifier = qname.split('.')[:-1]

class MetaFeature(MetaModelElement, metaclass=abc.ABCMeta):
    
    pyMethod: Any   # check types
    many: Any
    required: Any
    type: Any
    
    def __init__(self, qname, metaClass, pyMethod):
        super(MetaFeature, self).__init__(qname)

        self._metaClass = metaClass
        # inverse set in sub-metaclasses

        self.pyMethod = pyMethod

        self.many = None
        self.required = None
        self.type = None  # basic type or metaCLass


class MetaAttribute(MetaFeature):

    def __init__(self, qname, metaClass, pyMethod):
        super(MetaAttribute, self).__init__(
            qname=qname,
            metaClass=metaClass,
            pyMethod=pyMethod)


class MetaReference(MetaFeature):
    
    opposite: Optional['MetaReference']

    def __init__(self, qname, metaClass, pyMethod):
        super(MetaReference, self).__init__(
            qname=qname,
            metaClass=metaClass,
            pyMethod=pyMethod)
        self.opposite = None


class MetaClass(MetaModelElement):
    
    _metaPackage: 'MetaPackage'
    pyClass: Any # check what is the type of python classes
    _superMetaClasses: List['MetaClass']
    metaAttributeNamed: Dict[str, MetaAttribute]
    metaReferenceNamed: Dict[str, MetaReference]
    metaOperationNamed: Any  # to be checked
    
    def __init__(self, qname, metaPackage, pyClass):
        super(MetaClass, self).__init__(qname)

        self._metaPackage=metaPackage
        self._metaPackage.metaClassNamed[self.name] = self

        self.pyClass = pyClass
        self._superMetaClasses = []
        self.metaAttributeNamed = collections.OrderedDict()
        self.metaReferenceNamed = collections.OrderedDict()
        self.metaOperationNamed = collections.OrderedDict()

    @property
    def metaPackage(self):
        return self._metaPackage

    @property
    def superMetaClasses(self):
        return self._superMetaClasses

    @property
    def metaAttributes(self):
        return list(self.metaAttributeNamed.values())

    @property
    def metaReferences(self):
        return list(self.metaReferenceNamed.values())

    @property
    def metaOperations(self):
        return list(self.metaOperationNamed.values())


class MetaPackage(MetaModelElement):
    pyPackageName: str
    pyModule: types.ModuleType
    metaClassNamed: Dict[str, MetaClass]

    def __init__(self, qname):
        """ Create a MetaPackage and import the corresponding pyModule. """
        super(MetaPackage, self).__init__(qname=qname)
        self.pyPackageName = 'modelscript.metamodels.' + qname
        if DEBUG >= 1:
            print(('MM3: import metapackage %s' % self.pyPackageName))
        self.pyModule = importlib.import_module(
            self.pyPackageName)
        self.metaClassNamed=collections.OrderedDict()
        Megamodel.registerMetaPackage(self)


class MetaCheckerPackage(MetaModelElement):
    """
    Create a MetaCheckerPackage and import the corresponding pyModule
    """
    def __init__(self, qname):
        super(MetaCheckerPackage, self).__init__(qname=qname)
        self.pyPackageName = 'modelscript.metamodels.' + qname
        if DEBUG>=1:
            print(('MM3: import metacheckerpackage %s' % self.pyPackageName))
        self.pyModule=importlib.import_module(
            self.pyPackageName)
        #type: types.ModuleType

        Megamodel.registerMetaCheckerPackage(self)





