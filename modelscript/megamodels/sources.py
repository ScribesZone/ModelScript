# coding=utf-8
"""Source files for models.
"""
from typing import Text, Optional, List, Any, Union, Dict, Set
from abc import ABCMeta, abstractmethod
import collections

from textx.exceptions import TextXSyntaxError

from modelscript.base.sources import SourceFile
from modelscript.base.metrics import (
    Metrics,
    Metric)
from modelscript.base.issues import (
    IssueBox,
    FatalError,
    LocalizedSourceIssue,
    Levels)
from modelscript.base.brackets import (
    BracketError)
from modelscript.megamodels.models import (
    Model)
from modelscript.megamodels.dependencies.sources import (
    ImportBox,
    SourceImport)
from modelscript.megamodels.elements import (
    SourceModelElement)
from modelscript.scripts.megamodels.parser import (
    fillDependencies)
from modelscript.megamodels.metamodels import (
    Metamodel)
from modelscript.base.exceptions import (
    MethodToBeDefined,
    UnexpectedCase)

__all__ =(
    'ASTBasedModelSourceFile',
)


class ASTBasedModelSourceFile(SourceFile, metaclass=ABCMeta):
    """A source file with a model and an AST.

    An ASTBasedModelSourceFile contains :
    * a fileName (inherited from SourceFile)
    * sourceLines (inherited from SourceFile)
    * issueBox (inherited from SourceFile)
    * a model,
    * an importBox and
    * an AST
    """

    model: Model
    grammarFile: str
    grammar: 'Grammar'      # from modelscript.base.grammars
    ast: 'ModelSourceAST'   # from modelscript.base.grammars
    importBox: ImportBox

    def __init__(self,
                 fileName: str,
                 grammarFile: str) -> None:

        """Creates a ASTBasedModelSourceFile.

        An empty model is created automatically.
        This model is associated with this source file.
        This empty model is created according to
        the metamodel specified by the property 'metamodel'.

        Read the given file and creates a AST.

        An importBox is also created.
        In order to do this the content of the source file is
        parsed looking the declaration of the model name as
        well as import statements. All this information is
        stored in the importBox.

        Register the model and the source file into the megamodel.

        Link the source issueBox as a parent of the model' issueBox
        """

        # ----- (0) Create an empty model -------------------------------

        # Create an empty model.
        # The code must not be moved after super(...)
        # This should be done in all cases so that
        # the "model" attribute always exist even if there
        # are some errors in reading the file.
        self.model = self.emptyModel()

        # ----- (1) read the file ---------------------------------------
        # Call the super class. Basically read the file.
        try:
            # This can raise an exception for instance if
            # there is a problem reading the file.
            super(ASTBasedModelSourceFile, self).__init__(
                fileName=fileName)
        except FatalError:
            # An issue has already been registered.
            # So there is nothing to do here.
            pass
        # super(ASTBasedModelSourceFile, self).__init__(
        #     fileName=fileName) #CHECK232

        # ----- (2) register/link models/sources/issues------------------

        from modelscript.megamodels import Megamodel
        Megamodel.registerSourceFile(self)
        Megamodel.registerModel(self.model)

        # Backward link
        self.model.source = self

        # Link issue box
        self.model._issueBox.addParent(self._issueBox)

        # Source to ModelElement Mapping
        self._modelMapping = _ModelSourceMapping()

        # ----- (3) syntactic parsing, create the ast -------------------
        self.grammarFile = grammarFile

        # Create first an empty ImportBox.
        self.importBox = ImportBox(self)

        # Then fill it by reading megamodel statements,
        # unless specified.

        mode = Megamodel.analysisLevel
        # removed this code
        try:
            self.fillAST()
            if mode != 'justAST':
                fillDependencies(self)
                if mode != 'justASTDep':
                    self.fillModel()
                    self.resolve()
                    self.finalize()
        except FatalError:
            pass  # nothing to do, the issue has been registered


    def _addSourceModelElement(self, sme: SourceModelElement) -> None:
        self._modelMapping.add(sme)

    def atLine(self,
               line: Optional[int],
               unique: bool = True) \
            -> Union[Optional[SourceModelElement],
                     List[SourceModelElement]]:
        """
        Return the source model element(s) at line S.
        Because most of the time 1 element at most is
        expected the parameter unique return only one
        element or None with an exception otherwise.
        Since it is normal to have various elements
        at line 0/None, then always return a list.
        """
        return self._modelMapping.atLine(line, unique)

    @property
    def label(self):
        return self.basename

    @property
    def modelKinds(self):
        return self.importBox.modelKinds

    @property
    def modelName(self):
        return self.importBox.modelName

    def fillAST(self)  -> None :
        """Parse the source file and create the AST.
        Bracket and syntax error are converted to LocalizedSourceIssue"""
        from modelscript.base.grammars import (
            Grammars,
            ModelSourceAST)
        self.grammar = Grammars.get(self.grammarFile)
        try:
            self.ast = ModelSourceAST(self.grammar, self, self.fileName)
        except TextXSyntaxError as e:
            from modelscript.base.grammars import AST
            err = AST.extractErrorFields(e)
            LocalizedSourceIssue(
                code='src.syn',
                sourceFile=self,
                level=Levels.Fatal,
                message='Syntax error. %s' % str(err),
                line=err.line,
                column=err.column)
        except BracketError as e:
            LocalizedSourceIssue(
                code='src.bra',
                sourceFile=self,
                level=Levels.Fatal,
                message='Wrong indentation. %s' % str(e),
                line=e.line)

    @abstractmethod
    def fillModel(self) -> None:
        raise MethodToBeDefined(  # raise:OK
            'fillModel() must be implemented')

    def resolve(self):
        """Resolves the model."""
        self.model.resolve()

    def finalize(self):
        """Finalize the model."""
        self.model.finalize()

    @property
    @abstractmethod
    def metamodel(self) -> Metamodel:
        """The model corresponding to the parser.
        This must be implemented by all parsers.
        """
        raise MethodToBeDefined( #raise:OK
            'metamodel() must be implemented')

    def emptyModel(self) -> Model:
        """Returns an empty model. """
        return self.metamodel.modelClass()  # type: Model

    @property
    def fullIssueBox(self) -> IssueBox:
        """All issues including model issues. """
        return self.model._issueBox

    @property
    def outgoingDependencies(self) -> List[SourceImport]:
        return self.importBox.imports

    @property
    def incomingDependencies(self) -> List[SourceImport]:
        from modelscript.megamodels import Megamodel
        return Megamodel.sourceDependencies(target=self)

    @property
    def usedSourceFiles(self) -> List[SourceFile]:
        return [dep.target
                for dep in self.outgoingDependencies]

    @property
    def allUsedSourceFiles(self) -> Set[SourceFile]:
        _all = set()
        for us in self.usedSourceFiles:
            _all = _all.union(us.allUsedSourceFiles)  # TODO:2 check type
        return _all

    @property
    def allUsedMetamodels(self) -> Set[Metamodel]:
        return set([
            sf.metamodel for sf in self.allUsedSourceFiles])  # TODO:2 check type

    @property
    def usingSourceFiles(self) -> [SourceFile]:
        return [dep.source
                 for dep in self.incomingDependencies]

    @property
    def metrics(self) -> Metrics:
        """Metrics that are specific to source files """
        return Metrics().add(
            Metric('source line', len(self.sourceLines))
        )

    @property
    def fullMetrics(self) -> Metrics:
        """Metrics both for source file and for the model """
        ms=self.metrics
        if self.model is not None:
            ms.addMetrics(self.model.metrics)
        return ms

    @property
    def text(self):
        return self.metamodel.sourcePrinterClass(self).do()

    def str(self,
             method='do',
             config=None
            ):
        printer_class = self.metamodel.sourcePrinterClass
        printer = printer_class(
            theSource=self,
            config=config,
        )
        try:
            the_method = getattr(printer_class, method)
            return the_method(printer)
        except AttributeError:
            raise MethodToBeDefined(  # raise:OK
                "Class `{}` does not implement `{}`".format(
                    printer_class.__class__.__name__,
                    method))


