# coding=utf-8

from typing import Callable, Any
import io
import tempfile
import os

from modelscribes.base.issues import (
    Levels,
    Issue
)

def raiseIssueOrException(exception, message, issueOrigin):
    if issueOrigin is None:
        raise exception
    else:
        Issue(
            origin=issueOrigin,
            level=Levels.Fatal,
            message=message % file
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



def writeTmpFile(
        text,
        extension='.txt',
        issueOrigin=None,
        message='Cannot write tmp file'):
    try:
        (f, tmp_filename) = (
            tempfile.mkstemp(
                suffix=extension,
                text=True))
        os.close(f)
        import codecs
        with codecs.open(tmp_filename, "w", "utf-8") as f:
            f.write(text)
        return tmp_filename
    except Exception as e:
        raiseIssueOrException(
            exception=e,
            message=message,
            issueOrigin=issueOrigin)

def writeTmpFileLines(
        lines,
        extension='.txt',
        issueOrigin=None,
        message='Cannot write tmp file'):
    return writeTmpFile(
        text='\n'.join(lines),
        extension=extension,
        issueOrigin=issueOrigin,
        message=message)