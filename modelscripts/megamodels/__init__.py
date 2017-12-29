import os

from modelscripts.megamodels.models import Model

from modelscripts.megamodels.dependencies import Dependency
from modelscripts.megamodels.megamodels._registries.metamodels import _MetamodelRegistry
from modelscripts.megamodels.megamodels._registries.models import _ModelRegistry
from modelscripts.megamodels.megamodels._registries.sources import _SourceRegistry
from modelscripts.megamodels.megamodels._registries.metapackages import _MetaPackageRegistry
from modelscripts.megamodels.megamodels._registries.metacheckers import _MetaCheckerPackageRegistry
from modelscripts.megamodels.megamodels._registries.issues import _IssueBoxRegistry



from modelscripts.megamodels.models import Model
from modelscripts.megamodels.metamodels import Metamodel
# from modelscripts.megamodels import Megamodel

# class MegamodelModel(Model, Megamodel):
#     def __init__(self):
#         super(MegamodelModel, self).__init__()
#
#     @property
#     def metamodel(self):
#         #type: () -> Metamodel
#         return METAMODEL


class Megamodel(
    Model,
    _MetamodelRegistry,
    _ModelRegistry,
    _SourceRegistry,
    _MetaPackageRegistry,
    _MetaCheckerPackageRegistry,
    _IssueBoxRegistry):

    model=None
    """
    A unique instance of Megamodel()
    """
    # Will be filled later by a unique instance
    # of MegamodelModel()
    # This cannot be done now as this creates a
    # circular dependency between Megamodel and MegamodelModel

    """
    Static class containing a global registry
    of metamodels
    and models and corresponding dependencies.
    """

    def __init__(self):
        Model.__init__(self)

    @property
    def metamodel(self):
        #type: () -> Metamodel
        return METAMODEL

    @classmethod
    def fileMetamodel(cls, filename):
        try:
            extension = os.path.splitext(filename)[1]
            return cls.theMetamodel(ext=extension)
        except:
            return None

    @classmethod
    def loadFile(cls, filename):
        if not os.path.exists(filename):
            raise ValueError('File not found: %s' % filename)
        try:
            path = os.path.realpath(filename)
            # check if already registered
            return cls.source(path=path)
        except:
            # source not registered, so builf it
            mm = cls.fileMetamodel(filename)
            if mm is None:
                b = os.path.basename(filename)
                raise ValueError(
                    'No metamodel available for %s' % b)
            try:
                factory = mm.sourceClass
            except NotImplementedError:
                raise ValueError(
                    'No parser available for %s' %
                    mm.name)
            else:
                return factory(filename)

    @classmethod
    def displayModel(cls,
                     model,
                     config=None):
        printer = model.metamodel.modelPrinterClass(
            theModel=model,
            config=config)
        printer.display()

    @classmethod
    def displaySource(cls,
                      source,
                      config=None):
        printer = source.metamodel.sourcePrinterClass(
            theSource=source,
            config=config)
        printer.display()

    @classmethod
    def displayModelDiagram(
            cls,
            model,
            config=None):
        raise NotImplementedError()



METAMODEL=Metamodel(
    id='mg',
    label='megamodel',
    extension='.mgs',
    modelClass=Megamodel
)

