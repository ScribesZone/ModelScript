# coding=utf-8

"""
Megamodel statements are always extracted from
RAW UNPROCESSED ORIGINAL source file.
"""
from __future__ import print_function

import os

from modelscripts.base.issues import (
    Issue,
    Levels)
from modelscripts.base.symbols import (
    Symbol)
from modelscripts.megamodels.dependencies.sources import SourceImport
from modelscripts.megamodels.metamodels import (
    Metamodel)
from modelscripts.scripts.megamodels.parser.statements import (
    ImportStatement,
    DefinitionStatement)
from modelscripts.scripts.textblocks.parser import (
    astTextBlockToTextBlock)
from modelscripts.base.exceptions import (
    UnexpectedValue)


# ModelSourceFile='ModelOldSourceFile'



DEBUG=0

#TODO:2 find a handy solution/convention for file naming
#      Currently the variable below allow to keep
#      a sync between filenames and models but this
#      could be changed/relaxed.
CHECK_FILENAMES_AND_MODELS=False

ISSUES={
    'IMPORT_EXCEPTION':'mgm.env.Import.Exception',
    'IMPORT_ALLOWED':'mgm.sem.Import.Allowed',
    'IMPORT_EXTENSION':'mgm.sem.Import.Extension',
    'IMPORT_NO_FILE':'mgm.sem.Import.NotFound',
    'DEFINITION_EXCEPTION':'mgm.sem.Definition.Exception',
    'DEFINITION_KIND':'mgm.sem.Definition.Kind',
    'DEFINITION_CASE':'mgm.sem.Definition.Case',
    'DEFINITION_NAMING':'mgm.sem.Definition.Naming',
    'BOX_TWICE':'mgm.sem.Box.Twice',
    'DEFINITION_UNAMED':'mgm.sem.Definition.Unamed',
}

def icode(ilabel):
    return ISSUES[ilabel]


def getModelDefinitionStatement(modelSourceFile, astModelDefinition):
    """
    Extract from the AST the model definition and build a
    Model definition statements.
    This method can raise Levels.fatal errors or Levels.error.

    Model definition looks like this
        preliminary usecase model MyModel
        class model MyModel
    """
    from modelscripts.base.grammars import ASTNodeSourceIssue

    metamodel_label=astModelDefinition.labels[-1]
    model_kinds=astModelDefinition.labels[:-1]
    modelName=astModelDefinition.name
    modelDescription=astTextBlockToTextBlock(
        container=modelSourceFile.model,
        astTextBlock=astModelDefinition.textBlock)
    if DEBUG>=3:
        print('MEG: Defining %s %s model %s' %
              (unicode(model_kinds), metamodel_label, modelName))

    # get the actual metamodel based on the metamodel label
    try:
        # could raise UnexpectedValue
        from modelscripts.megamodels import Megamodel
        metamodel=Megamodel.theMetamodel(
            label=metamodel_label) #type: Metamodel
    except UnexpectedValue as e: #except:OK
        ASTNodeSourceIssue(
            code=icode('DEFINITION_EXCEPTION'),
            astNode=astModelDefinition,
            level=Levels.Fatal, # could be error with some work
            message=unicode(e))

    # check that model_kinds are all available with the metamodel
    # noinspection PyUnboundLocalVariable
    for model_kind in model_kinds:
        if model_kind not in metamodel.modelKinds:
            ASTNodeSourceIssue(
                code=icode('DEFINITION_EXCEPTION'),
                astNode=astModelDefinition,
                level=Levels.Fatal, # could be error with some work
                message=(
                    '%s models can\'t be "%s".'
                    ' Choose one of %s.' % (
                        metamodel_label,
                        model_kind,
                        unicode(metamodel.modelKinds))))

    if CHECK_FILENAMES_AND_MODELS:

        # Check name
        if modelName is not None:
            if not (Symbol.is_CamlCase(modelName)):
                ASTNodeSourceIssue(
                    code=icode('DEFINITION_CASE'),
                    astNode=astModelDefinition,
                    level=Levels.Error,
                    message=(
                        'Invalid model name "%s". It must be in CamlCases.'
                        % (modelName)))
            if modelName.lower() != modelSourceFile.name.lower():
                ASTNodeSourceIssue(
                    code=icode('DEFINITION_NAMING'),
                    astNode=astModelDefinition,
                    level=Levels.Error,
                    message=(
                        'Model must be named %s according to the'
                        'name of the file' % (
                        # modelSourceFile.fileName,
                        modelSourceFile.name
                    )))

    ds=DefinitionStatement(
        astNode=astModelDefinition,
        metamodel=metamodel,
        modelSourceFile=modelSourceFile,
        modelName=modelName,
        modelKinds=model_kinds,
        modelDescription=modelDescription
    )
    return ds

