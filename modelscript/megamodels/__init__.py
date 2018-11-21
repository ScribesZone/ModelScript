
"""
Implement a megamodel as a singleton.
"""
from typing import Text, Optional
import os
import io
import re
from modelscript.megamodels.models import Model
from modelscript.megamodels.dependencies import Dependency

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
    # with hundreds of methods.
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

    analysisLevel='full'
    """
    The analysisLevel attribute can take the following values:
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
    def homeDirectory(self):
        return os.path.realpath(
            os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                '..', '..'))
    @property
    def version(self):
        """
        get the version by extracting :version: label from CHANGES.rst
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

