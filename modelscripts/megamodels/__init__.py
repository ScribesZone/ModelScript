
"""
Implement a megamodel as a singleton.
"""
from typing import Text, Optional
import os

from modelscripts.megamodels.models import Model
from modelscripts.megamodels.dependencies import Dependency

# import facets for extending Megamodel
from modelscripts.megamodels.megamodels._registries.metamodels import (
    _MetamodelRegistry)
from modelscripts.megamodels.megamodels._registries.models import (
    _ModelRegistry)
from modelscripts.megamodels.megamodels._registries.sources import (
    _SourceFileRegistry)
from modelscripts.megamodels.megamodels._registries.metapackages import (
    _MetaPackageRegistry)
from modelscripts.megamodels.megamodels._registries.metacheckers import (
    _MetaCheckerPackageRegistry)
from modelscripts.megamodels.megamodels._registries.issues import (
    _IssueBoxRegistry)

from modelscripts.base.exceptions import (
    MethodToBeDefined)
from modelscripts.base.issues import (
    Issue,
    Levels,
    FatalError)

from modelscripts.megamodels.models import Model
from modelscripts.megamodels.metamodels import Metamodel
from modelscripts.base.exceptions import (
    NotFound,
    NoSuchFeature,
    UnexpectedValue)


ISSUES={
    'NO_FILE': 'mg.FileNotFound',
    'NO_META': 'mg.NoMetamodel',
    'NO_PARSER': 'mg.NoParser',
}

def icode(ilabel):
    return ISSUES[ilabel]

class Megamodel(
    Model,
    # All the classes below make it possible to define related
    # methods in separated modules. This avoid having a huge class
    # with unhundreds of methods.
    _MetamodelRegistry,
    _ModelRegistry,
    _SourceFileRegistry,
    _MetaPackageRegistry,
    _MetaCheckerPackageRegistry,
    _IssueBoxRegistry):

    model=None
    """
    A unique instance of Megamodel()
    """
    # Will be filled later by a unique instance of MegamodelModel()
    # This cannot be done now as this creates a
    # circular dependency between Megamodel and MegamodelModel

    """
    Static class containing a global registry of metamodels
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
        """
        The metamodel corresponding to a given file or None.
        The extension of the file is used to determine the metamodel.
        If no metamodel is found return None
        """
        try:
            extension = os.path.splitext(filename)[1]
            return cls.theMetamodel(ext=extension)
        except UnexpectedValue: #except:TODO:4
            return None

    #TODO:3 check the difference between loadFile() vs. sourceFile()
    #   not sure if sourceFile contains so different code from
    #   loadFile. It could make sense to extend sourceFile()
    @classmethod
    def loadFile(cls, filename, withIssueList=None):
        #type: (Text, 'WithIssueList')->Optional['ModelSource']
        """
        Load a given file into the megamodel.
        Return a model source file. This source file can
        naturally contain some issues in its issue box.
        If it not possible at all to create such a source file
        then return None. In this case the issue that cause
        and the corresponding issue is stored in the issue box
        of the givenparameter. If withIssueList is none then
        then the issue goes to issue box of the global megamodel.
        """
        origin=cls.model if withIssueList is None else withIssueList
        try:
            if not os.path.exists(filename):
                message='File not found:  %s' % filename
                Issue(
                    origin=origin,
                    level=Levels.Fatal,  # see below
                    # The lovel should be Fatal but except Fatal
                    # is within the context of the source.
                    # Here it will necessary to catch the Fatal
                    # again. A much simpler way to
                    message=message,
                    code=icode('NO_FILE'))
            try:
                path = os.path.realpath(filename)
                # check if already registered
                return cls.sourceFile(path=path)
            except NotFound:
                # source not registered, so builf it
                mm = cls.fileMetamodel(filename)
                if mm is None:
                    b = os.path.basename(filename)
                    message='No metamodel available for %s' % b
                    Issue(
                        origin=origin,
                        level=Levels.Fatal,
                        message=message,
                        code=icode('NO_META'))
                try:
                    factory = mm.sourceClass
                except NoSuchFeature:
                    Issue(  # TODO:3 check why it is not caught
                        origin=cls.model,  # the megamodel itself,
                        level=Levels.Fatal,
                        message=
                            'No parser available for %s metamodel'
                            % mm.label,
                        code=icode('NO_PARSER')
                    )
                else:
                    return factory(filename)
        except FatalError:
            return None


    @classmethod
    def displayModel(cls,
                     model,
                     config=None):
        """
        Display the given model with the associated printer.
        A configration can be provided.
        """
        printer = model.metamodel.modelPrinterClass(
            theModel=model,
            config=config)
        printer.display()

    @classmethod
    def displaySource(cls,
                      source,
                      config=None):
        """
        Display the given source with the associated printer.
        A configration can be provided.
        """
        printer = source.metamodel.sourcePrinterClass(
            theSource=source,
            config=config)
        printer.display()

    @classmethod
    def displayModelDiagram(
            cls,
            model,
            config=None):
        """
        Display the given model diagram.
        """
        raise MethodToBeDefined( #raise:OK
            'displayModelDiagram() not implemented.'
        )



METAMODEL=Metamodel(
    id='mg',
    label='megamodel',
    extension='.mgs',
    modelClass=Megamodel
)

