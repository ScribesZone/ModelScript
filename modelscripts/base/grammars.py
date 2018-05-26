import os
import sys
from typing import Text, Optional
from textx import metamodel_from_str
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

#TODO: remove the kludge below and add some kind of include grammar

INCLUDES= (
    '../scripts/megamodels/parser/grammar.tx',
    '../scripts/textblocks/parser/grammar.tx',
)

def _read_file(filename):
    with open(filename, 'r') as content_file:
        content = content_file.read()
    return content

class Grammar(object):
    def __init__(self, grammarFile):
        self.file=grammarFile
        full_grammar_text=self._get_grammar_str()
        self.metamodel=metamodel_from_str(full_grammar_text)
        self.metamodel.auto_init_attributes=False
        self.parser=self.metamodel.parser

    def _read_file(self, filename):
        with open(filename, 'r') as content_file:
            content = content_file.read()
        return content

    def _get_grammar_str(self):
        grammar_str=self._read_file(self.file)
        this_dir = os.path.dirname(os.path.realpath(__file__))
        for include in INCLUDES:
            included_file=os.path.join(this_dir, include)
            grammar_str += _read_file(included_file)
        return grammar_str

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
        #type: (Grammar, Text) -> None
        print('NN'*30, file)
        self.grammar=grammar
        self.file=file
        self.bracketedFile=\
            modelscripts.base.brackets.BracketedScript(self.file).save()
        print('NN'*30, self.bracketedFile)
        self.model=self.grammar.metamodel.model_from_file(
            self.bracketedFile)
        print('NN'*30, type(self.model), self.model)
        # instrument textx model with a reference back to this object
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
