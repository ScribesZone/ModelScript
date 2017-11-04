# coding=utf-8
"""
Manage import boxes and source imports.
Actually import source files, that is parse them
and bound them in "SourceImport".
"""
from typing import Dict, Text, List, Optional

#from modelscribes.megamodels.sources import ModelSourceFile
ModelSourceFile='ModelSourceFile'

#from modelscribes.scripts.megamodels.parser import ImportStatement
ImportStatement='ImportStatement'

from collections import OrderedDict

# XXX FIXME: th testucm_parser should raise an issue for importing a uc

from modelscribes.base.issues import (
    Levels,
    Issue
)
from modelscribes.megamodels.megamodels import Megamodel

DEBUG=1

__all__ = (
    'SourceImport',
    'ImportBox'
)

class SourceImport(object):
    """
    Basically a pair of model sources, one being
    the importing source, the other one the imported source.
    Actually perform the import, that is read and parse the
    target file.
    """
    def __init__(self, importStmt):
        #type: (ImportStatement) -> None
        """
        Create an import and actually import the
        target source file into the source file.
        Also bind the issueBox of the source towards
        to target as issues in the target are important
        for the source.
        """

        self.importStmt=importStmt #type: ImportStatement
        """ Link to the syntactic import statement """

        self.importingSourceFile=self.importStmt.sourceFile
        #type: ModelSourceFile
        """ source file that contains the import """

        self.importBox=None #type: Optional[ImportBox]
        # filled in ImportBox.addImport

        # Actually perform the import
        self.importedSourceFile= self.doImport(importStmt)
        #type: ModelSourceFile
        """ imported file. The target of the import"""

        self.doBindIssueBoxes()

        if self.importedSourceFile.issueBox.bigIssues:
            Issue(
                origin=self.importingSourceFile,
                level=Levels.Fatal,
                message='Serious issue(s) found when importing "%s"' %
                    self.importedSourceFile.basename
            )

    def doImport(self, importStmt):
        #type: (ImportStatement) -> ModelSourceFile
        """
        Actually perform the import of the target
        Create the sourceFile for the target
        This actually launch the corresponding parser
        and create the target model, etc.
        If there is a "bigIssue" than an error then a
        fatal importation error is generated.
        """
        importedFactory=importStmt.metamodel.sourceClass
        importedSourceFile=importedFactory(
            importStmt.absoluteTargetFilename)
        return importedSourceFile

    def doBindIssueBoxes(self):
        """
        bind the issuebox from importing file to imported file
        """
        self.importingSourceFile.issueBox.addParent(
            self.importedSourceFile.issueBox)
        if DEBUG>=9:
            print('DEBUG: aaa'+str(self.importingSourceFile.issueBox))

        # return

    def __repr__(self):
        return ('%s import %s' % (
                    self.importingSourceFile.basename,
                    self.importedSourceFile.basename))

    def __str__(self):
        return ('import %s model from %s' % (
            self.importStmt.metamodel.label,
            self.importStmt.literalTargetFileName
        ))


class ImportBox(object):
    """
    An import box is basically a collection of SourceImports
    for a given model source, the one containing the ImportBox.
    A convinient way to access to imported sources and models.
    The ImportBox contains as well the name of the model, and the
    kind of the model (even though strictly speaking this info
    is not linked to 'Imports'.
    """

    def __init__(self, modelSource):
        #type: (ModelSourceFile) -> None

        self.modelSource=modelSource #type: ModelSourceFile
        """ 
        Source file containing the import box.
        """

        self._modelName=None #type: Optional[Text]
        """ 
        Name of the importing model.
        This name is found in the model declaration statement.
        """
        # will be set by parseToFillImportBox

        self._modelKind=None #type: Optional[Text]
        """ 
        Model kind of the importing model. Could be for
        instance "conceptual" or "preliminary".
        This information is found in the model 
        declaration statement.
        """
        # will be set by parseToFillImportBox

        self._importsByMetamodelId=OrderedDict()
        #type: Dict[Text, List[SourceImport]]
        """
        Store the imports indexed by metamodel id.
        This attribute is private. Use instead
        addImport, imports, models, etc.
        """
        # ??? type: Dict[Text, List[ModelSourceFile]] <-- probably an error


    @property
    def modelName(self):
        #type: () -> Text
        return self._modelName

    @property
    def modelKind(self):
        #type: () -> Text
        return self._modelKind


    def setModelInfo(self, modelName, modelKind):
        """
        Set 'importing' attributes in this import box.
        Set as well the same information in the model.
        This cannot be avoided via a property for instance
        because the model may exist independently from the source.
        """
        self._modelName=modelName
        self._modelKind=modelKind
        # Fill as well the model box. It cannot be derived
        # as models can be build without any source
        self.modelSource.model.modelName = modelName
        self.modelSource.model.modelKind = modelKind
        # the metamodel metamodel should be set already

    @property
    def imports(self):
        #type: () -> List[SourceImport]
        """
        List of all source imports
        """
        return [
            i for ilist in self._importsByMetamodelId.values()
                for i in ilist ]

    def addImport(self, sourceImport_):
        #type: (SourceImport) -> None
        """
        Add a source import to this box
        """
        m2id=sourceImport_.importStmt.metamodel.id
        if m2id not in self._importsByMetamodelId:
            self._importsByMetamodelId[m2id]=[]
        self._importsByMetamodelId[m2id].append(sourceImport_)
        sourceImport_.importBox=self
        # TODO: the megamodel and model dependencies should
        # be updated

    # TODO: improve the methods based on metamodel dependencies
    def sourceImports(self, id):
        #type: (Text) -> List[SourceImport]
        """
        Return all sourceImports for a given metamodel id.
        None if no sourcesImport for this id.
        """
        if id not in self._importsByMetamodelId:
            return []
        else:
            return self._importsByMetamodelId[id]

    def sourceImport(self, id, optional=True):
        #type: (Text) -> Optional[SourceImport]
        """
        Return "the one and only one" sourceImport for a
        given metamodel id.
        If there is no sourceImport then add an issue,
        unless optional is True in which case None is returned.
        If there is more than one sourceImport then an issue
        is added.
        """
        metamodel_label = Megamodel.metamodel(id=id).label
        if id not in self._importsByMetamodelId:
            if optional:
                return None
            else:
                Issue(
                    origin=self.modelSource,
                    level=Levels.Fatal,
                    message=
                        'No %s model imported.' % metamodel_label )
        r=self._importsByMetamodelId[id]
        if len(r)==1:
            return r[0]
        else:
            Issue(
                origin=self.modelSource,
                level=Levels.Fatal,
                message=
                    'More than on %s model imported.' % metamodel_label)

    def sources(self, id):
        return [
            s.importedSourceFile for s in self.sourceImports(id)]

    def source(self, id, optional=False):
        si=self.sourceImport(id, optional=optional)
        if si is None:
            return None
        else:
            return si.importedSourceFile

    def models(self, id):
        return [s.importedSourceFile.model for s in self.sourceImports(id)]

    def model(self, id, optional=False):
        si=self.sourceImport(id, optional=optional)
        if si is None:
            return None
        else:
            return si.importedSourceFile.model

