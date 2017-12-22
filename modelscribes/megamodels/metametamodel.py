# coding=utf-8

import collections
import types
import abc
import importlib
from typing import List

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
        self.pyPackageName = 'modelscribes.metamodels.' + qname
        print('import metapackage %s' % self.pyPackageName)
        self.pyModule=importlib.import_module(
            self.pyPackageName)
        #type: types.ModuleType
        self.metaClassNamed=collections.OrderedDict()
        #type: List[MetaClass]

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

