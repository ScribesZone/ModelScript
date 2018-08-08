# coding=utf-8
"""
Manage "SourceImports" and "ImportBoxes".

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
from modelscripts.megamodels.dependencies import Dependency
from modelscripts.megamodels.dependencies.models import ModelDependency
#from modelscripts.megamodels.sources import ModelOldSourceFile
ModelSourceFile='ModelOldSourceFile'

#from modelscripts.scripts.megamodels.parser import ImportStatement
ImportStatement='ImportStatement'

from collections import OrderedDict

# FIXME:1 test_ucm_parser should raise an issue for importing a uc

from modelscripts.base.issues import (
    Levels,
    Issue
)
# from modelscripts.megamodels import Megamodel

DEBUG=1

__all__ = (
    'SourceFileDependency',
    'SourceImport',
    'ImportBox'
)


class SourceFileDependency(Dependency):
    """
    A pair of source files representing a dependency between
    these two files.
    """
    __metaclass__ = ABCMeta

    def __init__(self, importingSourceFile, importedSourceFile):
        #type: (ModelSourceFile, ModelSourceFile) -> None
        """
        Create the dependency and register it in the metamodel.
        """

        self.importingSourceFile=importingSourceFile
        #type: ModelSourceFile
        """ Source file that contains the import """

        self.importedSourceFile= importedSourceFile
        #type: ModelSourceFile
        """ Imported source file. The target of the import"""

        from modelscripts.megamodels import Megamodel
        Megamodel.registerSourceDependency(self)

        # register model dependency if not already there
        # (it should not be there)
        sm=self.importingSourceFile.model
        tm=self.importedSourceFile.model
        if Megamodel.modelDependency(sm, tm) is None:
            d=ModelDependency(sm, tm)
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
    """
    A SourceFileDependency with its concrete representation
    in the term of the source import statement
    located the source in the form
    of a ImportStatement created by the megamodel parser.
    """
    def __init__(self, importStmt):
        #type: (ImportStatement) -> None
        """
        Create an SourceImport and actually perform the
        actuel import of target source file. If the target
        source file is not already registered in the megamodel
        then the target is
        read and a ModelOldSourceFile is therefore created.
        This possibly could generate some issues but these
        are stored in the target ModelOldSourceFile.
        The _issueBox of the importing ModelOldSourceFile is
        linked to the one of the target. This allows to
        source to "see" issues produced in the target.
        """

        self.importStmt=importStmt #type: ImportStatement
        """ Link to the syntactic import statement """

        self.importBox=None #type: Optional[ImportBox]
        """ Back reference to the containing import box """
        # filled in ImportBox.addImport

        try:
            # already registered
            from modelscripts.megamodels import Megamodel
            importedSourceFile=Megamodel.source(
                importStmt.absoluteTargetFilename)
        except ValueError :
            # Not registered yet:
            # actually perform the import
            importedSourceFile=self._doImport(importStmt)
            # XXXXXXZZZZZZZ
        except:
            import traceback
            for i in range(0, 10):
                print('ZZ'*80)
            print(traceback.format_exc())
            for i in range(0, 10):
                print('ZZ'*80)
            raise

        super(SourceImport, self).__init__(
            self.importStmt.modelSourceFile,
            importedSourceFile
        )

        self._doBindIssueBoxes()

        if self.importedSourceFile.issues.bigIssues:
            Issue(
                code='iss.source.import.fatal',
                origin=self.importingSourceFile,
                level=Levels.Fatal,
                message=
                    'Serious issue(s) found when importing "%s"' %
                    self.importedSourceFile.basename
            )

    def _doImport(self, importStmt):
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

    def _doBindIssueBoxes(self):
        """
        Bind the issuebox from importing file to imported file
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



class ModelDescriptor(object):
    __metaclass__ = ABCMeta

    def __init__(self):

        self._modelName=None #type: Optional[Text]
        """ 
        Name of the importing model.
        This name is found in the model declaration statement.
        It is set by the method setModelInfo().
        """
        # will be set by parseToFillImportBox

        self._modelKinds=[] #type: List[Text]
        """ 
        Model kinds of the importing model. A list of label like
        instance "draft", "conceptual" or "preliminary".
        This information is found in the model 
        definition statement. It will be set by
        the method parseToFillImportBox() in the model source
        which call setModelInfo().
        """

        self._modelDescription=None  #type: Optional[Text]

    @property
    def modelName(self):
        # type: () -> Text
        return self._modelName

    @property
    def modelKinds(self):
        # type: () -> List[Text]
        return self._modelKinds

    def setModelInfo(self, modelName, modelKinds, modelDescription):
        """
        Set description.
        """
        self._modelName = modelName
        self._modelKinds = modelKinds
        self._modelDescription = modelDescription



class ImportBox(ModelDescriptor):
    """
    An import box is like a collection of SourceImports
    but for a given model source, the one containing the
    ImportBox.
    A convinient way to access to imported sources and models.

    The ImportBox contains as well the name of the model, and
    the kind of the model (even though strictly speaking this
    information is not linked to 'Imports'. (Not found a
    better place to put these attributes and a better name
    for ImportBox)
    """

    def __init__(self, modelSource):
        #type: (ModelSourceFile) -> None
        """
        Creates an empty ImportBox for the given
        ModelOldSourceFile.
        """

        super(ImportBox, self).__init__()

        self.modelSource=modelSource #type: ModelSourceFile
        """ 
        Source file containing the import box.
        """



        self._importsByMetamodelId=OrderedDict()
        #type: Dict[Text, List[SourceImport]]
        """
        Store the imports indexed by metamodel id.
        This attribute is private. Use instead
        addImport, imports, models, etc.
        """
        # ??? type: Dict[Text, List[ModelOldSourceFile]] <-- probably an error




    @property
    def imports(self):
        #type: () -> List[SourceImport]
        """
        List of all SourceImports starting from this
        ImportBox, that is, from the corresponding.
        ModelOldSourceFile.
        """
        return [
            i for ilist in self._importsByMetamodelId.values()
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
        # TODO:4 update megamodel/model dependencies


    # TODO:4 improve the methods based on metamodel dependencies
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
        from modelscripts.megamodels import Megamodel
        metamodel_label = Megamodel.theMetamodel(id=id).label
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

    def sourceFiles(self, id):
        #type: () -> List[ModelSourceFile]
        """
        Returns the list of all source files imported for
        a given metamodel id.
        """
        return [
            s.importedSourceFile for s in self.sourceImports(id)]

    def sourceFile(self, id, optional=False):
        #type: (Text, bool) -> Optional[ModelSourceFile]
        """
        Return "the one and only one" source file for a
        given metamodel id. If there is no such source file
        then return None. If there are more than one source
        file then produce a fatal issue.
        """
        si=self.sourceImport(id, optional=optional)
        if si is None:
            return None
        else:
            return si.importedSourceFile

    def models(self, id):
        """
        Returns the list of all models imported for
        a given metamodel id.
        """
        return [s.importedSourceFile.model
                for s in self.sourceImports(id)]

    def model(self, id, optional=False):
        """
        Returns "the one and only one" model imported for
        a given metamodel id.  If there is no such model
        then return None. If there are more than one
        then produce a fatal issue.
        """
        si=self.sourceImport(id, optional=optional)
        if si is None:
            return None
        else:
            return si.importedSourceFile.model

