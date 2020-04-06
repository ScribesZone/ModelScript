# coding=utf-8
""" Implement a megamodel as a singleton. """

from typing import Text, Optional, ClassVar, Any
import os
import io
import re

from modelscript.megamodels.models import Model
from modelscript.megamodels.dependencies import Dependency
from modelscript.base.exceptions import (
    MethodToBeDefined)
from modelscript.base.issues import (
    Issue,
    Levels,
    FatalError)
from modelscript.megamodels.models import Model
from modelscript.megamodels.metamodels import Metamodel
from modelscript.base.exceptions import (
    NotFound,
    NoSuchFeature,
    UnexpectedValue)

# import facets for extending Megamodel
from modelscript.megamodels.megamodels._registries.metamodels import (
    _MetamodelRegistry)
from modelscript.megamodels.megamodels._registries.models import (
    _ModelRegistry)
from modelscript.megamodels.megamodels._registries.sources import (
    _SourceFileRegistry)
from modelscript.megamodels.megamodels._registries.metapackages import (
    _MetaPackageRegistry)
from modelscript.megamodels.megamodels._registries.metacheckers import (
    _MetaCheckerPackageRegistry)
from modelscript.megamodels.megamodels._registries.issues import (
    _IssueBoxRegistry)

__all__=(
    'Megamodel',
    'METAMODEL'
)

# list of issue codes
_ISSUES = {
    'NO_FILE': 'mg.FileNotFound',
    'NO_META': 'mg.NoMetamodel',
    'NO_PARSER': 'mg.NoParser',
}


def _icode(ilabel):
    return _ISSUES[ilabel]


class Megamodel(
        Model,
        # All the classes below make it possible to define related
        # methods in separated modules. This avoid having a huge class
        # with hundreds of methods.
        _MetamodelRegistry,
        _ModelRegistry,
        _SourceFileRegistry,
        _MetaPackageRegistry,
        _MetaCheckerPackageRegistry,
        _IssueBoxRegistry):

    model: Optional['MegamodelModel'] = None  # will be not null
    """A unique instance of Megamodel() """
    # Will be filled later by a unique instance of MegamodelModel()
    # This cannot be done now as this creates a
    # circular dependency between Megamodel and MegamodelModel

    """Static class containing a global registry of metamodels
    and models and corresponding dependencies.
    """

    analysisLevel: ClassVar[str] = 'full'
    """The analysisLevel attribute can take the following values:
    *  "justAST": source files are just parsed independently from each 
       others. The "import" statement are not followed.
    *  "justASTDep": source files are parsed and "import" statements are
       followed.
    *  "full": the source files are fully analyzed.
    The model of each source files are empty when using "justAST" or 
    "justASTDep".
    The attribute default is "full", but a program can change this
    value before all analysis start, so that the analysis level is
    consistent.
    """

    def __init__(self):
        Model.__init__(self)

    @property
    def homeDirectory(self) -> str:
        """Modelscript home directory."""
        return os.path.realpath(
            os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                '..', '..'))

    @property
    def version(self) -> str:
        """Get the version by extracting :version: label from CHANGES.rst
        """
        VERSION_FILE='CHANGES.rst'
        def read(file):
            encoding = 'utf-8'
            buf = []
            with io.open(file, encoding=encoding) as f:
                buf.append(f.read())
            return '\n'.join(buf)

        file=os.path.join(self.homeDirectory, VERSION_FILE)
        content = read(file)
        version_match = re.search(r"^:version: *([^\s]+)",
                                  content, re.M)
        if version_match:
            return version_match.group(1)
        raise RuntimeError(
            "Unable to find version string from file '%s.'" % VERSION_FILE)

    @property
    def metamodel(self) -> Metamodel:
        return METAMODEL

    @classmethod
    def fileMetamodel(cls, filename: str) -> Any:
        """The metamodel corresponding to a given file or None.
        The extension of the file is used to determine the metamodel.
        If no metamodel is found return None
        """
        try:
            extension = os.path.splitext(filename)[1]
            return cls.theMetamodel(ext=extension)
        except UnexpectedValue:  # raise except:TODO:4
            return None

    #TODO:3 check the difference between loadFile() vs. sourceFile()
    #   not sure if sourceFile contains so different code from
    #   loadFile. It could make sense to extend sourceFile()
    @classmethod
    def loadFile(cls,
                 filename: Text,
                 withIssueList: Optional['WithIssueList'] = None)\
            -> Optional ['ModelSource'] :
        """Load a given file into the megamodel.
        Return a model source file. This source file can
        naturally contain some issues in its issue box.
        If it not possible at all to create such a source file
        then return None. In this case the issue that cause
        and the corresponding issue is stored in the issue box
        of the given parameter. If withIssueList is none then
        then the issue goes to issue box of the global megamodel.
        """
        origin = cls.model if withIssueList is None else withIssueList
        try:
            if not os.path.exists(filename):
                # The file to load does not exist
                # Raise a fatal error.
                message = 'File not found:  %s' % filename
                Issue(
                    origin=origin,
                    level=Levels.Fatal,
                    message=message,
                    code=_icode('NO_FILE'))
            try:
                # Check if the file to be loaded  has been already
                # registered. In this case just return it.
                path = os.path.realpath(filename)
                return cls.sourceFile(path=path)
            except NotFound:
                # The file has not been loaded yet.
                # Build the sourcefile according to its metamodel.
                mm = cls.fileMetamodel(filename)
                if mm is None:
                    # The metamodel is not registered :
                    # create a Fatal issue.
                    b = os.path.basename(filename)
                    message = 'No metamodel available for %s' % b
                    Issue(
                        origin=origin,
                        level=Levels.Fatal,
                        message=message,
                        code=_icode('NO_META'))
                try:
                    # Get the python factory class for the given metamodel.
                    # This is a subclass of ASTBasedModelSourceFile.
                    # For instance UsecaseModelSource, a parser of a
                    # script.
                    factory = mm.sourceClass
                except NoSuchFeature:
                    # No such factory class has been registered. This
                    # is an odd situation.
                    Issue(  # TODO:3 check why it is not caught
                        origin=cls.model,  # the megamodel itself,
                        level=Levels.Fatal,
                        message=
                            'No parser available for %s metamodel'
                            % mm.label,
                        code=_icode('NO_PARSER')
                    )
                else:
                    # Create a source file using the factory.
                    # This launch the parser and create the source file.
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



METAMODEL = Metamodel(
    id='mg',
    label='megamodel',
    extension='.mgs',
    modelClass=Megamodel
)

