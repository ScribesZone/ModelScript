# coding=utf-8
"""
Source files for models. Additional to regular source files,
a ModelSourceFile contains an attribute `model` containing
the model resulting from parsing the sourc file, as well
as an issueBox containg all import statement and the
model declaration statement.
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
    A source file with a model and an importBox.
    
    An empty model is created automatically and it
    is associated with this source file.
    This empty model is created according to 
    the metamodel specificed by the property 'metamodel'.
    
    This initializer create also an importBox.
    In order to do this the content of the source file is
    parsed looking the declaration of the model name as
    well as import statements. All this information is
    stored in the importBox.
    If `fillImportBoxLater` is True then this importBox
    is left empty. The client have to call explictely
    parseToFillImportBox()
    when possible.

    The parameter recognizeUSEOCLNativeModelDefinition
    is a patch to allow parsing regular .use file.
    This patch could be removed if .use files are generated.
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
                 recognizeUSEOCLNativeModelDefinition=False):
        #type: (Text, Optional[Text], List[Any], bool) -> None


        # Create an empty model
        # Not to be moved after super
        # This should be done in all case so that
        # the model attribute always exit even if there
        # are some error in reading the file
        self.model=self.metamodel.modelClass()  #type: Model

        try:
            # This can raise an exception fir instance if
            # there is a problem reading the file
            super(ModelSourceFile, self).__init__(
                fileName=fileName,
                realFileName=realFileName,
                preErrorMessages=preErrorMessages,
                doNotReadFile=readFileLater
            )
        except FatalError:
            pass

        # Backward link & issue box linking
        self.model.source=self
        self.model.issueBox.addParent(self.issueBox)

        # Create an empty ImportBox and fill it unless specified
        self.importBox= ImportBox(self)


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
        All issues including model issues if present
        """
        # if not self.model is not None:
        #     # the sources issues are already in the model isses
        #     # print('********** fullIssueBox for model -> %s ' % self.model.issueBox.parent)
        return self.model.issueBox
        # else:
        #     # print('********** fullIssueBox no model ' )
        #     return self.issueBox

    @abstractproperty
    def megamodelStatementPrefix(self):
        raise NotImplementedError('Method must be implemented')


