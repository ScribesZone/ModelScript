# coding=utf-8

import collections
import types
import abc
import importlib
from typing import List
from modelscripts.megamodels import Megamodel

DEBUG=0

#TODO:4 merge metamodelelements in the megamodel

class MetaModelElement(object):
    def __init__(self, qname):
        self.qname=qname
        self.name= qname.split('.')[-1:]
        self.qualifier= qname.split('.')[:-1]

class MetaPackage(MetaModelElement):
    """
    Create a MetaPackage and import the corresponding pyModule
    """
    def __init__(self, qname):
        super(MetaPackage, self).__init__(qname=qname)
        self.pyPackageName = 'modelscripts.metamodels.' + qname
        if DEBUG>=1:
            print('MM3: import metapackage %s' % self.pyPackageName)
        self.pyModule=importlib.import_module(
            self.pyPackageName)
        #type: types.ModuleType
        self.metaClassNamed=collections.OrderedDict()
        #type: List[MetaClass]

        Megamodel.registerMetaPackage(self)

class MetaCheckerPackage(MetaModelElement):
    """
    Create a MetaCheckerPackage and import the corresponding pyModule
    """
    def __init__(self, qname):
        super(MetaCheckerPackage, self).__init__(qname=qname)
        self.pyPackageName = 'modelscripts.metamodels.' + qname
        if DEBUG>=1:
            print('MM3: import metacheckerpackage %s' % self.pyPackageName)
        self.pyModule=importlib.import_module(
            self.pyPackageName)
        #type: types.ModuleType

        Megamodel.registerMetaCheckerPackage(self)

class MetaClass(MetaModelElement):

    def __init__(self, qname, metaPackage, pyClass):
        super(MetaClass, self).__init__(qname)

        self._metaPackage=metaPackage
        self._metaPackage.metaClassNamed[self.name]=self

        self.pyClass=pyClass
        self._superMetaClasses=[]
        self.metaAttributeNamed=collections.OrderedDict()
        self.metaReferenceNamed=collections.OrderedDict()
        self.metaOperationNamed=collections.OrderedDict()

    @property
    def metaPackage(self):
        return self._metaPackage

    @property
    def superMetaClasses(self):
        return self._superMetaClasses

    @property
    def metaAttributes(self):
        return self.metaAttributeNamed.values()

    @property
    def metaReferences(self):
        return self.metaReferenceNamed.values()

    @property
    def metaOperations(self):
        return self.metaOperationNamed.values()


class MetaFeature(MetaModelElement):
    __metaclass__ = abc.ABCMeta

    def __init__(self, qname, metaClass, pyMethod):
        super(MetaFeature, self).__init__(qname)

        self._metaClass=metaClass
        # inverse set in submetaclasses

        self.pyMethod=pyMethod

        self.many=None
        self.required=None
        self.type=None  # basic type or metaCLass


class MetaAttribute(MetaFeature):

    def __init__(self, qname, metaClass, pyMethod):
        super(MetaAttribute, self).__init__(
            qname=qname,
            metaClass=metaClass,
            pyMethod=pyMethod)

class MetaReference(MetaFeature):

    def __init__(self, qname, metaClass, pyMethod):
        super(MetaReference, self).__init__(
            qname=qname,
            metaClass=metaClass,
            pyMethod=pyMethod)
        self.opposite=None

