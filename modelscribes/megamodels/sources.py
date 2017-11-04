# coding=utf-8
"""
Source files for models. Additionally to a regular source files,
a ModelSourceFile contains:

*   an attribute `model` containing the model resulting from
    parsing the source file,
*   an issueBox containing all import statements
*   the model declaration statement.
"""
from typing import Text, Optional, List, Any
from abc import ABCMeta, abstractproperty, abstractmethod

from modelscribes.base.sources import SourceFile
from modelscribes.base.issues import (
    IssueBox,
    FatalError
)
from modelscribes.megamodels.metamodels import (
    Metamodel
)
from modelscribes.megamodels.models import (
    Model
)
from modelscribes.megamodels.dependencies.sources import (
    ImportBox
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

        Create also an importBox.
        In order to do this the content of the source file is
        parsed looking the declaration of the model name as
        well as import statements. All this information is
        stored in the importBox.

        If `fillImportBoxLater` is True then this importBox
        is left empty. The client have to call explicitly
        parseToFillImportBox() when possible.

        The parameter recognizeUSEOCLNativeModelDefinition
        is a patch to allow parsing regular .use file.
        This patch could be removed if .use files are generated.



        Args:
            fileName:
                The logical name of the file.
                This is not necessarily the file parsed.
            realFileName:
                The real file to be read. If the reading
                has to be postponed, then the parameter
                should be set to None. The doRealFileRead()
                will set this parameter
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

        """


        # Create an empty model
        # Not to be moved after super
        # This should be done in all case so that
        # the model attribute always exist even if there
        # are some error in reading the file
        self.model=self.metamodel.modelClass()  #type: Model



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

        # Backward link & issue box linking
        self.model.source=self
        self.model.issueBox.addParent(self.issueBox)


        # Create an empty ImportBox and fill it unless specified
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
        raise NotImplementedError('Method must be implemented')

    @property
    def fullIssueBox(self):
        #type: () -> IssueBox
        """
        All issues including model issues.
        """
        return self.model.issueBox
