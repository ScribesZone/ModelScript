# coding=utf-8
"""Annotations in the form of ******** like parts embedded in source code
for instance to display information about errors.
"""

__all__ = (
    'Annotations'
)

import re
import os
import tempfile
from typing import Text, Optional

class Annotations(object):
    lineLength = 80
    char = '*'
    full = char*lineLength
    prefix = char*4+' '
    cont = char*2+'   '

    @classmethod
    def fullLine(cls, text):
        """ Full line of * """
        _ = cls.prefix+text+' '
        return _+cls.char*(cls.lineLength-len(_))

    @classmethod
    def _regexp(cls):
        return (r'^ *(%s|%s)' % (
            re.escape(Annotations.prefix),
            re.escape(Annotations.cont)
        ))

    @classmethod
    def _match(cls, line):
        return re.match(cls._regexp(), line)

    @classmethod
    def filterText(cls, text):
        return '\n'.join(
            [
                line for line in text.split('\n')
                if not cls._match(line) ])

    @classmethod
    def filterFile(cls,
                   filename: str,
                   createTmpFile: bool = True)\
            -> Optional[str]:

        def tmp_file():
            _, extension = os.path.splitext(filename)
            (f, tmp_filename) = (
                tempfile.mkstemp(
                    suffix='_'+extension,
                    text=True))
            os.close(f)
            return tmp_filename

        with open(filename, 'rU') as f:
            text = f.read()
        new_text = cls.filterText(text)
        has_changed = new_text != text
        if has_changed:
            new_filename=tmp_file() if createTmpFile else filename
            with open(new_filename, 'w') as f:
                f.write(new_text)
            return new_filename
        else:
            return None




