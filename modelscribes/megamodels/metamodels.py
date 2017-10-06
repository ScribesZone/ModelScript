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
        self.modelClass=modelClass
        self.modelKinds=modelKinds
        self.sourceClass=sourceClass
        self.modelPrinterClass=modelPrinterClass
        self.sourcePrinterClass=sourcePrinterClass
        self.diagramPrinterClass=diagramPrinterClass
        Megamodel.registerMetamodel(self)

    def registerSource(self, cls):
        # TODO: check that cls is a subclass
        self.sourceClass=cls

    def registerModelPrinter(self, cls):
        # TODO: check that cls is a subclass
        self.modelPrinterClass=cls

    def registerSourcePrinter(self, cls):
        # TODO: check that cls is a subclass
        self.sourcePrinterClass=cls

    def registerDiagramPrinter(self, cls):
        # TODO: check that cls is a subclass
        self.diagramPrinterClass=cls

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
            [ mmd.sourceMetamodel
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
            name(self.modelClass),
            name(self.sourceClass),
            name(self.modelPrinterClass),
            name(self.sourcePrinterClass),
            name(self.diagramPrinterClass))