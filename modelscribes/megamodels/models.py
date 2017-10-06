# coding=utf-8

import abc

from typing import Optional, Text, List

from modelscribes.base.issues import WithIssueList
from modelscribes.base.sources import SourceElement, SourceFile
from modelscribes.megamodels.megamodels import Megamodel
# from modelscribes.megamodels.dependencies.models import ModelDependency
from modelscribes.megamodels.metamodels import Metamodel
# from modelscribes.megamodels.dependencies.metamodels import MetamodelDependency
#MetamodelDependency='MetamodelDependency'
ModelDependency='ModelDependency'
MetamodelDependency='MetamodelDependency'

class Model(WithIssueList):
    """
    The root class for all models.

    Basically a model have a name, possibly a source file if
    the model is the result of parsing this file, a metamodel
    as well as an issue box. This issue box stores "semantical"
    errors found on the model while the source file stores
    "syntactical" errors. The issueBox has as a parent the
    sourceFile' issue box if any.
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        #type: () -> None



        self.name='' #type: Text
        # set later
        # If the model is from a sourceFile then set by parseToFillImportBox

        self.source=None  #type: Optional[SourceFile]
        # set later if build from a ModelSourceFile.
        # Set in the constuctor of ModelSourcFile
        super(Model, self).__init__(parents=[])
        # parents set at the same time as source

        self.modelKind='' #type: Text
        # set later. A keyword like "conceptual", "preliminary', ...
        # If the model is from a sourceFile then this attribute
        # is set by parseToFillImportBox
        # Could be '' if no kind specified

        # FIXME: add model dependencies. FIXME first check the code below (outDep, etc.)
        # The source contains importBox, but here we should have dependency box


    @abc.abstractproperty
    def metamodel(self):
        #type: () -> Metamodel
        pass

    # def addDependency(self, targeModel, sourceElement=None):
    #     md=ModelDependency(self, targeModel, sourceElement=sourceElement)
    #     Megamodel.registerModelDependency(md)
    #     return md

    def outDependencies(self, targetMetamodel=None, metamodelDependency=None):
        #type: (Optional[Metamodel]) -> List[ModelDependency]

        # select all out dependencies from self
        all_deps=Megamodel.modelDependencies(source=self)
        if targetMetamodel is None:
            deps=all_deps
        else:
            deps=[
                dep for dep in all_deps
                    if dep.targetModel.metamodel == targetMetamodel
            ]
        if metamodelDependency is None:
            return deps
        else:
            return [
                dep for dep in deps
                    # could raise ValueError, but should not
                    if dep.metamodelDependency==metamodelDependency
            ]

    def inDependencies(self, sourceMetamodel=None):
        #type: (Optional[Metamodel]) -> List[ModelDependency]
        deps=Megamodel.modelDependencies(target=self)
        if sourceMetamodel is None:
            return deps
        return [
            dep for dep in deps
                if dep.sourceModel.metamodel == sourceMetamodel
        ]

    def checkDependencies(self, metamodelDependencies=None):
        #type: (List[MetamodelDependency])->None
        """
        Check if this model has not problems with dependencies.
        Do nothing if this is not the case. Otherwise
        it is else raise a ValueError.
        This could be because there is no corresponding
        metamodel dependency for a model metamodel.
        This could also due because of too much outgoing
        dependency of the same typel.
        This could be because of missing dependency.
        """

        #-- metamodels dependencies to be check against
        if metamodelDependencies is None:
            mm_deps=Megamodel.metamodelDependencies(
                source=self.metamodel)
        else:
            mm_deps=metamodelDependencies

        #-- perform check for all metamodels dependencies
        for mm_dep in mm_deps:
            # all model dependencies of type mm_dep
            # starting from here
            m_deps=self.outDependencies(metamodelDependency=mm_dep)
            if len(m_deps)==0 and not mm_dep.optional:
                raise ValueError(
                    'Reference to a %s model is model is missing'
                    % mm_dep.targetMetamodel)
            elif len(m_deps)>=0 and not mm_dep.multiple:
                raise ValueError(
                    'Too many %s models associated with this model'
                    % mm_dep.targetMetamodel)
            else:
                pass
