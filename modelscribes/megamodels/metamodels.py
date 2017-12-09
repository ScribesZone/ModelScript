# coding=utf-8
"""
Metamodel with its description (label, extension, kinds) but
also implementation (modelClass, sourceClass, printer Classes).
"""
from typing import Text, Callable, Optional, List
from collections import OrderedDict

from modelscribes.megamodels.megamodels import (
    Megamodel,
    MegamodelElement
)
Cls=Callable
OptCls=Optional[Cls]


class Metamodel(MegamodelElement):
    # TODO:5 should be (Model) instead of (Object)

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
                'Modelscribes: %s.model not implemented yet' % self.label)
        else:
            return self._modelClass

    @property
    def sourceClass(self):
        if self._sourceClass is None:
            raise NotImplementedError(
                'Modelscribes: %s.source not implemented yet' % self.label)
        else:
            return self._sourceClass

    @property
    def modelPrinterClass(self):
        if self._modelPrinterClass is None:
            raise NotImplementedError(
                'Modelscribes: %s.modelPrinter not implemented yet' % self.label)
        else:
            return self._modelPrinterClass

    @property
    def sourcePrinterClass(self):
        if self._sourcePrinterClass is None:
            raise NotImplementedError(
                'Modelscribes: %s.sourcePrinter not implemented yet' % self.label)
        else:
            return self._sourcePrinterClass

    @property
    def diagramPrinterClass(self):
        if self._diagramPrinterClass is None:
            raise NotImplementedError(
                'Modelscribes: %s.sourcePrinter not implemented yet' % self.label)
        else:
            return self._diagramPrinterClass

    def registerSource(self, cls):
        self._sourceClass=cls

    def registerModelPrinter(self, cls):
        self._modelPrinterClass=cls

    def registerSourcePrinter(self, cls):
        self._sourcePrinterClass=cls

    def registerDiagramPrinter(self, cls):
        self._diagramPrinterClass=cls


    @property
    def models(self):
        #type: () -> List['Model']
        """
        Return all models for the current metamodel.
        """
        return Megamodel.models(metamodel=self)

    @property
    def outMetamodelDependencies(self):
        """
        Return all metamodel dependencies from the current
        metamodel.
        """
        return Megamodel.metamodelDependencies(
            source=self
        )

    @property
    def outgoingDependencies(self):
        return self.outMetamodelDependencies

    @property
    def incomingDependencies(self):
        return Megamodel.metamodelDependencies(target=self)

    @property
    def outMetamodels(self):
        """
        Return all metamodels that this metamodel depends on.
        """
        return list(OrderedDict.fromkeys(
            [ mmd.targetMetamodel
              for mmd in self.outMetamodelDependencies ]

        ))

    @property
    def targets(self):
        return self.outMetamodels



    def __str__(self):
        return '%s metamodel' % self.label

    def __unicode__(self):
        return self.__str__()

    def __repr__(self):
        def name(cls):
            return 'None' if cls is None else cls.__name__

        return (
            'metamodel(%s/%s/%s/%s ' % (
            # 'new(%s) src(%s) prt(%s) prtSrc(%s) prtDg(%s)' % (
            self.label,
            self.id,
            self.extension,
            '[%s]' % ','.join(self.modelKinds)
            # name(self._modelClass),
            # name(self._sourceClass),
            # name(self._modelPrinterClass),
            # name(self._sourcePrinterClass),
            # name(self._diagramPrinterClass))
        ))