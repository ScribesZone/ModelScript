import os
import sys
from typing import Text, Optional
from textx import metamodel_from_file
from textx.export import (
    metamodel_export,
    model_export
)
# future versions of textx use get_model
# instead of model_root
from textx.model import model_root as get_model

import modelscripts.base.brackets
from modelscripts.base.issues import LocalizedSourceIssue
from modelscripts.megamodels.sources import ModelSourceFile

__all__= (
    'Grammar',
    'AST',
    'ModelSourceAST',
    'ASTBasedModelSourceFile',
    'ASTNodeSourceIssue'
)

class Grammar(object):
    def __init__(self, grammarFile):
                 # useLanguageCode=False):
        # self.languageCode=language[0:2]
        # if useLanguageCode:
        #     self.directory=os.path.join(
        #         grammarDirectory, self.languageCode)
        # else:
        #     self.directory=grammarDirectory
        self.file=grammarFile
        self.metamodel=metamodel_from_file(self.file)
        self.metamodel.auto_init_attributes=False
        self.parser=self.metamodel.parser

    def visualize(self):
        dot_file=self.file+'.dot'
        metamodel_export(self.metamodel, dot_file)
        os.system('dot -Tpng -O %s' % dot_file)


class AST(object):

    @classmethod
    def ast(cls, astNode):
        """ Return the AST from a given ast node """
        # this implemenation is based both on a method from textX
        # and the fact that the textX model has been instrumented
        # with an ast attribute
        return get_model(astNode).ast

    def __init__(self, grammar, file):
        self.grammar=grammar
        self.file=file
        self.bracketedFile= modelscripts.base.brackets.BracketedScript(self.file).save()
        self.model=self.grammar.metamodel.model_from_file(
            self.bracketedFile)
        # instrument textx model with a reference back to this object
        # this allo
        self.model.ast=self
        # self.bracketedtext=brackets.BracketedScript(self.file).text
        # self.model=self.grammar.metamodel.model_from_str(
        #     self.bracketedtext)

    def pos(self, element):
        return self.grammar.parser.pos_to_linecol(
            element._tx_position)

    def posEnd(self, element):
        return self.grammar.parser.pos_to_linecol(
            element._tx_position_end)

    def line(self, element):
        (l,c)=self.pos(element)
        return l

    def column(self, element):
        (l,c)=self.pos(element)
        return c

    def visualize(self):
        dot_file=self.file+'.dot'
        model_export(self.model, dot_file)
        os.system('dot -Tpng -O %s' % dot_file)




class ModelSourceAST(AST):
    """
    An AST but with "modelSourceFile" as an extra attribute.
    This attribute contains a model source file instead of
    a plain filename.
    """
    def __init__(self, grammar, modelSourceFile):
        self.sourceFile=modelSourceFile
        super(ModelSourceAST, self).__init__(
            grammar=grammar,
            file=modelSourceFile.fileName
        )


class ASTBasedModelSourceFile(ModelSourceFile):
    """
    Source file with a model produced via an AST.
    """
    def __init__(self, fileName, grammarFile):
        #type: (Text, Text) -> None

        self.grammar=Grammar(grammarFile)
        #type:

        self.ast=None  #type: Optional[ModelSourceAST]
        # must be filled by subclasses

        super(ASTBasedModelSourceFile, self).__init__(fileName)


class ASTNodeSourceIssue(LocalizedSourceIssue):
    def __init__(self, astNode, level, message, code=None):
        ast=AST.ast(astNode)
        super(ASTNodeSourceIssue, self).__init__(
            code=code,
            sourceFile=ast.sourceFile,
            level=level,
            message=message,
            line=ast.line(astNode),
            column=ast.column(astNode)
        )

if __name__ == "__main__":

    grammar_file = sys.argv[1]
    print('Loading %s grammar ... ' % grammar_file)
    grammar = Grammar(grammar_file)
    grammar.visualize()
    print('OK')

    if len(sys.argv)>=3:
        script_file = sys.argv[2]
        print('Loading script %s ...' % script_file)
        ast=AST(grammar, script_file)
        ast.visualize()
        print('OK')
