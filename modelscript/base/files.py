# coding=utf-8
"""Helpers dealing with file management."""

__all__=(
    'ensureDir',
    'extension',
    'withoutExtension',
    'replaceExtension',
    'readFileLines',
    'writeFile',
    'writeFileLines'
)

from typing import Optional, List, Union, Iterable
import io
import os
from distutils.dir_util import mkpath

from modelscript.base.issues import (
    Levels,
    Issue,
    WithIssueList)




def ensureDir(dir: str) -> None:
    """ Make sur that a directory exist. Create it if necessary.
    Raises:
        IOError
    """
    if not os.path.isdir(dir):
        try:
            mkpath(dir)
        except Exception:  # except:OK
            raise IOError(
                'Cannot create directory %s' % dir)  # raise:TODO:3


def extension(path: str) -> str:
    """ Extension of a file. """
    filename, file_extension = os.path.splitext(os.path.basename(path))
    return file_extension


def withoutExtension(path: str) -> str:
    """ Filename without the extension """
    filename, file_extension =os.path.splitext(path)
    return filename


def replaceExtension(path: str, ext: str) -> str:
    """ Replace the extension of a file """
    return withoutExtension(path)+ext


def filesInTree(
        directory: str,
        suffix: Union[str, Iterable[str]]) \
        -> List[str]:
    """Search for all filenames ending with the suffix(es).

    Args:
        directory: the directory where to search.
        suffix: a string or a list of string serving as suffixes.

    Returns:
        The list of filenames ending with the suffix(es).
    """
    if isinstance(suffix,str):
        suffixes = [suffix]
    else:
        suffixes = suffix
    _ = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            for s in suffixes:
                if file.endswith(s):
                    path = os.path.join(root, file)
                    _.append(path)
                    break
    return _


# -------------------------------------------------------------------------
# Issue-based file operations
# -------------------------------------------------------------------------

def _raiseIssueOrException(
        exception: Exception,
        message: str,
        origin: Optional[WithIssueList]) -> Issue:
    """Raise an issue or an exception depending on the issue of origin.
    If the issue of origin is None, the raise the given exception.
    Otherwise raise a fatal issue with the given message and the given
    origin of issue.

    Args:
        exception: The exception to raise if necessary.
        message: The message of the issue to be raised if necessary.
        origin: The issue of origin used to determine
            whether to raise an exception or an issue.
    Returns:
        Returns an fatal issue or raise an exception.

    Raises:
        Raises the provided exception if issueOrigin is none.
    """
    if origin is None:
        raise exception  # raise:TODO:1
    else:
        assert isinstance(origin, WithIssueList)
        Issue(
            origin=origin,
            level=Levels.Fatal,
            message=message
        )


def readFileLines(
        file: str,
        origin: Optional[WithIssueList] = None,
        message: str = 'Cannot read file %s')\
        -> List[str]:
    """Read a file as a set of lines.
    This function can raise an issue or exception.

    Args:
        file: The name of the file to read.
        origin: The issue of origin, if any.
        message: The message of the issue to create in case of errors.

    Returns:
        The list of lines read from the files.
        TODO:1 check what happen when an issue is produced
        Currently the method return None...
    """
    try:
        with io.open(file,
                     'rU',
                     encoding='utf8') as f:
            lines = list(
                line.rstrip() for line in f.readlines())
        return lines
    except Exception as e:
        # What happen with issue is not clear
        _raiseIssueOrException(
            e,
            message % file,
            origin)


def writeFile(
        text: str,
        filename: str,
        origin: Optional[Issue] = None,
        message: str = 'Cannot write file')\
        -> str :
    """Write a file.
    This function can raise an issue or exception.

    Args:
        text: The text to write in the file.
        filename: The name of the file to be written.
        origin: The issue of origin, if any.
        message: The message of the issue to create in case of errors.

    Returns:
        Return the name of the file written.
        TODO:1 check what happen when an issue is produced
        Currently the method return None...

    """
    try:
        import codecs
        with codecs.open(filename, "w", "utf-8") as f:
            f.write(text)
        return filename
    except Exception as e:
        _raiseIssueOrException(
            exception=e,
            message=message,
            origin=origin)


def writeFileLines(
        lines: List[str],
        filename: str,
        issueOrigin: Optional[Issue] = None,
        message='Cannot write file'):

    return writeFile(
        text='\n'.join(lines),
        filename=filename,
        origin=issueOrigin,
        message=message)


