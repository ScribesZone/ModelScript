# coding=utf-8


import os
import re
from abc import ABCMeta

from typing import Text, Optional, Union

from modelscribes.base.issues import (
    LocalizedIssue,
    Issue,
    Levels,
)
from modelscribes.base.symbols import (
    Symbol
)
from modelscribes.megamodels.dependencies.sources import SourceImport
from modelscribes.megamodels.megamodels import (
    Megamodel
)
from modelscribes.megamodels.metamodels import (
    Metamodel
)

__all__=(
    'MegamodelStatement'
    'ImportStatement',
    'DefinitionStatement',

    'parseToFillImportBox',
    'isMegamodelStatement',
)

ModelSourceFile='ModelSourceFile'

class MegamodelStatement(object):
    __metaclass__ = ABCMeta
    def __init__(self,
                 lineNo,
                 sourceFile,
                 metamodel):
        # type: (int, ModelSourceFile, Metamodel) -> None
        self.lineNo=lineNo
        self.sourceFile=sourceFile
        self.metamodel=metamodel

class ImportStatement(MegamodelStatement):
    def __init__(self,
                 lineNo,
                 sourceFile,
                 metamodel,
                 absoluteTargetFilename,
                 literalTargetFileName):
        # type: (int, ModelSourceFile, Metamodel, Text) -> None
        super(ImportStatement, self).__init__(
            lineNo, sourceFile, metamodel)
        self.literalTargetFileName=literalTargetFileName
        self.absoluteTargetFilename=absoluteTargetFilename


class DefinitionStatement(MegamodelStatement):
    def __init__(self,
                 lineNo,
                 sourceFile,
                 modelKind,
                 metamodel,
                 name):
        #type: (int, ModelSourceFile, Text, Metamodel, Text) -> None
        super(DefinitionStatement, self).__init__(
            lineNo, sourceFile, metamodel)
        self.modelKind=modelKind
        self.name=name

def isMegamodelStatement(
        lineNo,
        modelSourceFile,
        prefixRegexp=r' *(--)? *@',
        noSymbolChecking=False,
        recognizeUSEOCLNativeModelDefinition=False):

    r1=_matchModelDefinition(
        lineNo,
        modelSourceFile=modelSourceFile,
        justMatch=True,
        prefixRegexp=prefixRegexp,
        noSymbolChecking=noSymbolChecking,
        recognizeUSEOCLNativeModelDefinition=
            recognizeUSEOCLNativeModelDefinition)
    if r1 is None:
        return False
    r2=_matchModelImport(
        lineNo,
        modelSourceFile=modelSourceFile,
        justMatch=True,
        prefixRegexp=prefixRegexp)
    return r2 is not None

def _matchModelImport(
        lineNo,
        modelSourceFile,
        justMatch=False,
        prefixRegexp=r' *(--)? *@'):
    #type: (int, ModelSourceFile, bool, Text) -> Optional[Union[bool,ImportStatement]]
    """
        Check if the line is an import statement.

        If justMatch just indicates if the line is recognized.
        In that case it returns True otherwise None.

        If not justMatch build an ImportStatement (if possible)
        Return None if this is not the case.
        Otherwise return a ModelImportStatement if the import is valid.
        Otherwise raise a fatal error that go in the issue box.
        Import statements looks like this
            import usecase model x.cs
            import glossary model a/b/../c.glm
    """
    re_stmt=(
        prefixRegexp
        +r' *(?P<import>import)'
        +r' +(?P<metamodelLabel>\w+)'
        +r' +model'
        +r' +(?P<target>[\w\./\-]+) *$')
    line=modelSourceFile.realSourceLines[lineNo - 1]
    m = re.match(re_stmt, line, re.MULTILINE)
    if m is None:
        return None
    else:
        if justMatch:
            return True
        else:
            source_metamodel=modelSourceFile.metamodel

            # get actual metamodel
            metamodel_label=m.group('metamodelLabel')
            try:
                # could raise ValueError
                metamodel=Megamodel.metamodel(
                    label=metamodel_label) #type: Metamodel
            except ValueError as e:
                LocalizedIssue(
                    sourceFile=modelSourceFile,
                    line=lineNo,
                    level=Levels.Fatal, # could be error with some work
                    message=str(e))

            # Check that metamodel dependency is allowed
            target_mms=source_metamodel.outMetamodels
            # noinspection PyUnboundLocalVariable
            if metamodel not in target_mms:
                LocalizedIssue(
                    sourceFile=modelSourceFile,
                    line=lineNo,
                    level=Levels.Fatal, # could be error with some work
                    message=(
                        'A %s model cannot reference a %s model.' % (
                            source_metamodel.label,
                            metamodel.label  )))

            # Check path
            literal_target_filename=m.group('target')
            abs_target_filename=os.path.abspath(
                os.path.join(modelSourceFile.directory,
                             literal_target_filename))
            file_extension=os.path.splitext(abs_target_filename)[1]
            if file_extension != metamodel.extension:
                LocalizedIssue(
                    sourceFile=modelSourceFile,
                    line=lineNo,
                    level=Levels.Fatal, # could be error with some work
                    message=(
                        'The extension of the file must be "%s".' % (
                            metamodel.extension )))
            if not os.path.isfile(abs_target_filename):
                LocalizedIssue(
                    sourceFile=modelSourceFile,
                    line=lineNo,
                    level=Levels.Fatal, # could be error with some work
                    message=(
                        'File not found: %s' % literal_target_filename))

            return ImportStatement(
                lineNo=lineNo,
                sourceFile=modelSourceFile,
                metamodel=metamodel,
                absoluteTargetFilename=abs_target_filename,
                literalTargetFileName=literal_target_filename
            )




