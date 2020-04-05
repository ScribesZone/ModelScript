# coding=utf-8
"""Manage "SourceImports" and "ImportBoxes".

A SourceImport is a concrete implementation of
"SourceFileDependency". It is materialized by a
statement like "import usecase model from "<file>"
(the actual format is defined in the megamodel parser).

A import box is basically a list of source import.

This module actually import source files: is parse them
and bound them in "SourceImport".
"""

from typing import Dict, Text, List, Optional
from abc import ABCMeta
from collections import OrderedDict

from modelscript.megamodels.dependencies import Dependency
from modelscript.megamodels.dependencies.models import ModelDependency
from modelscript.base.issues import (
    Levels,
    Issue)
from modelscript.base.exceptions import (
    NotFound)

ModelSourceFile = 'ModelOldSourceFile'
ImportStatement = 'ImportStatement'

__all__ = (
    'SourceFileDependency',
    'SourceImport',
    'ModelDescriptor',
    'ImportBox'
)

# FIXME:1 test_ucm_parser should raise an issue for importing a uc

DEBUG = 1


class SourceFileDependency(Dependency, metaclass=ABCMeta):
    """A pair of source files representing a dependency between
    these two files. Abstract class extended by SourceImport.
    """

    importingSourceFile: ModelSourceFile
    """Source file that contains the import """

    importedSourceFile: ModelSourceFile
    """ Imported source file. The target of the import"""

    def __init__(self,
                 importingSourceFile: ModelSourceFile,
                 importedSourceFile: ModelSourceFile) -> None:
        """ Create the dependency and register it in the metamodel.
        """
        self.importingSourceFile = importingSourceFile
        self.importedSourceFile = importedSourceFile

        from modelscript.megamodels import Megamodel
        Megamodel.registerSourceFileDependency(self)

        # register model dependency if not already there
        # (it should not be there)

        sm = self.importingSourceFile.model
        tm = self.importedSourceFile.model
        if Megamodel.modelDependency(sm, tm) is None:
            d = ModelDependency(sm, tm)
            Megamodel.registerModelDependency(d)


    @property
    def source(self):
        #type: () -> ModelSourceFile
        return self.importingSourceFile

    @property
    def target(self):
        #type: () -> ModelSourceFile
        return  self.importedSourceFile


class SourceImport(SourceFileDependency):
    """Semantical element corresponding to an ImportStatement.
    """

    importStmt: ImportStatement
    """ Link to the syntactic import statement """

    importBox: Optional['ImportBox']
    """Back reference to the containing import box """

    def __init__(self, importStmt: ImportStatement) -> None:
        """Create an SourceImport and actually perform the
        import of target source file.

        The importStmt given as a concrete parameter is the concrete
        representation of this SourceImport. The importStmt is
        a syntactic element located in the source file.
        The ImportStatement is created by the megamodel parser.

        If the target source file is not already registered
        in the megamodel then the target is read and a
        ModelSourceFile is therefore created.
        This possibly could generate some issues but these
        are stored in the target ModelSourceFile.

        The _issueBox of the importing ModelSourceFile is
        linked to the one of the target. This allows tHE
        source to "see" issues produced in the target.
        """

        self.importStmt = importStmt

        self.importBox = None
        # filled in ImportBox.addImport

        # get the target SourceFile object
        try:

            # --- case 1: imported file is already registered
            #   just get it:
            from modelscript.megamodels import Megamodel
            imported_source_file = Megamodel.sourceFile(
                importStmt.absoluteTargetFilename)

        except NotFound :

            # --- case 2: imported file has never been registered!
            #    process it and get it
            origin_sourcefile = importStmt.modelSourceFile
            used_metamodels = origin_sourcefile.allUsedMetamodels
            # print('QQ'*40+'Importing '+str(importStmt))
            imported_source_file = self._doImport(importStmt)

        super(SourceImport, self).__init__(
            self.importStmt.modelSourceFile,
            imported_source_file
        )

        # --- not more used
        # The parent relationship is not good enough to represent
        # a dag with various sources and share parent
        # "parent" beetween imported issue box has been desactivated
        # It only remains for model/source.
        #
        # self._doBindIssueBoxes()

    def _doImport(self,
                  importStmt: ImportStatement)\
            -> ModelSourceFile:
        """Actually perform the import of the target
        Create the sourceFile for the target
        This actually launch the corresponding parser
        and create the target model, etc.
        If there is a "bigIssue" than an error then a
        fatal importation error is generated.
        """
        imported_factory = importStmt.metamodel.sourceClass
        imported_source_file = imported_factory(
            importStmt.absoluteTargetFilename)
        return imported_source_file

    def _doBindIssueBoxes(self):
        """Bind the issuebox from importing file to imported file
        """
        self.importingSourceFile.issues.addParent(
            self.importedSourceFile.issues)

    def __repr__(self):
        return ('%s import %s' % (
                    self.importingSourceFile.basename,
                    self.importedSourceFile.basename))

    def __str__(self):
        return ('import %s model from %s' % (
            self.importStmt.metamodel.label,
            self.importStmt.literalTargetFileName
        ))


