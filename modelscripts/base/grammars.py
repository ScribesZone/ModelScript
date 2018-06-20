import os
import sys
import re
from typing import Text, Optional
from abc import abstractmethod
from textx import metamodel_from_str
from textx.export import (
    metamodel_export,
    model_export
)
# future versions of textx use get_model
# instead of model_root
from textx.model import model_root as get_model

from modelscripts.base.brackets import (
    BracketedScript,

)
from modelscripts.base.issues import (
    IssueBox,
    FatalError,
    LocalizedSourceIssue,
    Levels
)
from modelscripts.megamodels.sources import ASTBasedModelSourceFile

__all__= (
    'Grammar',
    'AST',
    'ModelSourceAST',
    'ASTBasedModelSourceFile',
    'ASTNodeSourceIssue'
)

from modelscripts.scripts.textblocks.parser import (
    astTextBlockToTextBlock
)

#TODO: remove the kludge below and add some kind of include grammar

INCLUDES= (
    '../scripts/megamodels/parser/grammar.tx',
    '../scripts/textblocks/parser/grammar.tx',
    '../scripts/stories/parser/grammar.tx'
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
            grammar_str += '\n\n'
            grammar_str += _read_file(included_file)
        return grammar_str

    def visualize(self):
        dot_file=self.file+'.dot'
        metamodel_export(self.metamodel, dot_file)
        os.system('dot -Tpng -O %s' % dot_file)

class SyntaxicError(object):
    def __init__(self, message, line, column):
        self.line=line
        self.column=column
        self.message=message

class TokenBasedSyntaxicError(SyntaxicError):

    def __init__(self, message, line, column, tokens, cursor):
        super(TokenBasedSyntaxicError, self).__init__(
            message, line, column
        )
        TOKEN_MAP = {
            'o_': 'OpenBlock',
            '_o': 'CloseBlock',
            'X': 'EndOfLine'
        }
        def cleaned_tokens(tokens):
            # eliminate duplicates
            ts = list(set(tokens))
            # replace key tokens
            for i, t in enumerate(ts):
                if t in TOKEN_MAP:
                    ts[i]=TOKEN_MAP[t]
            # limit to 10
            if len(ts) > 10:
                ts = ts[:10] + ['...']
            return ts

        self.tokens=cleaned_tokens(tokens)
        self.cursor=cursor
        self.message=(
            '(%i:%i): expecting %s' % (
                self.line,
                self.column,
                ', '.join(self.tokens)))

class AST(object):

    @classmethod
    def ast(cls, astNode):
        """ Return the AST from a given ast node """
        # this implemenation is based both on the get_model method from
        # textX and the fact that the textX model has been instrumented
        #  with an ast attribute to go from the textX model to AST.
        return get_model(astNode).ast

    @classmethod
    def nodeLine(cls, astNode):
        return AST.ast(astNode).line(astNode)

    @classmethod
    def extractErrorFields(cls, e):

        # TEXTX CODE PRODUCING THE ERROR MESSAGE:
        #      what_is_expected = ["{}".format(rule_to_exp_str(r))
        #                         for r in self.rules]
        #     what_str = " or ".join(what_is_expected)
        #     err_message = "Expected {}".format(what_str)
        #
        # return "{} at position {}{} => '{}'."\
        #     .format(err_message,
        #             "{}:".format(self.parser.file_name)
        #             if self.parser.file_name else "",
        #             text(self.parser.pos_to_linecol(self.position)),
        #             self.parser.context(position=self.position))
        RE = r'^Expected (?P<tokens>.*) ' \
             r'at position (.*):\(\d+, \d+\)'\
             r' => \'(?P<cursor>.*)\'\.'
        m=re.match(RE, e.message)
        if m is not None:
            tokens=m.group('tokens').split(' or ')
            cursor=m.group('cursor')
            return TokenBasedSyntaxicError(
                message=e.message,
                line=e.line,
                column=e.col,
                tokens=tokens,
                cursor=cursor)
        else:
            return SyntaxicError(
                message=e.message,
                line=e.line,
                column=e.column,
            )


    def __init__(self, grammar, file):
        #type: (Grammar, Text) -> None
        """
        Bracket the file for nested parsing and then parse the file.
        This could raise a TextXError if the analyzer fail to recognize
        a valid file.
        """
        self.grammar=grammar
        self.file=file
        self.basename=os.path.basename(self.file)
        self.bracketedFile=\
            BracketedScript(self.file).save()
        self.model=self.grammar.metamodel.model_from_file(
            self.bracketedFile)
        # instrument textx model with a reference back to this object
        self.model.ast=self
        # self.bracketedtext=brackets.BracketedScript(self.file).text
        # self.model=self.grammar.metamodel.model_from_str(
        #     self.bracketedtext)

    def pos(self, astNode):
        return self.grammar.parser.pos_to_linecol(
            astNode._tx_position)

    def posEnd(self, astNode):
        return self.grammar.parser.pos_to_linecol(
            astNode._tx_position_end)

    def line(self, astNode):
        (l,c)=self.pos(astNode)
        return l

    def column(self, astNode):
        (l,c)=self.pos(astNode)
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
    def __init__(self, grammar, modelSourceFile, fileName):
        self.sourceFile=modelSourceFile
        super(ModelSourceAST, self).__init__(
            grammar=grammar,
            #file=modelSourceFile.fileName
             file=fileName  # modelSourceFile.fileName
        )


class ASTBasedModelSourceFile(ASTBasedModelSourceFile):
    """
    Source file with a model produced via an AST.
    """
    def __init__(self, fileName, grammarFile):
        #type: (Text, Text) -> None

        # self.grammar=Grammar(grammarFile)
        # #type:

        # self.ast=None  #type: Optional[ModelSourceAST]

        # filled just below
        # type: Optional[ModelSourceAST]
        # self.ast=ModelSourceAST(self.grammar, self, fileName)


        super(ASTBasedModelSourceFile, self).__init__(
            fileName,
            grammarFile)
        # self.ast=ModelSourceAST(self.grammar, self, fileName)

    def fillModel(self):
        # self.ast=ModelSourceAST(self.grammar, self)
        self.model.description = astTextBlockToTextBlock(
            container=self.model,
            astTextBlock=(
                self.ast.model.megamodelPart.modelDefinition.textBlock))
        self.parseMainBody()

    @abstractmethod
    def parseMainBody(self):
        raise NotImplementedError()




class ASTNodeSourceIssue(LocalizedSourceIssue):
    """
    An issue based on a ASTNode.
    """
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
