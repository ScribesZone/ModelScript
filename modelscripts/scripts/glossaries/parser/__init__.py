# coding=utf-8
from __future__ import unicode_literals, print_function, absolute_import, division
from typing import Text, Union, Optional, Dict, List
import re
import os
# from modelscripts.scripts.megamodels.parser import (
#     isMegamodelStatement
# )
from modelscripts.metamodels.glossaries import (
    GlossaryModel,
    Package,
    Entry,
    METAMODEL,
)
from modelscripts.megamodels.sources import (
    ASTBasedModelSourceFile
)
from modelscripts.base.grammars import (
    ASTNodeSourceIssue
)
from modelscripts.base.issues import (
    Levels,
)
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
        # although this is not specified the glossary model
        # depends on itelf
        self.model.glossaryModelUsed=self.model
        if self.isValid and self.model is not None and self.model.glossaryModelUsed:
            self.resolve()


    @property
    def metamodel(self):
        #type: () -> Metamodel
        return METAMODEL

    @property
    def glossaryModel(self):
        #type: () -> GlossaryModel
        m=self.model #type: GlossaryModel
        return m

    def fillModel(self):

        def _ensurePackage(name):
            if name in self.glossaryModel.packageNamed:
                return self.glossaryModel.packageNamed[name]
            else:
                p=Package(self.glossaryModel, name)
                return p




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
                entry.description=astTextBlockToTextBlock(
                    container=entry,
                    astTextBlock=ast_entry.textBlock)




METAMODEL.registerSource(GlossaryModelSource)
