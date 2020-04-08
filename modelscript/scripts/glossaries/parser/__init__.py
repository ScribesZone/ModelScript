# coding=utf-8

from typing import Text, Union, Optional, Dict, List, cast
import os

from modelscript.base.exceptions import (
    UnexpectedCase)
from modelscript.metamodels.glossaries import (
    GlossaryModel,
    Package,
    Entry,
    METAMODEL,)
from modelscript.megamodels.sources import (
    ASTBasedModelSourceFile)
from modelscript.base.grammars import (
    ASTNodeSourceIssue)
from modelscript.base.issues import (
    Levels,)
from modelscript.megamodels.metamodels import Metamodel
from modelscript.scripts.textblocks.parser import (
    astTextBlockToTextBlock)

__all__ = (
    'GlossaryModelSource'
)

DEBUG = 0

ISSUES = {
    'ENTRY_TWICE': 'gl.syn.entry.twice',
    'PACKAGE_DOC_TWICE': 'gl.syn.packageDoc.twice'
}

def icode(ilabel):
    return ISSUES[ilabel]


class GlossaryModelSource(ASTBasedModelSourceFile):

    _currentTopLevelPackage: Optional[Package]
    # Temporary variable to store current package
    # Will be used by fillModel

    def __init__(self, glossaryFileName: str) -> None:
        this_dir = os.path.dirname(os.path.realpath(__file__))
        self._currentTopLevelPackage = None
        super(GlossaryModelSource, self).__init__(
            fileName=glossaryFileName,
            grammarFile=os.path.join(this_dir, 'grammar.tx')
        )
        # Although this is not specified the glossary model
        # depends on itself.
        self.model.glossaryModelUsed = self.model

    @property
    def metamodel(self) -> Metamodel:
        return METAMODEL

    @property
    def glossaryModel(self) -> GlossaryModel:
        return cast(GlossaryModel, self.model)

    def fillModel(self):

        def _ensure_package(name):
            if name in self.glossaryModel.packageNamed:
                return self.glossaryModel.packageNamed[name]
            else:
                p=Package(self.glossaryModel, name)
                return p

        def _process_top_level_package_declaration(ast_package):
            package=_ensure_package(ast_package.name)
            if (package.description is not None
                and ast_package.textBlock is not None):
                ASTNodeSourceIssue(
                    code=icode('PACKAGE_DOC_TWICE'),
                    astNode=ast_package,
                    level=Levels.Error,
                    message=(
                        'Package "%s" already declared with some doc.' % (
                        ast_package.name)))
            package.description=astTextBlockToTextBlock(
                container=package,
                astTextBlock=ast_package.textBlock)
            self._currentTopLevelPackage=package
            return

        def _processEntry(ast_entry):

            # If no inline 'package:' is defined for the current entry
            # then the package is defined at the top level one.
            if ast_entry.inlinePackage is None:
                if self._currentTopLevelPackage is None:
                    package = _ensure_package('')
                else:
                    package = self._currentTopLevelPackage
            else:
                package = _ensure_package(ast_entry.inlinePackage.name)

            if ast_entry.term in package.entryNamed:
                existing_entry = package.entryNamed[ast_entry.term]
                ASTNodeSourceIssue(
                    code=icode('ENTRY_TWICE'),
                    astNode=ast_entry,
                    level=Levels.Error,
                    message=(
                            'Entry "%s" already declared at line %s' % (
                                ast_entry.term,
                                self.ast.line(existing_entry.astNode))))
            else:
                entry = Entry(
                    package=package,
                    term=ast_entry.term,
                    label=(
                        None if ast_entry.label is None
                        else ast_entry.label.text),
                    synonyms=(
                        [] if ast_entry.synonymPart is None
                        else ast_entry.synonymPart.synonyms
                    ),
                    inflections=(
                        [] if ast_entry.inflectionPart is None
                        else ast_entry.inflectionPart.inflections
                    ),
                    translations=(
                        {} if ast_entry.translationPart is None
                        else {
                            t.language: t.label
                            for t in
                        ast_entry.translationPart.translations}
                    ),
                    astNode=ast_entry
                )
                entry.description = astTextBlockToTextBlock(
                    container=entry,
                    astTextBlock=ast_entry.textBlock)

        for ast_declaration in self.ast.model.declarations:
            type_ = ast_declaration.__class__.__name__
            if type_ == 'TopLevelPackageDeclaration':
                _process_top_level_package_declaration(ast_declaration)
            elif type_ == 'Entry':
                _processEntry(ast_declaration)
            else:
                raise UnexpectedCase(  # raise:OK
                    'Unexpected type %s' % type_)


METAMODEL.registerSource(GlossaryModelSource)