class ModelDescriptor(object, metaclass=ABCMeta):

    _modelName: Optional[Text]
    """Name of the importing model.
    This name is found in the model declaration statement.
    It is set by the method setModelInfo().
    """

    _modelKinds: List[Text]
    """Model kinds of the importing model. A list of label like
    instance "draft", "conceptual" or "preliminary".
    This information is found in the model 
    definition statement. It will be set by
    the method parseToFillImportBox() in the model source
    which call setModelInfo().
    """


    _modelDescription: Optional[Text]

    def __init__(self):

        self._modelName = None
        # will be set by parseToFillImportBox

        self._modelKinds = []

        self._modelDescription = None

    @property
    def modelName(self) -> Text:
        return self._modelName

    @property
    def modelKinds(self) -> List[Text]:
        return self._modelKinds

    def setModelInfo(self, modelName, modelKinds, modelDescription):
        """Set description.
        """
        self._modelName = modelName
        self._modelKinds = modelKinds
        self._modelDescription = modelDescription


class ImportBox(ModelDescriptor):
    """An import box is like a collection of SourceImports
    but for a given model source, the one containing the
    ImportBox.
    A convenient way to access to imported sources and models.

    The ImportBox contains as well:

    *   the name of the model,

    *   and the kind of the model (even though strictly speaking this
        information is not linked to 'Imports'. (Not found a
        better place to put these attributes and a better name
        for ImportBox)
    """

    modelSource: ModelSourceFile
    """Source file containing the import box. """

    _importsByMetamodelId: Dict[Text, List[SourceImport]]
    """ Imports indexed by metamodel id.
    This attribute is private. Use instead addImport, imports, models, etc.
    """

    def __init__(self, modelSource: ModelSourceFile) -> None:
        """ Creates an empty ImportBox for a given ModelSourceFile.
        """
        super(ImportBox, self).__init__()
        self.modelSource = modelSource
        self._importsByMetamodelId = OrderedDict()

    @property
    def imports(self) -> List[SourceImport]:
        """ List of all SourceImports starting from this
        ImportBox, that is, from the corresponding.
        ModelOldSourceFile.
        """
        return [
            #TODO:4 2to3 was self._importsByMetamodelId.values()
            i for ilist in list(self._importsByMetamodelId.values())
                for i in ilist ]

    def setModelInfo(self, modelName, modelKinds, modelDescription):
        super(ImportBox, self).setModelInfo(
            modelName,
            modelKinds,
            modelDescription)
        # Fill as well the model box. It cannot be derived
        # as models can be build without any source
        # This cannot be avoided via a property for instance
        # because the model may exist independently from
        # the source.
        self.modelSource.model.name = modelName
        self.modelSource.model.description = modelDescription
        self.modelSource.model.kinds = modelKinds

    def addImport(self, sourceImport_: SourceImport) -> None:
        """ Add a source import to this box
        """
        m2id = sourceImport_.importStmt.metamodel.id
        if m2id not in self._importsByMetamodelId:
            self._importsByMetamodelId[m2id]=[]
        self._importsByMetamodelId[m2id].append(sourceImport_)
        sourceImport_.importBox = self
        # TODO:4 update megamodel/model dependencies


    # TODO:4 improve the methods based on metamodel dependencies
    def sourceImports(self, id_: str) -> List[SourceImport]:
        """Return all sourceImports for a given metamodel id.
        None if no sourcesImport for this id.
        """
        if id_ not in self._importsByMetamodelId:
            return []
        else:
            return self._importsByMetamodelId[id_]

    def sourceImport(self,
                     id_: str,
                     optional: bool =True) \
            -> Optional[SourceImport]:
        """Return "the one and only one" sourceImport for a
        given metamodel id.
        If there is no sourceImport then add an issue,
        unless optional is True in which case None is returned.
        If there is more than one sourceImport then an issue
        is added.
        """
        from modelscript.megamodels import Megamodel
        metamodel_label = Megamodel.theMetamodel(id=id_).label
        if id_ not in self._importsByMetamodelId:
            if optional:
                return None
            else:
                Issue(
                    origin=self.modelSource,
                    level=Levels.Fatal,
                    message=
                        'No %s model imported.' % metamodel_label )
        r=self._importsByMetamodelId[id_]
        if len(r)==1:
            return r[0]
        else:
            Issue(
                origin=self.modelSource,
                level=Levels.Fatal,
                message=
                    'More than on %s model imported.' % metamodel_label)

    def sourceFiles(self, id) -> List[ModelSourceFile]:
        """Returns the list of all source files imported for
        a given metamodel id.
        """
        return [
            s.importedSourceFile for s in self.sourceImports(id)]

    def sourceFile(self,
                   id_: str,
                   optional: bool = False)\
            -> Optional[ModelSourceFile]:
        """Return "the one and only one" source file for a
        given metamodel id. If there is no such source file
        then return None. If there are more than one source
        file then produce a fatal issue.
        """
        si = self.sourceImport(id_, optional=optional)
        if si is None:
            return None
        else:
            return si.importedSourceFile

    def models(self, id_):
        """Returns the list of all models imported for
        a given metamodel id.
        """
        return [s.importedSourceFile.model
                for s in self.sourceImports(id_)]

    def model(self, id_, optional=False):
        """Returns "the one and only one" model imported for
        a given metamodel id.  If there is no such model
        then return None. If there are more than one
        then produce a fatal issue.
        """
        si=self.sourceImport(id_, optional=optional)
        if si is None:
            return None
        else:
            return si.importedSourceFile.model

