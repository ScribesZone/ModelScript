# coding=utf-8

from typing import Callable, Any
import io
import os
from distutils.dir_util import mkpath

from modelscripts.base.issues import (
    Levels,
    Issue
)

__all__=(
    'ensureDir',
    'extension',
    'withoutExtension',
    'replaceExtension',
    'raiseIssueOrException',
    'readFileLines',
    'writeFile',
    'writeFileLines'
)

def ensureDir(dir):
    if not os.path.isdir(dir):
        try:
            mkpath(dir)
        except:
            raise IOError('Cannot create directory %s' % dir)

def extension(path):
    filename, file_extension =os.path.splitext(os.path.basename(path))
    return file_extension

def withoutExtension(path):
    filename, file_extension =os.path.splitext(path)
    return filename

def replaceExtension(path, ext):
    return withoutExtension(path)+ext


def raiseIssueOrException(exception, message, issueOrigin):
    if issueOrigin is None:
        raise exception
    else:
        Issue(
            origin=issueOrigin,
            level=Levels.Fatal,
            message=message
        )

def readFileLines(
        file,
        issueOrigin=None,
        message='Cannot read file %s'):
    try:
        with io.open(file,
                     'rU',
                     encoding='utf8') as f:
            lines = list(
                line.rstrip() for line in f.readlines())
        return lines
    except Exception as e:
        raiseIssueOrException(
            e,
            message % file,
            issueOrigin)

def writeFile(
        text,
        filename,
        # extension='.txt',
        issueOrigin=None,
        message='Cannot write file'):
    try:
        # if outputFileName is not None:
        # else:
        #     (f, filename) = (
        #         tempfile.mkstemp(
        #             suffix=extension,
        #             text=True))
        #     os.close(f)
        import codecs
        with codecs.open(filename, "w", "utf-8") as f:
            f.write(text)
        return filename
    except Exception as e:
        raiseIssueOrException(
            exception=e,
            message=message,
            issueOrigin=issueOrigin)

def writeFileLines(
        lines,
        filename,
        issueOrigin=None,
        message='Cannot write file'):
    return writeFile(
        text='\n'.join(lines),
        filename=filename,
        issueOrigin=issueOrigin,
        message=message)