class _ModelSourceMapping(object):

    _sourceModelElementsAtLine: Dict[int, List[SourceModelElement]]

    def __init__(self):
        self._sourceModelElementsAtLine = (
            collections.OrderedDict())

    def add(self, sourceModelElement):
        # Line 0 serve as elements with no lineNo specified
        line = sourceModelElement.lineNo
        if line is None or line == 0:
            line = 0
        if line not in self._sourceModelElementsAtLine:
            self._sourceModelElementsAtLine[line] = []
        self._sourceModelElementsAtLine[line].append(
            sourceModelElement
        )

    def atLine(self,
               line: Optional[int],
               unique: bool = True) \
            -> Union[Optional[SourceModelElement],
                     List[SourceModelElement]]:
        """
        Return the source model element(s) at line S.
        Because most of the time 1 element at most is
        expected the parameter unique return only one
        element or None with an exception otherwise.
        Since it is expected to have various elements
        at line 0/None, then always return a list.
        """
        # Line 0 serve as elements with no lineNo specifiecd
        if line is None or line == 0:
            line = 0
        if line not in self._sourceModelElementsAtLine:
            elems = []
        else:
            elems = self._sourceModelElementsAtLine[line]
        if unique and line != 0:
            assert(len(elems) <= 1)
            return None if len(elems) == 0 else elems[0]
        else:
            return elems

        # if line not in self._sourceModelElementsAtLine:
        #     return None if unique else []
        # if line==0:
        #     # return always a list
        #     return list(self._sourceModelElementsAtLine[0])
        # elems=self._sourceModelElementsAtLine[line]