def _matchModelDefinition(
        lineNo,
        modelSourceFile,
        justMatch=False,
        prefixRegexp=r' *(--)? *@',
        noSymbolChecking=False,
        recognizeUSEOCLNativeModelDefinition=False):
    # type: (int, ModelSourceFile, bool, Text) -> Optional[Union[bool,DefinitionStatement]]
    """
        Check if the line is a model definition statement.

        If justMatch just indicates if the line is recognized.
        In that case it returns True otherwise None.

        If not justMatch build an ImportStatement (if possible)
        Return None if this is not the case.
        Return a ModelDefinitionStatement if the stmt is valid.
        Otherwise raise a value error.
        Definition statements looks like this
            preliminary usecase model MyModel
            class model MyModel

        If 'recognizeUSEOCLNativeModelDefinition' then the line
        "model <NAME>" is accepted as the model definition in USE OCL
        files. This is a patch good enough for now for .use file.
        Later the .use file could be generated and the syntax improved.
    """
    def _parseStandardSyntax():
        re_stmt = (
            prefixRegexp
            + r' *((?P<modelKind>\w+) +)?'
            + r'(?P<metamodelLabel>\w+)'
            + r' +model'
            + r' +(?P<name>\w+) *$')
        line = modelSourceFile.realSourceLines[lineNo - 1]
        m = re.match(re_stmt, line, re.MULTILINE)
        if m is None:
            return None
        else:
            if m.group('modelKind')=='import':  # because overlapping regexp
                return None
            if justMatch:
                return True
            else:
                return {
                    'modelKind': m.group('modelKind'),
                    'metamodelLabel': m.group('metamodelLabel'),
                    'name': m.group('name')
                }
    def _parseUSEOCLSyntax():
        re_stmt = (
            '^'
            + r' *model'
            + r' +(?P<name>\w+) *$')
        line = modelSourceFile.realSourceLines[lineNo - 1]
        m = re.match(re_stmt, line, re.MULTILINE)
        if m is None:
            return None
        if justMatch:
            return True
        else:
            return {
                'modelKind': '',
                'metamodelLabel': 'class',
                'name': m.group('name')
            }

    def _parse():
        r1=_parseStandardSyntax()
        if r1 is not None or not recognizeUSEOCLNativeModelDefinition:
            return r1
        else:
            # No match so search USEOCL
            return _parseUSEOCLSyntax()

    m=_parse()
    if m in [True, None]:
        return m
    else:
        source_metamodel=modelSourceFile.metamodel

        # get actual metamodel
        metamodel_label=m['metamodelLabel']
        try:
            # could raise ValueError
            metamodel=Megamodel.metamodel(
                label=metamodel_label) #type: Metamodel
        except ValueError as e:
            LocalizedIssue(
                sourceFile=modelSourceFile,
                line=lineNo,
                level=Levels.Fatal, # could be error with some work
                message=str(e))

        # check model_kind
        model_kind=(
            '' if m['modelKind'] is None
            else m['modelKind'])
        # noinspection PyUnboundLocalVariable
        if model_kind not in metamodel.modelKinds:
            LocalizedIssue(
                sourceFile=modelSourceFile,
                line=lineNo,
                level=Levels.Fatal, # could be error with some work
                message=(
                    '%s models can\'t be "%s".'
                    ' Choose one of %s.' % (
                        metamodel_label,
                        model_kind,
                        str(metamodel.modelKinds))))

        # Check that the metamodel is the expected one
        if metamodel != source_metamodel:
            LocalizedIssue(
                sourceFile=modelSourceFile,
                line=lineNo,
                level=Levels.Fatal,  # could be error with some work
                message=(
                    'A %s model cannot be defined in a "%s" file.' % (
                        metamodel.label,
                        source_metamodel.extension,
                    )))

        # Check name
        name=m['name']
        if not noSymbolChecking and not(Symbol.is_CamlCase(name)):
            LocalizedIssue(
                sourceFile=modelSourceFile,
                line=lineNo,
                level=Levels.Error,
                message=(
                    'Invalid model name "%s". It must be in CamlCases.' % (
                        name
                    )))
        if name.lower() != modelSourceFile.name.lower():
            if not recognizeUSEOCLNativeModelDefinition:
                LocalizedIssue(
                    sourceFile=modelSourceFile,
                    line=lineNo,
                    level=Levels.Error,
                    message=(
                        'Model must be named %s according to the name of the file' % (
                            # modelSourceFile.fileName,
                            modelSourceFile.name
                        )))
        return DefinitionStatement(
            lineNo=lineNo,
            sourceFile=modelSourceFile,
            modelKind=model_kind,
            metamodel=metamodel,
            name=name
        )


