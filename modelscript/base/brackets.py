# coding=utf-8
""" Conversion of a regular indented file into a bracketed file.
This module makes it possible to use regular parser like textX
with indented based language. Basically BracketedScript is a
preprocesssor that replace all indentations by some "brackets"
like { and } so that a parser can find these block markers.

The preprocessor is aware of comments (//) and documentation
lines (starting with |).

Consider for instance the following text ::

    class model Cl_association01

    class Elephant
    class Banana
    class Tree

    abstract association class Meal
        | Take record of the bananas eaten by elephants.
        roles
            eater : Elephant[0..1]
            bananas : Banana[*]

The text above is bracketed as following. The character separator
are prefixed with special character to avoid confusion with the text
itself. ::

    class model Cl_association01 ;

    class Elephant ;
    class Banana ;
    class Tree ;

    abstract association class Meal {
        | Take record of the bananas eaten by elephants. | ;
        roles {
            eater : Elephant[0..1] ;
            bananas : Banana[*] ; } ; } ;

For more examples see for instance testcases/cls/.mdl/*.clsb
"""

__all__ = (
    'BracketError',
    'BracketedScript'
)

from typing import Match, ClassVar, List
import re

# The following dependencies could be removed if necessary.
# The environment is used only to save bracketed file in a
# convenient way.

from modelscript.interfaces.environment import Environment


class BracketError(Exception):
    """ Error message for an illegal indentation. """

    def __init__(self, message, line):
        super(BracketError, self).__init__(message)
        self.line = line


class BracketedScript(object):
    """ Converter of a indented file into a bracketed file.
    """

    # -- input parameters ------------------------------------------

    SPACE_INDENT: int = 4
    """ Number of spaces for each indentation. """

    IS_BLANK_LINE: ClassVar[Match[str]] = \
        re.compile('^ *((--[^@|]*)|(//.*))?$')
    """ Regular expressions matching blank lines (includes comments).
    Comments are just ignored for indentation purposes but they are still 
    taken into account for regular parsing.
    The definition of comments is also implemented in the grammar 
    textblocks/parser/grammar.tx 
    """
    # TODO:2 remove support for ModelScript. See below
    # ModelScript1:
    #      added [^@\|] so that --@ and --| are not treated as comment

    IS_DOC_LINE_REGEX: ClassVar[Match[str]] = re.compile('^ *\|')
    """ Regular expression for a documentation line. """

    # -- output parameters -----------------------------------------

    OPENING_BRACKET: ClassVar[str] = '\000{'
    """ Opening bracket string. """

    CLOSING_BRACKET: ClassVar[str] = '\000}'
    """ Closing bracket string. """

    EOL: ClassVar[str] = '\000;'
    """ End of line string. """

    CLOSING_DOC_LINE: ClassVar[str] = '\000|'
    """ Closing documentation line string. """

    DOC_LINE_CONTENT: ClassVar[Match[str]] = \
        re.compile(' *\| ?(?P<content>.*)\000\|\000;(\000}\000;)*$')
    """ Regular expression for a documentation line. """

    # -- output parameters -----------------------------------------

    file: str
    """ Name of the input file. """

    lines: List[str]
    """ Content of the input file represented as list of lines. """

    bracketedLines: List[str]
    """ """

    targetFilename: str
    """ Name of the output file.
    The location of the output file is computed by the Environment.
    See  modelscript.interfaces.environment. """

    def __init__(self, file: str) -> None:
        self.file = file
        self.lines = [line.rstrip('\n') for line in open(file)]
        self.bracketedLines = []
        basic_file_name = self.file+'b'
        self.targetFilename = Environment.getWorkerFileName(basic_file_name)

    def _is_blank_line(self, index: int) -> bool:
        """ Check if the line is blank or a comment line """
        m = re.match(self.IS_BLANK_LINE, self.lines[index])
        return m is not None

    def _is_doc_line(self, index: int) -> bool:
        m = re.match(self.IS_DOC_LINE_REGEX, self.lines[index])
        return m is not None

    def _terminate_doc_line(self, docLine: str) -> str:
        return docLine + self.CLOSING_DOC_LINE

    @classmethod
    def extractDocLineText(cls, docLine: str) -> str:
        m = re.match(cls.DOC_LINE_CONTENT, docLine)
        assert m is not None
        return m.group('content')

    def _nb_spaces(self, index: int) -> int:
        m = re.match(' *', self.lines[index])
        if m:
            return len(m.group(0))
        else:
            return 0

    def _line_indent(self, index: int) -> int:
        blanks = self._nb_spaces(index)
        if blanks % self.SPACE_INDENT  == 0:
            return blanks // self.SPACE_INDENT
        else:
            raise BracketError(  # raise:OK
                message = '%i spaces found. Multiple of %i expected.'
                        % (blanks, self.SPACE_INDENT),
                line = index+1)

    def _suffix(self, delta: int) -> str:
        if delta == 1:
            return self.OPENING_BRACKET
        elif delta == 0:
            return self.EOL
        else:
            return (
                self.EOL
                +  (self.CLOSING_BRACKET+self.EOL) * - delta
            )

    @property
    def text(self) -> str:
        """ Returns the bracketed text. """
        self.bracketedLines = list(self.lines)
        # LNBL = Last Non Black Line
        lnbl_index = -1
        lnbl_indent = 0
        # take all lines + a extra virtual line to close everything
        for (index, line) in enumerate(self.lines):
            if not self._is_blank_line(index):
                indent = self._line_indent(index)
                delta = indent-lnbl_indent
                if self._is_doc_line(index):
                    self.bracketedLines[index] = (
                        self._terminate_doc_line(self.bracketedLines[index])
                    )
                if delta > 1:
                    # this will never happened for the last line

                    raise BracketError(  # raise:OK
                        message = '"%s"' % line,
                        line=index+1)
                else:
                    if lnbl_index != -1:
                        self.bracketedLines[lnbl_index] \
                            += self._suffix(delta)
                lnbl_index = index
                lnbl_indent = indent

        # close the last line if any
        if lnbl_index != -1:
            delta = 0-lnbl_indent
            self.bracketedLines[lnbl_index] += self._suffix(delta)

        return '\n'.join(self.bracketedLines)

    def save(self) -> str:
        """ Save the bracked text into the output file.
        :return: the name of the output file
        """
        f = open(self.targetFilename, "w")
        f.write(self.text)
        f.close()
        return self.targetFilename


import sys

if __name__ == "__main__":
    source=sys.argv[1]
    text = BracketedScript(source).save()
