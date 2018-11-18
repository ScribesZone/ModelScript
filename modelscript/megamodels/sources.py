# coding=utf-8
"""
Source files for models.
Additionally to a regular source files, a ModelOldSourceFile
contains:

*   an attribute `model` containing the model resulting from
    parsing the source file,
*   an _issueBox containing all import statements.
*   the model declaration statement.
"""
from typing import Text, Optional, List, Any, Union, Dict, Set
from abc import ABCMeta, abstractproperty, abstractmethod
import collections
import sys
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

__all__=(
    'ASTBasedModelSourceFile',
)


class ASTBasedModelSourceFile(SourceFile):

    """
    A source file with a model, and an AST.

    * a fileName (inherited)
    * sourceLines (inherited)
    * issueBox (inherited)
    * a model,
    * an importBox and
    * an AST
    """
    __metaclass__ = ABCMeta

    def __init__(self,
                 fileName,
                 grammarFile):
        #type: (Text, Text) -> None
        """
        An empty model is created automatically.
        This model is associated with this source file.
        This empty model is created according to
        the metamodel specified by the property 'metamodel'.

        An importBox is also created.
        In order to do this the content of the source file is
        parsed looking the declaration of the model name as
        well as import statements. All this information is
        stored in the importBox.
        """

        #----- (0) create an empty model ---------

        # Create an empty model
        # Not to be moved after super
        # This should be done in all case so that
        # the model attribute always exist even if there
        # are some error in reading the file
        self.model = self.emptyModel()  # type: Model


        #----- (1) read the file ------------------
        # Call the super class. Basically read the file.
        try:
            # This can raise an exception for instance if
            # there is a problem reading the file
            super(ASTBasedModelSourceFile, self).__init__(
                fileName=fileName
            )
        except FatalError:
            pass   # an error as already been registered
        super(ASTBasedModelSourceFile, self).__init__(
            fileName=fileName)

        #----- (2) register/link models/sources/issues----

        from modelscript.megamodels import Megamodel
        Megamodel.registerSourceFile(self)
        Megamodel.registerModel(self.model)

        # Backward link
        self.model.source=self

        # Link issue box
        self.model._issueBox.addParent(self._issueBox)

        # Source to ModelElement Mapping
        self._modelMapping=_ModelSourceMapping()

        #----- (2) syntactic parsing, create the ast
        self.grammarFile=grammarFile
        #type: Text

        # Create first an empty ImportBox.
        self.importBox=ImportBox(self)

        # Then fill it by reading megamodel statements,
        # unless specified.

        # removed this code
        try:
            self.fillAST()
            fillDependencies(self)
            self.fillModel()
            self.resolve()
            self.finalize()
        except FatalError:
            pass  # nothing to do, the issue has been registered


    def resolve(self):
        self.model.resolve()

    def finalize(self):
        self.model.finalize()

    def _addSourceModelElement(self, sme):
        #type: (SourceModelElement) -> None
        self._modelMapping.add(sme)

    def atLine(self, line, unique=True):
        #type: (Optional[int], bool) -> Union[Optional[SourceModelElement], List[SourceModelElement]]
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

    def fillAST(self):
        from modelscript.base.grammars import (Grammar, ModelSourceAST)
        self.grammar=Grammar(self.grammarFile)
        #type: Grammar
        try:
            self.ast = ModelSourceAST(self.grammar, self, self.fileName)
        except TextXSyntaxError as e:
            from modelscript.base.grammars import AST
            err=AST.extractErrorFields(e)
            LocalizedSourceIssue(
                code='src.syn',
                sourceFile=self,
                level=Levels.Fatal,
                message='Syntax error. %s' % err.message,
                line=err.line,
                column=err.column)
        except BracketError as e:
            LocalizedSourceIssue(
                code='src.bra',
                sourceFile=self,
                level=Levels.Fatal,
                message='Wrong indentation. %s' % e.message,
                line=e.line)

    @abstractmethod
    def fillModel(self):
        #type: () -> None
        raise MethodToBeDefined( #raise:OK
            'fillModel() must be implemented')

    @abstractproperty
    def metamodel(self):
        #type: () -> Metamodel
        """
        The model corresponding to the parser.
        This must be implemented by all parsers.
        """
        raise MethodToBeDefined( #raise:OK
            'metamodel() must be implemented')

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
        from modelscript.megamodels import Megamodel
        return Megamodel.sourceDependencies(target=self)

    @property
    def usedSourceFiles(self):
        #type: () -> List[SourceFile]
        return [ dep.target
                 for dep in self.outgoingDependencies ]

    @property
    def allUsedSourceFiles(self):
        #type: () -> Set[SourceFile]
        all=set()
        for us in self.usedSourceFiles:
            all=all.union(us.allUsedSourceFiles)
        return all

    @property
    def allUsedMetamodels(self):
        #type: ()-> Set[Metamodel]
        return [
            sf.metamodel for sf in self.allUsedSourceFiles]

    @property
    def usingSourceFiles(self):
        #type: () -> [SourceFile]
        return [ dep.source
                 for dep in self.incomingDependencies ]

    @property
    def metrics(self):
        """ Return metrics that are specific to source files """
        return Metrics().add(
            Metric('source line',len(self.sourceLines))
        )

    @property
    def fullMetrics(self):
        #type: () -> Metrics
        """ Return metrics both for source file and for the model """
        ms=self.metrics
        if self.model is not None:
            ms.addMetrics(self.model.metrics)
        return ms

    @property
    def text(self):
        return self.metamodel.sourcePrinterClass(self).do()


    def str( self,
             method='do',
             config=None
            ):
        printer_class=self.metamodel.sourcePrinterClass
        printer=printer_class(
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
#     @abstractproperty
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



class _ModelSourceMapping(object):

    def __init__(self):
        self._sourceModelElementsAtLine=(
            collections.OrderedDict())
        #type: Dict[int, List[SourceModelElement]]

    def add(self, sourceModelElement):
        # Line 0 serve as elements with no lineNo specified
        line=sourceModelElement.lineNo
        if line is None or line==0:
            line=0
        if not line in self._sourceModelElementsAtLine:
            self._sourceModelElementsAtLine[line]=[]
        self._sourceModelElementsAtLine[line].append(
            sourceModelElement
        )

    def atLine(self, line, unique=True):
        #type: (Optional[int], bool) -> Union[Optional[SourceModelElement], List[SourceModelElement]]
        """
        Return the source model element(s) at line S.
        Because most of the time 1 element at most is
        expected the parameter unique return only one
        element or None with an exception otherwise.
        Since it is execpted to have various elements
        at line 0/None, then always return a list.
        """
        # Line 0 serve as elements with no lineNo specifiecd
        if line is None or line==0:
            line=0
        if line not in self._sourceModelElementsAtLine:
            elems=[]
        else:
            elems=self._sourceModelElementsAtLine[line]
        if unique and line!=0:
            assert(len(elems)<=1)
            return None if len(elems)==0 else elems[0]
        else:
            return elems

        # if line not in self._sourceModelElementsAtLine:
        #     return None if unique else []
        # if line==0:
        #     # return always a list
        #     return list(self._sourceModelElementsAtLine[0])
        # elems=self._sourceModelElementsAtLine[line]




