# coding=utf-8
"""Syntax related concepts.
Grammars, abstract syntax trees, syntax errors
"""

__all__ = (
    'Grammar',
    'Grammars',
    'AST',
    'ModelSourceAST',
    'SyntaxError',
    'TokenBasedSyntaxError',
    'ASTNodeSourceIssue'
)

import os
import sys
import re
from typing import  Dict, ClassVar, Tuple
from typing_extensions import Literal

from textx import metamodel_from_str
from textx.export import (
    metamodel_export,
    model_export)
from textx.model import get_model
from textx.metamodel import TextXMetaModel
# NOTE: the type TextXNode and TextXModel used below as types
# between quotes do not exist since they correspond to classes
# generated on the fly by textX and that have no superclasses.

from modelscript.base.brackets import (
    BracketedScript)
from modelscript.base.issues import (
    Level,
    LocalizedSourceIssue)
from modelscript.base.exceptions import (
    UnexpectedCase)

#TODO:4 remove the include grammar kludge

INCLUDES = (
    '../scripts/megamodels/parser/grammar.tx',
    '../scripts/textblocks/parser/grammar.tx',
    '../scripts/stories/parser/grammar.tx'
)
""" List of grammars to be included in all grammars.
This hack allows to avoid dealing with grammar dependencies.
Not really neat, but good enough for now.
"""

# TODO:2 Check how to deal with exception. Why not using the module files
def _read_file(filename):
    with open(filename, 'r') as content_file:
        content = content_file.read()
    return content


class Grammar(object):
    """Grammar and its metamodel."""
    file: str
    metamodel: TextXMetaModel

    def __init__(self, grammarFile: str) -> None:
        self.file = grammarFile
        full_grammar_text = self._get_grammar_str()
        self.metamodel = metamodel_from_str(full_grammar_text)
        self.metamodel.auto_init_attributes = False

    def _get_grammar_str(self) -> str:
        """Get the full grammar text.
        The content of the include files (see INCLUDES) are added
        at the end.
        """
        grammar_str = _read_file(self.file)
        this_dir = os.path.dirname(os.path.realpath(__file__))
        for include in INCLUDES:
            included_file = os.path.join(this_dir, include)
            grammar_str += '\n\n'
            grammar_str += _read_file(included_file)
        return grammar_str

    def visualize(self) -> None:
        dot_file = self.file+'.dot'
        metamodel_export(self.metamodel, dot_file)
        os.system('dot -Tpng -O %s' % dot_file)


class Grammars(object):
    """ Factory of grammars.
    This class avoid to create the same grammar multiple times.
    """
    _grammars: ClassVar[Dict[str, Grammar]] = {}
    """Map of grammars"""

    @classmethod
    def get(cls, grammarFile: str) -> Grammar:
        """Get the grammar corresponding to the given grammar file."""
        if grammarFile not in cls._grammars:
            grammar = Grammar(grammarFile)
            cls._grammars[grammarFile] = grammar
        return cls._grammars[grammarFile]


class SyntaxError(object):
    """Syntax error"""
    line: int
    column: int
    message: str

    def __init__(self, message, line, column):
        self.line = line
        self.column = column
        self.message = message


class TokenBasedSyntaxError(SyntaxError):

    def __init__(self,
                 message: str,
                 line: int,
                 column: int,
                 tokens,
                 cursor):

        super(TokenBasedSyntaxError, self).__init__(
            message, line, column
        )

        token_map = {
            'o_': 'OpenBlock',
            '_o': 'CloseBlock',
            'X': 'EndOfLine'
        }

        def cleaned_tokens(tokens):
            # eliminate duplicates
            ts = list(set(tokens))
            # replace key tokens
            for i, t in enumerate(ts):
                if t in token_map:
                    ts[i] = token_map[t]
            # limit to 10
            if len(ts) > 10:
                ts = ts[:10] + ['...']
            return ts

        self.tokens = cleaned_tokens(tokens)
        self.cursor = cursor
        self.message = (
            '(%i:%i): expecting %s' % (
                self.line,
                self.column,
                ', '.join(self.tokens)))