def parseToFillImportBox(modelSource,
                         noSymbolChecking=False,
                         recognizeUSEOCLNativeModelDefinition=False):
    """
    Parse all the lines from the model source and fill
    modelsource.importBox with the information found.

    When a model definition is found call
        importBox.setModelInfo

    When a import is found then add a SourceImport

    Generate an issue
    - when there is more than one model definition

    recognizeUSEOCLNativeModelDefinition is a patch to
    parse line like "model <name>" in use file. This patch
    could be remove when a generator will be provided.



    This method can raise an exception FatalError


    """
    assert modelSource.sourceLines is not None
    assert modelSource.model is not None
    assert modelSource.importBox is not None

    def _parse():
        for line_no in range(1, len(modelSource.sourceLines) + 1):

            # --------- model definition ----------------------
            md = _matchModelDefinition(
                lineNo=line_no,
                modelSourceFile=modelSource,
                justMatch=False,
                prefixRegexp=modelSource.megamodelStatementPrefix,
                noSymbolChecking=noSymbolChecking,
                recognizeUSEOCLNativeModelDefinition=
                    recognizeUSEOCLNativeModelDefinition
            )
            if md is not None:
                if modelSource.importBox.modelName is not None:
                    LocalizedIssue(
                        sourceFile=modelSource,
                        line=line_no,
                        level=Levels.Warning,
                        message=('The model is already named : "%s"'
                                 % modelSource.model.modelName))

                modelSource.importBox.setModelInfo(
                    modelName=md.name,
                    modelKind=md.modelKind
                )
                continue

            # --------- model import ----------------------

            mi = _matchModelImport(
                lineNo=line_no,
                modelSourceFile=modelSource,
                justMatch=False,
                prefixRegexp=modelSource.megamodelStatementPrefix
            )
            if mi is not None:
                modelSource.importBox.addImport(
                    SourceImport(importStmt=mi)
                )
                continue

            # --------- whatever line is ok -------------------
            continue

    def _check():
        if modelSource.importBox.modelName is None:
            Issue(
                origin = modelSource,
                level = Levels.Warning,
                message = (
                    'Unamed model.'
                    ' A statement like'
                    ' "class model <name>" must be added.'))
        # TODO: add here other checks about import cards

    model_definition_found = True
    _parse()
    _check()


    #
# def extractMegaModelFromText(sourceFile):
#
#
#
#
# def extractModelStatements(
#         sourceFile,
#         prefixRegexp=r' *(--)? *@'):
#     #type: (SourceFile, Text) -> List[MegamodelStatement]
#     def read_file():
#         with io.open(sourceFile.fileName,
#                      'rU',
#                      encoding='utf8') as f:
#             lines = list(
#                 line.rstrip() for line in f.readlines())
#         return lines
#
#     _=[]
#     for line in read_file():
#         stmt=matchModelStatement(
#             line,
#             sourceFile,
#             prefixRegexp)
#         if stmt is not None:
#             _.append(stmt)
#     return _
