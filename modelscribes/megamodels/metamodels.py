# coding=utf-8
from typing import Text, Callable, Optional, List
from collections import OrderedDict

from modelscribes.megamodels.megamodels import Megamodel

Cls=Callable
OptCls=Optional[Cls]


class Metamodel(object):  # TODO should be model instead of object
    def __init__(self,
                 id,
                 label,
                 extension,
                 modelClass,
                 modelKinds=('',),
                 sourceClass=None,
                 modelPrinterClass=None,
                 sourcePrinterClass=None,
                 diagramPrinterClass=None,
                 ):
        #type: (Text, Text, Text, Cls, OptCls, OptCls, OptCls, OptCls) -> None
        self.id=id
        self.label=label
        self.extension=extension
        self.modelKinds=modelKinds
        self._modelClass=modelClass
        self._sourceClass=sourceClass
        self._modelPrinterClass=modelPrinterClass
        self._sourcePrinterClass=sourcePrinterClass
        self._diagramPrinterClass=diagramPrinterClass
        Megamodel.registerMetamodel(self)

    @property
    def modelClass(self):
        if self._modelClass is None:
            raise NotImplementedError(
                '%s.model not implemented' % self.label)
        else:
            return self._modelClass

    @property
    def sourceClass(self):
        # print('&&&&&&&&&&'*10,self.label)
        if self._sourceClass is None:
            raise NotImplementedError(
                '%s.source not implemented' % self.label)
        else:
            return self._sourceClass

    @property
    def modelPrinterClass(self):
        if self._modelPrinterClass is None:
            raise NotImplementedError(
                '%s.modelPrinter not implemented' % self.label)
        else:
            return self._modelPrinterClass

    @property
    def sourcePrinterClass(self):
        if self._sourcePrinterClass is None:
            raise NotImplementedError(
                '%s.sourcePrinter not implemented' % self.label)
        else:
            return self._sourcePrinterClass

    @property
    def diagramPrinterClass(self):
        if self._diagramPrinterClass is None:
            raise NotImplementedError(
                '%s.sourcePrinter not implemented' % self.label)
        else:
            return self._diagramPrinterClass

    def registerSource(self, cls):
        # TODO: check that cls is a subclass
        self._sourceClass=cls
        # print('+-'*10+'%s.registerSource(%s)' %
        #      (self.label, cls))

    def registerModelPrinter(self, cls):
        # TODO: check that cls is a subclass
        self._modelPrinterClass=cls
        # print('+-'*10+'%s.registerModelPrinter(%s)' %
        #      (self.label, cls))

    def registerSourcePrinter(self, cls):
        # TODO: check that cls is a subclass
        self._sourcePrinterClass=cls
        #print('+-'*10+'%s.registerSourcePrinter(%s)' %
        #      (self.label, cls))

    def registerDiagramPrinter(self, cls):
        # TODO: check that cls is a subclass
        self._diagramPrinterClass=cls
        # print('+-'*10+'%s.registerDiagramPrinter(%s)' %
        #       (self.label, cls))

    @property
    def models(self):
        #type: () -> List['Model']
        return Megamodel.models(metamodel=self)

    @property
    def outMetamodelDependencies(self):
        return Megamodel.metamodelDependencies(
            source=self
        )

    @property
    def outMetamodels(self):
        return list(OrderedDict.fromkeys(
            [ mmd.targetMetamodel
              for mmd in self.outMetamodelDependencies ]

        ))


    def __str__(self):
        return '%s metamodel' % self.label

    def __unicode__(self):
        return self.__str__()

    def __repr__(self):
        def name(cls):
            return 'None' if cls is None else cls.__name__

        return 'metamodel(%s/%s/%s/%s new(%s) src(%s) prt(%s) prtSrc(%s) prtDg(%s)' % (
            self.label,
            self.id,
            self.extension,
            '[%s]' % ','.join(self.modelKinds),
            name(self._modelClass),
            name(self._sourceClass),
            name(self._modelPrinterClass),
            name(self._sourcePrinterClass),
            name(self._diagramPrinterClass))