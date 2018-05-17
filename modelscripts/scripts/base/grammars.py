import sys
import os

from textx import metamodel_from_file
from textx.export import (
    metamodel_export,
    model_export
)


import brackets

class Grammar(object):
    def __init__(self, language,
                 grammarDirectory ):
                 # useLanguageCode=False):
        self.language=language
        # self.languageCode=language[0:2]
        # if useLanguageCode:
        #     self.directory=os.path.join(
        #         grammarDirectory, self.languageCode)
        # else:
        #     self.directory=grammarDirectory
        self.directory=grammarDirectory
        self.file=os.path.join(self.directory,language+'.tx')
        self.metamodel=metamodel_from_file(self.file)
        self.metamodel.auto_init_attributes=False

    def visualize(self):
        dot_file=self.file+'.dot'
        metamodel_export(self.metamodel, dot_file)
        os.system('dot -Tpng -O %s' % dot_file)


class AST(object):
    def __init__(self, grammar, file):
        self.grammar=grammar
        self.file=file
        self.bracketedFile=brackets.BracketedScript(self.file).save()
        self.model=self.grammar.metamodel.model_from_file(
            self.bracketedFile)
        # self.bracketedtext=brackets.BracketedScript(self.file).text
        # self.model=self.grammar.metamodel.model_from_str(
        #     self.bracketedtext)

    def visualize(self):
        dot_file=self.file+'.dot'
        model_export(self.model, dot_file)
        os.system('dot -Tpng -O %s' % dot_file)



if __name__ == "__main__":

    grammar_directory = sys.argv[1]
    language_name = sys.argv[2]
    script_file = sys.argv[3]

    print('Loading %s grammar ... ' % language_name)
    grammar = Grammar(language_name, grammar_directory)
    grammar.visualize()
    print('OK')

    print('Loading script %s ...' % script_file)
    ast=AST(grammar, script_file)
    ast.visualize()
    print('OK')

