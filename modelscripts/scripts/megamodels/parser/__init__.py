# coding=utf-8

"""
Megamodel statements are always extracted from
RAW UNPROCESSED ORIGINAL source file.
"""
from __future__ import print_function

import os

from modelscripts.base.issues import (
    Issue,
    Levels,
)
from modelscripts.base.symbols import (
    Symbol
)
from modelscripts.megamodels.dependencies.sources import SourceImport
# from modelscripts.megamodels import (
#     Megamodel
# )
from modelscripts.megamodels.metamodels import (
    Metamodel
)
from modelscripts.scripts.megamodels.parser.statements import \
    ImportStatement, DefinitionStatement
from modelscripts.scripts.textblocks.parser import astTextBlockToTextBlock

__all__=(
    'MegamodelStatement'
    'ImportStatement',
    'fillDependencies',
    'isMegamodelStatement',
)

ModelSourceFile='ModelOldSourceFile'



DEBUG=3

#TODO: find a handy solution/convention for file naming
#      The variable below allow to keep some check
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
              (str(model_kinds), metamodel_label, modelName))

    # get the actual metamodel based on the metamodel label
    try:
        # could raise ValueError
        from modelscripts.megamodels import Megamodel
        metamodel=Megamodel.theMetamodel(
            label=metamodel_label) #type: Metamodel
    except ValueError as e:
        ASTNodeSourceIssue(
            code=icode('DEFINITION_EXCEPTION'),
            astNode=astModelDefinition,
            level=Levels.Fatal, # could be error with some work
            message=str(e))

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
                        str(metamodel.modelKinds))))

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
        # could raise ValueError
        from modelscripts.megamodels import Megamodel
        target_metamodel = Megamodel.theMetamodel(
            label=target_metamodel_label)  # type: Metamodel
    except ValueError as e:
        ASTNodeSourceIssue(
            code=icode('IMPORT_EXCEPTION'),
            astNode=astModelImport,
            level=Levels.Fatal,  # could be error with some work
            message=str(e))

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
    # TODO: make the target path optional
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

    # def _parse():
    #     for line_no in range(1, len(modelSource.sourceLines) + 1):
    #
    #         mi = _matchModelImport(
    #             lineNo=line_no,
    #             modelSourceFile=modelSource,
    #             justMatch=False )
    #
    #         if mi is not None:
    #             if DEBUG>=1 or Config.realtimeImportPrint >=1:
    #                 print('\nimp: >>>>>>>> '+repr(mi))
    #             print('>>'*20, 'import')
    #
    #             modelSource.importBox.addImport(
    #                 SourceImport(importStmt=mi)
    #             )
    #
    #
    #             if DEBUG>=1 or Config.realtimeImportPrint >=1:
    #                 from modelscripts.scripts.megamodels.printer.imports import ImportBoxPrinter
    #                 ImportBoxPrinter(modelSource.importBox).display()
    #                 print('imp: <<<<<<<< '+repr(mi)+'\n')
    #             continue
    #
    #         # --------- any other line is ok -------------------
    #         continue

    def doImport(modelImportStatement):
        if DEBUG >= 1:
            print('\nMEG: >>>>>>>> ' + repr(modelImportStatement))
        modelSource.importBox.addImport(
            SourceImport(importStmt=modelImportStatement)
        )
        if DEBUG >= 1:
            from modelscripts.scripts.megamodels.printer.imports import \
                ImportBoxPrinter
            ImportBoxPrinter(modelSource.importBox).display()
            print('MEG: <<<<<<<< ' + repr(modelImportStatement) + '\n')

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
        # TODO: add here other checks about import cards


    ast_megamodelPart=modelSource.ast.model.megamodelPart

    definition_statement=getModelDefinitionStatement(
        modelSource, ast_megamodelPart.modelDefinition)

    modelSource.importBox.setModelInfo(
        modelName=definition_statement.modelName,
        modelKinds=definition_statement.modelKinds,
        modelDescription=definition_statement.modelDescription
    )




    for ast_modelImport in ast_megamodelPart.modelImports:
        print('MGE: >> "%s" "%s" model from "%s"' % (
              ast_modelImport.modifier,
              ast_modelImport.targetMetamodel,
              ast_modelImport.targetPath))
        import_statement=getModelImportStatement(
            modelSource,
            ast_modelImport
        )
        doImport(import_statement)

        # modelSource.importBox.addImport(
        #     SourceImport(importStmt=mi)
        # )
    _check()