class AST(object):
    """An abstract syntax tree representing a script.
    This class is an abstraction over a textX model and deals with
    all aspects of parsing including bracketed scripts.
    """

    grammar: Grammar
    file: str
    bracketedFile: str
    model: 'TextXModel'

    def __init__(self, grammar: Grammar, file: str) -> None:
        """
        Create an abstract syntax tree given a file and its grammar.
        * (1) the source file is first bracketed to deal with indentation,
        * (2) the bracketed file is then parsed resulting in a textX model,
        * (3) the resulting model (a textX object) is instrumented with
              and an ".ast" attribute that point to this AST object.
              This allows navigating between textX model and this AST
              object.
        Raises:
            This method could raise a TextXError if the analyzer fail
            to recognize a valid file.
        """
        self.grammar = grammar
        self.file = file
        self.basename = os.path.basename(self.file)
        self.bracketedFile = \
            BracketedScript(self.file).save()
        self.model = self.grammar.metamodel.model_from_file(
            self.bracketedFile)
        # instrument textx model with a reference back to this object
        self.model.ast = self

    def pos(self, astNode: 'TextXNode') -> Tuple[int, int]:
        return self.model._tx_parser.pos_to_linecol(
            astNode._tx_position)

    def posEnd(self, astNode: 'TextXNode') -> Tuple[int, int]:
        return self.model._tx_parser.pos_to_linecol(
            astNode._tx_position_end)

    def line(self, astNode: 'TextXNode') -> int:
        (l,c) = self.pos(astNode)
        return l

    def column(self, astNode: 'TextXNode') -> int:
        (l,c) = self.pos(astNode)
        return c

    def lineEnd(self, astNode: 'TextXNode') -> int:
        (l,c) = self.posEnd(astNode)
        return l

    def columnEnd(self, astNode: 'TextXNode') -> int:
        (l,c) = self.posEnd(astNode)
        return l

    def visualize(self) -> None:
        dot_file = self.file+'.dot'
        model_export(self.model, dot_file)
        os.system('dot -Tpng -O %s' % dot_file)

    @classmethod
    def ast(cls, astNode: 'TextXNode') -> "TextXModel":
        """ Return the AST from a given ast node """
        # This implementation is based both on the get_model method from
        # textX and the fact that the textX model has been instrumented
        #  with an ast attribute to go from the textX model to AST.
        return get_model(astNode).ast

    @classmethod
    def nodeLine(cls, astNode: 'TextXNode') -> int:
        return AST.ast(astNode).line(astNode)

    @classmethod
    def nodeLineEnd(cls, astNode: 'TextXNode') -> int:
        return AST.ast(astNode).lineEnd(astNode)

    @classmethod
    def extractErrorFields(cls, e) -> SyntaxError:

        RE = r'^Expected (?P<tokens>.*) ' \
             r'at position (.*):\(\d+, \d+\)'\
             r' => \'(?P<cursor>.*)\'\.'
        m = re.match(RE, e.message)
        if m is not None:
            tokens = m.group('tokens').split(' or ')
            cursor = m.group('cursor')
            return TokenBasedSyntaxError(
                message=e.message,
                line=e.line,
                column=e.col,
                tokens=tokens,
                cursor=cursor)
        else:
            return SyntaxError(
                message=e.message,
                line=e.line,
                column=e.column,
            )


class ModelSourceAST(AST):
    """
    An AST but with "modelSourceFile" as an extra attribute.
    This attribute contains a model source file instead of
    just a plain filename.
    """
    def __init__(self, grammar, modelSourceFile, fileName):
        self.sourceFile = modelSourceFile
        super(ModelSourceAST, self).__init__(
            grammar=grammar,
            # file=modelSourceFile.fileName
            file=fileName  # modelSourceFile.fileName
        )


class ASTNodeSourceIssue(LocalizedSourceIssue):
    """
    An issue based on a ASTNode.
    """
    def __init__(self,
                 astNode: 'TextXNode',
                 level: Level,
                 message: str,
                 code=None,
                 position: Literal['before', 'after', None] = None) \
            -> None:
        ast = AST.ast(astNode)
        assert message is not None  # just for to check the signature
        if position is None:
            line = ast.line(astNode)
            column = ast.column(astNode)
        elif position == 'before':
            line = ast.line(astNode)
            column = ast.column(astNode)
        elif position == 'after':
            line = ast.lineEnd(astNode)
            column = ast.columnEnd(astNode)
        else:
            raise UnexpectedCase(  # raise:OK
                'Unexpected position: %s' % position)
        super(ASTNodeSourceIssue, self).__init__(
            code=code,
            sourceFile=ast.sourceFile,
            level=level,
            message=message,
            line=line,
            column=column
        )

# class ASTBasedModelSourceFile(ASTBasedModelSourceFile):
#     """
#     Source file with a model produced via an AST.
#     """
#     def __init__(self, fileName, grammarFile):
#         #type: (Text, Text) -> None
#
#         # self.grammar=Grammar(grammarFile)
#         # #type:
#
#         # self.ast=None  #type: Optional[ModelSourceAST]
#
#         # filled just below
#         # type: Optional[ModelSourceAST]
#         # self.ast=ModelSourceAST(self.grammar, self, fileName)
#
#
#         super(ASTBasedModelSourceFile, self).__init__(
#             fileName,
#             grammarFile)
#         # self.ast=ModelSourceAST(self.grammar, self, fileName)
#
#     def fillModel(self):
#         # self.ast=ModelSourceAST(self.grammar, self)
#         self.model.description = astTextBlockToTextBlock(
#             container=self.model,
#             astTextBlock=(
#                 self.ast.model.megamodelPart.modelDefinition.textBlock))
#         self.parseMainBody()
#
#     @abstractmethod
#     def parseMainBody(self):
#         raise MethodToBeDefined( #raise:TODO:4
#             'parseMainBody mist be redefined')

if __name__ == "__main__":

    grammar_file = sys.argv[1]
    print('Loading %s grammar ... ' % grammar_file)
    grammar = Grammar(grammar_file)
    grammar.visualize()
    print('OK')

    if len(sys.argv) >= 3:
        script_file = sys.argv[2]
        print('Loading script %s ...' % script_file)
        ast = AST(grammar, script_file)
        ast.visualize()
        print('OK')