def getModelImportStatement(modelSourceFile, astModelImport):
    from modelscripts.base.grammars import ASTNodeSourceIssue

    source_metamodel = modelSourceFile.metamodel

    # get metamodel imported
    target_metamodel_label = astModelImport.targetMetamodel
    try:
        # could raise UnexpectedValue
        from modelscripts.megamodels import Megamodel
        target_metamodel = Megamodel.theMetamodel(
            label=target_metamodel_label)  # type: Metamodel
    except UnexpectedValue as e:  #except:OK
        ASTNodeSourceIssue(
            code=icode('IMPORT_EXCEPTION'),
            astNode=astModelImport,
            level=Levels.Fatal,  # could be error with some work
            message=unicode(e))

    # Check that metamodel dependency is allowed
    target_mms = source_metamodel.outMetamodels
    # noinspection PyUnboundLocalVariable
    if target_metamodel not in target_mms:
        ASTNodeSourceIssue(
            code=icode('IMPORT_ALLOWED'),
            astNode=astModelImport,
            level=Levels.Fatal,  # could be error with some work
            message=(
                'A %s model cannot reference a %s model.' % (
                    source_metamodel.label,
                    target_metamodel.label)))

    # Check imported file path and extension
    # TODO:2 make the target path optional
    literal_target_filename=astModelImport.targetPath
    abs_target_filename = os.path.abspath(
        os.path.join(modelSourceFile.directory,
                     literal_target_filename))
    file_extension = os.path.splitext(abs_target_filename)[1]
    if file_extension != target_metamodel.extension:
        ASTNodeSourceIssue(
            code=icode('IMPORT_EXTENSION'),
            astNode=astModelImport,
            level=Levels.Fatal,  # could be error with some work
            message=(
                'The extension of the file must be "%s".' % (
                    target_metamodel.extension)))

    # check that the target file exists
    if not os.path.isfile(abs_target_filename):
        ASTNodeSourceIssue(
            code=icode('IMPORT_NO_FILE'),
            astNode=astModelImport,
            level=Levels.Fatal,  # could be error with some work
            message=(
                'File not found: %s' % literal_target_filename))

    modifier=astModelImport.modifier

    return ImportStatement(
        astNode=astModelImport,
        modelSourceFile=modelSourceFile,
        metamodel=target_metamodel,
        modifier=modifier,
        absoluteTargetFilename=abs_target_filename,
        literalTargetFileName=literal_target_filename
    )


def fillDependencies(modelSource):
    """
    Parse all the lines from the model source and fill
    modelsource.importBox with the information found.

    When a model definition is found call
        importBox.setModelInfo

    When a import is found then add a SourceImport

    Generate an issue
    - when there is more than one model definition

    This method can raise an exception FatalError
    """
    assert modelSource.sourceLines is not None
    assert modelSource.model is not None
    assert modelSource.importBox is not None

    def doImport(modelImportStatement):
        if DEBUG >= 1:
            print('\nMEG: >>>>>>>> ' + repr(modelImportStatement))
        source_import=SourceImport(importStmt=modelImportStatement)
        modelSource.importBox.addImport(source_import)
        if DEBUG >= 1:
            from modelscripts.scripts.megamodels.printer.imports import \
                ImportBoxPrinter
            ImportBoxPrinter(modelSource.importBox).display()
            print('MEG: <<<<<<<< ' + repr(modelImportStatement) + '\n')
        return source_import

    def _check():
        if modelSource.importBox.modelName is None:
            m2_label=modelSource.model.metamodel.label
            Issue(
                code=icode('DEFINITION_UNAMED'),
                origin = modelSource,
                level = Levels.Warning,
                message = (
                    'Unamed model.'
                    ' Add "%s model <name>".'
                    % m2_label))
        #TODO:2 add here other checks about import cards


    ast_megamodelPart=modelSource.ast.model.megamodelPart

    definition_statement=getModelDefinitionStatement(
        modelSource, ast_megamodelPart.modelDefinition)

    modelSource.importBox.setModelInfo(
        modelName=definition_statement.modelName,
        modelKinds=definition_statement.modelKinds,
        modelDescription=definition_statement.modelDescription
    )



    imports_with_big_issues=False
    for ast_modelImport in ast_megamodelPart.modelImports:
        if DEBUG>=2:
            print('MEG: >> "%s" "%s" model from "%s"' % (
                  ast_modelImport.modifier,
                  ast_modelImport.targetMetamodel,
                  ast_modelImport.targetPath))
        import_statement=getModelImportStatement(
            modelSource,
            ast_modelImport
        )
        source_import=doImport(import_statement)
        with_big_issues=\
            source_import.importedSourceFile.issues.bigIssues
        imports_with_big_issues=\
            imports_with_big_issues or with_big_issues

    if imports_with_big_issues:
        Issue(
            code='iss.source.import.fatal',
            origin=modelSource,
            level=Levels.Fatal,
            message=
                'Serious issue(s) found during import. Analysis stopped.')

    _check()

