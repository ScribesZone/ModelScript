# coding=utf-8
from typing import Dict, Text, List, Optional

#from modelscribes.megamodels.sources import ModelSourceFile
ModelSourceFile='ModelSourceFile'

#from modelscribes.scripts.megamodels.parser import ImportStatement
ImportStatement='ImportStatement'

from collections import OrderedDict

# XXX FIXME: th testucm_parser should raise an issue for importing a uc

__all__ = (
    'SourceImport',
    'ImportBox'
)

class SourceImport(object):
    """
    Basically a pair of model sources, one being
    the importing source, the other one the imported source.
    """
    def __init__(self, importStmt):
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

        #-------- actually perform the import ------------
        # Create the sourceFile for the target
        # This actually launch the corresponding parser
        # and create the target model, etc.
        importedFactory=importStmt.metamodel.sourceClass

        self.importedSourceFile=importedFactory(
            importStmt.absoluteTargetFilename)
        #type: Optional[ModelSourceFile]
        """ imported file. The target of the import"""

        self.importedSourceFile= self.doImport(importStmt)

        # bind the issuebox from importing file to imported file
        self.importingSourceFile.issueBox.addParent(
            self.importedSourceFile.issueBox)

    def doImport(self, importStmt):
        """
        actually perform the import ------------
        # Create the sourceFile for the target
        # This actually launch the corresponding parser
        # and create the target model, etc.
        """
        importedFactory=importStmt.metamodel.sourceClass
        importedSourceFile=importedFactory(
            importStmt.absoluteTargetFilename)
        return importedSourceFile

    def __repr__(self):
        return ('%s import %s' % (
                    self.importingSourceFile.basename,
                    self.importedSourceFile.basename))

    def __str__(self):
        return ('import %s model %s' % (
            self.importStmt.metamodel.label,
            self.importStmt.literalTargetFileName
        ))


class ImportBox(object):

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
        #type: Dict[Text, List[ModelSourceFile]]
        # Store the imports.
        # This attribute is private
        # Use source(s) and model(s) instead.

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
        because the model may exist
        independently from the source.
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
        return [
            i for ilist in self._importsByMetamodelId.values()
                for i in ilist ]

    def addImport(self, sourceImport_):
        #type: (SourceImport) -> None
        """ Add a source import to this box """
        id=sourceImport_.importStmt.metamodel.id
        if id not in self._importsByMetamodelId:
            self._importsByMetamodelId[id]=[]
        self._importsByMetamodelId[id].append(sourceImport_)
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
        if id not in self._importsByMetamodelId[id]:
            return []
        else:
            return self._importsByMetamodelId[id]

    def sourceImport(self, id, optional=True):
        #type: (Text) -> Optional[SourceImport]
        """
        Return "the one and only" sourceImport for a
        given metamodel id.
        If there is no sourceImport then raise add an issue,
        unless optional is True in which case None is returned.
        If there is more than one sourceImport then an issue
        is added.
        """
        if id not in self._importsByMetamodelId[id]:
            if optional:
                return None
            else:
                # TODO: generate issue instead
                raise ValueError(
                    'Import of a "%s" model is missing.' % id)
        r=self._importsByMetamodelId[id]
        if len(r)==1:
            return r[0]
        else:
            # TODO: generate issue instead
            raise ValueError(
                '%i model imported. One expected.' %
                (len(r)))

    def sources(self, id):
        return [
            s.importedSourceFile for s in self.sourceImports(id)]

    def source(self, id, optional=True):
        si=self.sourceImport(id, optional=optional)
        if si is None:
            return None
        else:
            return si.importedSourceFile

    def models(self, id):
        return [s.importedSourceFile.model for s in self.sourceImports(id)]

    def model(self, id, optional=True):
        si=self.sourceImport(id, optional=optional)
        if si is None:
            return None
        else:
            return si.importedSourceFile.model

