# coding=utf-8
from __future__ import unicode_literals, print_function, absolute_import, division
from typing import Text, Union, Optional, Dict, List
import re
import os
from modelscripts.scripts.megamodels.parser import (
    isMegamodelStatement
)
from modelscripts.metamodels.glossaries import (
    GlossaryModel,
    Package,
    Entry,
    METAMODEL,
)
from modelscripts.base.grammars import (
    ModelSourceAST,
    ASTBasedModelSourceFile,
    ASTNodeSourceIssue
)
from modelscripts.base.issues import (
    Levels,
)
from modelscripts.metamodels.textblocks import (
    TextBlock,
)
# from modelscripts.scripts.textblocks.parser import TextBlockSource
from modelscripts.megamodels.metamodels import Metamodel
from modelscripts.scripts.textblocks.parser import (
    astTextBlockToTextBlock
)


DEBUG=0

ISSUES={
    'ENTRY_TWICE':'gl.syn.entry.twice'
}

def icode(ilabel):
    return ISSUES[ilabel]

class GlossaryModelSource(ASTBasedModelSourceFile):
    def __init__(self, glossaryFileName):
        #type: (Text) -> None
        this_dir=os.path.dirname(os.path.realpath(__file__))
        super(GlossaryModelSource, self).__init__(
            fileName=glossaryFileName,
            grammarFile=os.path.join(this_dir, 'grammar.tx')
        )

    @property
    def metamodel(self):
        #type: () -> Metamodel
        return METAMODEL

    @property
    def glossaryModel(self):
        #type: () -> GlossaryModel
        m=self.model #type: GlossaryModel
        return m


    def parseToFillModel(self):
        self._parse_main_body()
        if self.glossaryModel and self.isValid:
            self._resolve()

    def _parse_main_body(self):

        def _ensurePackage(name):
            if name in self.glossaryModel.packageNamed:
                return self.glossaryModel.packageNamed[name]
            else:
                p=Package(self.glossaryModel, name)
                return p

        self.ast = ModelSourceAST(self.grammar, self)

        self.glossaryModel.docComment = astTextBlockToTextBlock(
            container=self.glossaryModel,
            astTextBlock=self.ast.model.textBlock)

        for ast_entry in self.ast.model.entries:
            if ast_entry.package is None:
                package=_ensurePackage('')
            else:
                package=_ensurePackage(ast_entry.package.name)
            if ast_entry.term in package.entryNamed:
                existing_entry=package.entryNamed[ast_entry.term]
                ASTNodeSourceIssue(
                    code=icode('ENTRY_TWICE'),
                    astNode=ast_entry,
                    level=Levels.Error,
                    message=(
                        'Entry "%s" already declared at line %s' % (
                            ast_entry.term,
                            self.ast.line(existing_entry.astnode))))
            else:
                entry=Entry(
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
                            t.language : t.label
                            for t in ast_entry.translationPart.translations }
                    ),
                    astNode=ast_entry
                )
                entry.docComment=astTextBlockToTextBlock(
                    container=entry,
                    astTextBlock=ast_entry.textBlock)



    def _resolve(self):
        """
        For all entry description in the glossary
        resolve the description with this glossary.
        """
        for domain in self.glossaryModel.packageNamed.values():
            for entry in domain.entryNamed.values():
                entry.description.resolve()
                # description_parser= (
                #     self.descriptionBlockSourcePerEntry[entry])
                # # lno=self.__descriptionFirstLineNoPerEntry[entry]
                # description_parser.parseToFillModel(
                #     container=entry,
                #     glossary=self.model
                # )
                # if not description_parser.isValid:
                #     # TODO: check what should be done
                #     raise ValueError('Error in parsing Text source')
                # else:
                #     entry.description=description_parser.model



METAMODEL.registerSource(GlossaryModelSource)
