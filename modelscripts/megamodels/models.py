# coding=utf-8
"""
Define models with their features.
"""

import abc

from typing import Optional, Text, List

from modelscripts.megamodels.issues import WithIssueModel
from modelscripts.base.metrics import (
    Metrics,
    Metric
)
from modelscripts.megamodels.megamodels import (
    MegamodelElement
)
from modelscripts.megamodels.elements import ModelElement
from modelscripts.metamodels.textblocks import WithTextBlocks
# from modelscripts.megamodels.metamodels import Metamodel
# from modelscripts.megamodels.sources import (
#     ModelOldSourceFile
# )
# from modelscripts.megamodels.dependencies.models import ModelDependency
# from modelscripts.megamodels.dependencies.metamodels import MetamodelDependency
Metamodel='Metamodel'
ModelSourceFile='ModelOldSourceFile'
ModelDependency='ModelDependency'
MetamodelDependency='MetamodelDependency'

__all__=(
    'Model',
    'ModelElement',
)
DEBUG=1




class Model(MegamodelElement, ModelElement, WithIssueModel, WithTextBlocks):
    """
    The root class for all models.

    Basically a model have:
    - a name,
    - possibly a source file if the model is the result
      of parsing this file,
    - a metamodel
    - an issue box. This issue box stores "semanctical"
      errors found on the model, while the source
      file issuebox stores "syntactical" errors.
      The _issueBox has as a parent the sourceFile'
      issue box if any.
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        #type: () -> None

        self.name='' #type: Text
        # set later
        # If the model is from a sourceFile
        # then set by parseToFillImportBox

        self.source=None  #type: Optional[ModelSourceFile]
        # Set later if build from a ModelOldSourceFile.
        # Set in the constuctor of ModelOldSourceFile
        MegamodelElement.__init__(self)

        WithIssueModel.__init__(self, parents=[])
        # Parents set at the same time as source

        ModelElement.__init__(self, self)


        self.kind='' #type: Text
        # Set later.
        # A keyword like "conceptual", "preliminary', ...
        # If the model is from a sourceFile then
        # this attribute
        # is set by parseToFillImportBox
        # Could be '' if no kind specified

        self.status='' #type: Text
        # Set later
        # a keyword like "draft" | "" | "consolidated"

        # FIXME: add model dependencies.
        # FIXME first check the code below (outDep, etc.)
        # The source contains importBox, but
        # here we should have dependency box

    @abc.abstractproperty
    def metamodel(self):
        #type: () -> Metamodel
        raise NotImplementedError()


    @property
    def label(self):
        name='_' if self.name=='' else self.name
        if self.source is None:
            return '%s:%s()' % (
                name,
                self.metamodel.id)
        else:
            return '%s:%s(%s)' % (
                name,
                self.metamodel.id,
                self.source.label)

    # @property
    # def originLabel(self):
    #     return self.label

    @property
    def metrics(self):
        #type: ()->Metrics
        ms=Metrics()
        ms.add(
            Metric('model descriptor', len(self.descriptors))
        )
        ms.addMetrics(self.textBlocksMetrics)
        return ms

    @property
    def fullMetrics(self):
        #type: () -> Metrics
        ms=self.metrics
        if self.source is not None:
            ms.addMetrics(self.source.metrics)
        return ms

    @property
    def text(self):
        return self.metamodel.modelPrinterClass(self).do()

    def resolve(self):
        """
        Resolve the model. This is useful for instance to create actual
        references to model element by replacing symbols. What this
        method do is metamodel dependent. All sub methods have to call
        this method. This method solve references in text blocks.
        """

        def resolveTextBlocks():
            for block in self.textBlocks:
                block.resolve()

        if DEBUG>=1:
            _=(' RESOLVE '+self.label+' ').center(70, '.')
            print('MOD: '+_)
        resolveTextBlocks()

    def finalize(self):
        if DEBUG>=1:
            _=(' FINALIZE '+self.label+' ').center(70, '.')
            print('MOD: '+_)
        self.check()

    def str( self,
             method='do',
             config=None
            ):
        printer_class=self.metamodel.modelPrinterClass
        printer=printer_class(
            theModel=self,
            config=config
        )
        try:
            the_method = getattr(printer_class, method)
            return the_method(printer)
        except AttributeError:
            raise NotImplementedError(
                "Class `{}` does not implement `{}`".format(
                    printer_class.__class__.__name__,
                    method))

    def theModel(self, targetMetamodel):
        lm=self.usedModels(targetMetamodel=targetMetamodel)
        if len(lm)==0:
            raise ValueError(
                'No %s model found. Expected one.'
                % targetMetamodel.name)
        elif len(lm)>=2:
            raise ValueError(
                '%i %s models found. Expected one.'
                % (len(lm), targetMetamodel.name))
        else:
            return lm[0]


    def usedModels(self,
                   targetMetamodel=None,
                   metamodelDependency=None):
        outdeps=self.outDependencies(
            targetMetamodel=targetMetamodel,
            metamodelDependency=metamodelDependency)
        return [dep.targetModel for dep in outdeps]



    def clientModels(self,
                     targetMetamodel=None,
                     metamodelDependency=None):
        indeps=self.outDependencies(
            targetMetamodel=targetMetamodel,
            metamodelDependency=metamodelDependency)
        return [ dep.targetModel for dep in indeps]

    def outDependencies(self, targetMetamodel=None, metamodelDependency=None):
        #type: (Optional[Metamodel]) -> List[ModelDependency]
        """
        Returns the dependencies starting from this
        dependency filtered either by targetMetamodel,
        or by metamodelDependency.
        """

        # select all out dependencies from self
        from modelscripts.megamodels import Megamodel
        all_deps=Megamodel.modelDependencies(source=self)
        if targetMetamodel is None:
            deps=all_deps
        else:
            deps=[
                dep for dep in all_deps
                    if (
                        dep.targetModel.metamodel
                        == targetMetamodel)
            ]
        if metamodelDependency is None:
            return deps
        else:
            return [
                dep for dep in deps
                    # could raise ValueError, but should not
                    if (dep.metamodelDependency
                        == metamodelDependency)
            ]

    @property
    def outgoingDependencies(self):
        return self.outDependencies()


    def inDependencies(self, sourceMetamodel=None):
        #type: (Optional[Metamodel]) -> List[ModelDependency]
        """
        Returns the dependencies towards from this
        dependency filtered either by targetMetamodel,
        or by metamodelDependency.
        """
        from modelscripts.megamodels import Megamodel
        deps=Megamodel.modelDependencies(target=self)
        if sourceMetamodel is None:
            return deps
        return [
            dep for dep in deps
                if (dep.sourceModel.metamodel
                    == sourceMetamodel)
        ]

    @property
    def incomingDependencies(self):
        return self.inDependencies()


    def checkDependencies(self, metamodelDependencies=None):
        #type: (List[MetamodelDependency])->None
        """
        Check if this model has not problems with
        dependencies.
        Do nothing if this is not the case. Otherwise
        it is else raise a ValueError.
        This could be because there is no corresponding
        metamodel dependency for a model metamodel.
        This could also due because of too much outgoing
        dependency of the same typel.
        This could be because of missing dependency.
        """

        #-- metamodels dependencies to be check against
        from modelscripts.megamodels import Megamodel
        if metamodelDependencies is None:
            mm_deps=Megamodel.metamodelDependencies(
                source=self.metamodel)
        else:
            mm_deps=metamodelDependencies

        #-- perform check for all metamodels dependencies
        for mm_dep in mm_deps:
            # all model dependencies of type mm_dep
            # starting from here
            m_deps=self.outDependencies(
                metamodelDependency=mm_dep)
            if len(m_deps)==0 and not mm_dep.optional:
                raise ValueError(
                    'Reference to a %s model'
                    ' is model is missing'
                    % mm_dep.targetMetamodel)
            elif len(m_deps)>=0 and not mm_dep.multiple:
                raise ValueError(
                    'Too many %s models associated'
                    ' with this model'
                    % mm_dep.targetMetamodel)
            else:
                pass

    def __str__(self):
        return '<model:%s>' % self.label

    def __repr__(self):
        return '<model:%s>' % self.label


class Placeholder(object):
    """
    Used just to put some symbol value in some model
    waiting for some kind of symbol resolution. This will be
    replaced by an actual reference to a model element.
    """
    def __init__(self, placeholderValue, type=None):
        self.placeholderValue=placeholderValue
        self.type=type

    def __str__(self):
        return ('***%s(%s)***' %(
            self.placeholderValue,
            self.type))
