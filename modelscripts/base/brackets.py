import re

# The following dependencies could be removed if necessary.
# The environment is used only to save bracketed file in a
# convenient way.

from modelscripts.interfaces.environment import Environment

class BracketError(Exception):

    def __init__(self, message, line):
        super(BracketError, self).__init__(message)
        self.line = line


class BracketedScript(object):

    SPACE_INDENT=4
    # OPENING_BRACKET='{_'
    OPENING_BRACKET='\000{'
    # CLOSING_BRACKET='}_'
    CLOSING_BRACKET='\000}'
    #EOL=';_'
    EOL='\000;'
    IS_BLANK_LINE='^ *(#.*)?$'
    IS_DOC_LINE_REGEX='^ *\|'
    # CLOSING_DOC_LINE='|_'
    CLOSING_DOC_LINE='\000|'
    # DOC_LINE_CONTENT=' *\| ?(?P<content>.*)\|_;_(}_;_)*$'
    DOC_LINE_CONTENT=' *\| ?(?P<content>.*)\000\|\000;(\000}\000;)*$'


    def __init__(self, file):
        self.file=file
        self.lines=[line.rstrip('\n') for line in open(file)]
        self.bracketedLines=[]
        # basic_file_name=(
        #     self.file+'b' if targetFilename is None
        #     else targetFilename
        # )
        basic_file_name = self.file+'b'
        self.targetFilename=Environment.getWorkerFileName(basic_file_name)

    def _is_blank_line(self, index):
        """ Check if the line is blank or a comment line """
        m=re.match(self.IS_BLANK_LINE, self.lines[index])
        return m is not None

    def _is_doc_line(self, index):
        m=re.match(self.IS_DOC_LINE_REGEX, self.lines[index])
        return m is not None

    def _terminate_doc_line(self, docLine):
        return  docLine +self.CLOSING_DOC_LINE


    @classmethod
    def extractDocLineText(cls, docLine):
        m = re.match(cls.DOC_LINE_CONTENT, docLine)
        assert m is not None
        return m.group('content')

    def _nb_spaces(self, index):
        m=re.match(' *', self.lines[index])
        if m:
            return len(m.group(0))
        else:
            return 0

    def _line_indent(self, index):
        blanks=self._nb_spaces(index)
        if blanks % self.SPACE_INDENT==0:
            return blanks // self.SPACE_INDENT
        else:
            raise BracketError(
                message='%i spaces found. Multiple of %i expected.'
                        % (blanks, self.SPACE_INDENT),
                line=index+1)

    def _suffix(self, delta):
        if delta==1:
            return self.OPENING_BRACKET
        elif delta==0:
            return self.EOL
        else:
            return (
                self.EOL
                +  (self.CLOSING_BRACKET+self.EOL) * - delta
            )

    @property
    def text(self):
        self.bracketedLines=list(self.lines)
        # LNBL = Last Non Black Line
        lnbl_index=-1
        lnbl_indent=0
        # take all lines + a extra virtual line to close everything
        for (index, line) in enumerate(self.lines):
            if not self._is_blank_line(index):
                indent=self._line_indent(index)
                delta=indent-lnbl_indent
                if self._is_doc_line(index):
                    self.bracketedLines[index]=(
                        self._terminate_doc_line(self.bracketedLines[index])
                    )
                if delta>1:
                    # this will never happened for the last line

                    raise BracketError(
                        message='"%s"' % line,
                        line=index+1)
                else:
                    if lnbl_index!=-1:
                        self.bracketedLines[lnbl_index] += self._suffix(delta)
                lnbl_index=index
                lnbl_indent=indent
        # close the last line if any
        if lnbl_index!=-1:
            delta=0-lnbl_indent
            self.bracketedLines[lnbl_index] += self._suffix(delta)

        return '\n'.join(self.bracketedLines)

    def save(self):
        f = open(self.targetFilename, "w")
        f.write(self.text)
        f.close()
        return self.targetFilename

import sys
if __name__ == "__main__":
    source=sys.argv[1]
    text=BracketedScript(source).save()