# class NewModelSourceFile(SourceFile):
#
#     """
#     A source file with a model.
#
#     * a fileName (inherited)
#     * sourceLines (inherited)
#     * issueBox (inherited)
#     * a model,
#     * an importBox and
#     * a model declaration.
#     """
#     __metaclass__ = ABCMeta
#
#     def __init__(self,
#                  fileName,
#                  fillImportBoxLater=False,
#                  parseFileLater=False):
#         #type: (Text, Optional[Text], Optional[Text], bool, bool, bool) -> None
#         """
#         An empty model is created automatically.
#         This model is associated with this source file.
#         This empty model is created according to
#         the metamodel specified by the property 'metamodel'.
#
#         An importBox is also created.
#         In order to do this the content of the source file is
#         parsed looking the declaration of the model name as
#         well as import statements. All this information is
#         stored in the importBox.
#
#         If `fillImportBoxLater` is True then this importBox
#         is left empty for the moment. The client have
#         to call explicitly parseToFillImportBox() later.
#
#
#         Args:
#             fileName:
#                 The name of the file.
#             readFileLater:
#                 If False the file is read directly.
#                 Otherwise the method doReadFile() must be called!
#             fillImportBoxLater:
#                 If False, the file read is parsed to find
#                 megamodel statements (e.g. import) and to
#                 fill the import box.
#                 If not parseToFillImportBox() must be called
#                 after reading the file, and this in order to
#                 get the imported model.
#         """
#
#         # Create an empty model
#         # Not to be moved after super
#         # This should be done in all case so that
#         # the model attribute always exist even if there
#         # are some error in reading the file
#         self.model = self.emptyModel()  # type: Model
#
#
#         # Call the super class. Basically read the file.
#         try:
#             # This can raise an exception for instance if
#             # there is a problem reading the file
#             super(NewModelSourceFile, self).__init__(
#                 fileName=fileName
#             )
#         except FatalError:
#             pass   # an error as already been registered
#
#         from modelscript.megamodels import Megamodel
#         Megamodel.registerSourceFile(self)
#         Megamodel.registerModel(self.model)
#
#
#         # Backward link
#         self.model.source=self
#
#         # Link issue box
#         self.model._issueBox.addParent(self._issueBox)
#
#         # Source to ModelElement Mapping
#         self._modelMapping=_ModelSourceMapping()
#
#
#         # Create first an empty ImportBox.
#         self.importBox=ImportBox(self)
#
#         # Then fill it by reading megamodel statements,
#         # unless specified.
#         try:
#             if not fillImportBoxLater:
#                fillDependencies(self)
#
#             if not parseFileLater:
#                 self.parseToFillModel()
#                 self.finalize()
#
#         except FatalError:
#             pass  # nothing to do, the issue has been registered
#
#     def finalize(self):
#         self.model.finalize()
#
#     def _addSourceModelElement(self, sme):
#         #type: (SourceModelElement) -> None
#         self._modelMapping.add(sme)
#
#     def atLine(self, line, unique=True):
#         #type: (Optional[int], bool) -> Union[Optional[SourceModelElement], List[SourceModelElement]]
#         """
#         Return the source model element(s) at line S.
#         Because most of the time 1 element at most is
#         expected the parameter unique return only one
#         element or None with an exception otherwise.
#         Since it is normal to have various elements
#         at line 0/None, then always return a list.
#         """
#         return self._modelMapping.atLine(line, unique)
#
#
#     @property
#     def label(self):
#         return self.basename
#
#     @property
#     def modelKind(self):
#         return self.importBox.modelKind
#
#     @property
#     def modelName(self):
#         return self.importBox.modelName
#
#     @abstractmethod
#     def parseToFillModel(self):
#         #type: () -> None
#         raise NotImplementedError('Method must be implemented')
#
#     @property
#     @abstractmethod
#     def metamodel(self):
#         #type: () -> Metamodel
#         """
#         The model corresponding to the parser.
#         This must be implemented by all parsers.
#         """
#         raise NotImplementedError('Method must be implemented')
#
#     def emptyModel(self):
#         # type: () -> Model
#         """
#         Returns an empty model.
#         """
#         return self.metamodel.modelClass()  # type: Model
#
#     @property
#     def fullIssueBox(self):
#         #type: () -> IssueBox
#         """
#         All issues including model issues.
#         """
#         return self.model._issueBox
#
#     @property
#     def outgoingDependencies(self):
#         #type: () -> List[SourceImport]
#         return self.importBox.imports
#
#     @property
#     def incomingDependencies(self):
#         #type: () -> List[SourceImport]
#         return Megamodel.sourceDependencies(target=self)
#
#     @property
#     def metrics(self):
#         return Metrics().add(
#             Metric('source line',len(self.sourceLines))
#         )
#
#     @property
#     def fullMetrics(self):
#         #type: () -> Metrics
#         ms=self.metrics
#         if self.model is not None:
#             ms.addMetrics(self.model.metrics)
#         return ms
#
#     @property
#     def text(self):
#         return self.metamodel.sourcePrinterClass(self).do()
#
#
#     def str( self,
#              method='do',
#              config=None
#             ):
#         printer_class=self.metamodel.sourcePrinterClass
#         printer=printer_class(
#             theSource=self,
#             config=config,
#         )
#         try:
#             the_method = getattr(printer_class, method)
#             return the_method(printer)
#         except AttributeError:
#             raise NotImplementedError(
#                 "Class `{}` does not implement `{}`".format(
#                     printer_class.__class__.__name__,
#                     method))

