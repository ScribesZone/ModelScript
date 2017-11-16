# coding=utf-8
"""
Source files for models.
Additionally to a regular source files, a ModelSourceFile
contains:

*   an attribute `model` containing the model resulting from
    parsing the source file,
*   an _issueBox containing all import statements.
*   the model declaration statement.
"""
from typing import Text, Optional, List, Any
from abc import ABCMeta, abstractproperty, abstractmethod

from modelscribes.base.sources import SourceFile
from modelscribes.base.issues import (
    IssueBox,
    FatalError
)
from modelscribes.megamodels.megamodels import (
    Megamodel
)
from modelscribes.megamodels.metamodels import (
    Metamodel
)
from modelscribes.megamodels.models import (
    Model
)
from modelscribes.megamodels.dependencies.sources import (
    ImportBox,
    SourceImport
)
from modelscribes.scripts.megamodels.parser import (
    parseToFillImportBox
)


class ModelSourceFile(SourceFile):

    """
    A source file with

    * a model,
    * an importBox and
    * a model declaration.
    """
    __metaclass__ = ABCMeta

    def __init__(self,
                 fileName,
                 realFileName=None,
                 preErrorMessages=(),  #TODO: check the type
                 readFileLater=False,
                 fillImportBoxLater=False,
                 parseFileLater=False,
                 noSymbolChecking=False,
                 allowedFeatures=(),
                 recognizeUSEOCLNativeModelDefinition=False):
        #type: (Text, Optional[Text], List[Any], bool, bool, bool, bool, List[Text], bool) -> None
        """
        An empty model is created automatically and it
        is associated with this source file.
        This empty model is created according to
        the metamodel specified by the property 'metamodel'.

        An importBox is also created.
        In order to do this the content of the source file is
        parsed looking the declaration of the model name as
        well as import statements. All this information is
        stored in the importBox.

        If `fillImportBoxLater` is True then this importBox
        is left empty for the moment. The client have
        to call explicitly parseToFillImportBox() later.

        The parameter recognizeUSEOCLNativeModelDefinition
        is a patch to allow parsing regular .use file.

        Args:
            fileName:
                The logical name of the file.
                This is not necessarily the file parsed.
            realFileName:
                The real file to be read. If file reading
                has to be postponed, then the parameter
                should be set to None. The doRealFileRead()
                will set the filed realFileName.
            preErrorMessages:
                The errors in this list will be added.
            readFileLater:
                If False the file is read directly.
                Otherwise the method doReadFile() must be called!
            fillImportBoxLater:
                If False, the file read is parsed to find
                megamodel statements (e.g. import) and to
                fill the import box.
                If not parseToFillImportBox() must be called
                after reading the file, and this in order to
                get the imported model.
            allowedFeatures
                The list of features allowed. This depends on
                each parser. This allows to remove the use of
                some features during parsing. For instance to
                forbid the use of association classes.

        """

        # Create an empty model
        # Not to be moved after super
        # This should be done in all case so that
        # the model attribute always exist even if there
        # are some error in reading the file
        self.model = self.emptyModel()  # type: Model




        # Call the super class, read the file or not
        try:
            # This can raise an exception for instance if
            # there is a problem reading the file
            super(ModelSourceFile, self).__init__(
                fileName=fileName,
                realFileName=realFileName,
                preErrorMessages=preErrorMessages,
                doNotReadFiles=readFileLater,
                allowedFeatures=allowedFeatures
            )
        except FatalError:
            pass   # an error as already been registered

        Megamodel.registerSource(self)
        Megamodel.registerModel(self.model)


        # Backward link & issue box linking
        self.model.source=self
        self.model._issueBox.addParent(self._issueBox)


        # Create first an empty ImportBox.
        # Then fill it by reading megamodel statements,
        # unless specified.
        self.importBox=ImportBox(self)
        try:
            if not fillImportBoxLater:
               parseToFillImportBox(
                    self,
                    noSymbolChecking,
                    recognizeUSEOCLNativeModelDefinition)

            if not parseFileLater:
                self.parseToFillModel()

        except FatalError:
            pass  # nothing to do, the issue has been registered


    @property
    def label(self):
        return self.basename

    @property
    def modelKind(self):
        return self.importBox.modelKind

    @property
    def modelName(self):
        return self.importBox.modelName

    @abstractmethod
    def parseToFillModel(self):
        #type: () -> None
        raise NotImplementedError('Method must be implemented')

    @abstractproperty
    def metamodel(self):
        #type: () -> Metamodel
        """
        The model corresponding to the parser.
        This must be implemented by all parsers.
        """
        raise NotImplementedError('Method must be implemented')

    def emptyModel(self):
        # type: () -> Model
        """
        Returns an empty model.
        """
        return self.metamodel.modelClass()  # type: Model

    @property
    def fullIssueBox(self):
        #type: () -> IssueBox
        """
        All issues including model issues.
        """
        return self.model._issueBox

    @property
    def outgoingDependencies(self):
        #type: () -> List[SourceImport]
        return self.importBox.imports

    @property
    def incomingDependencies(self):
        #type: () -> List[SourceImport]
        return Megamodel.sourceDependencies(target=self)


    @property
    def text(self):
        return self.metamodel.sourcePrinterClass(self).do()


    @classmethod
    def __dir__(self):
        # Added from ipython but this not work
        return [
            'label',
            'name']

    # label
    #
    # name
    # basename
    # directory
    # extension
    # fileName
    # path
    # length
    #
    # hasIssues
    # isValid
    # _issueBox ?
    # fullIssueBox ?
    #
    # model
    # glossaryModel
    # permissionModel
    # scenarioModel
    # usecaseModel
    # metamodel
    #
    # incomingDependencies
    # outgoingDependencies
    # importBox ?