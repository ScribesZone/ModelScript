from typing import Union, List
import glob
import os
import re
import sys
from distutils.dir_util import mkpath

TEST_CASES_DIRECTORY = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '..', 'testcases')


VERIFIED_OUTPUT_DIRECTORY = os.path.join(
    TEST_CASES_DIRECTORY,
    'out-generated')


GENERATED_OUTPUT_DIRECTORY = os.path.join(
    TEST_CASES_DIRECTORY,
    'out-verified')


def _getDir(absolutePath, relDir, ensure=True):
    dir = os.path.join(absolutePath, relDir)
    if not os.path.exists(dir):
        if ensure:
            mkpath(dir)
        else:
            raise IOError(  # raise:OK
                'TST: Directory %s does not exist.' % dir)
    return dir


def getTestDir(relDir, ensure=True):
    """Get an absolute directory from a relative one.
    The directory can be created as necessary with the parameter ensure.
    """
    return _getDir(TEST_CASES_DIRECTORY, relDir, ensure)


def getTestFile(relativeFileName, checkExist=True):
    f = os.path.join(
        TEST_CASES_DIRECTORY,
        relativeFileName
    )
    if checkExist:
        if not os.path.isfile(f):
            raise IOError(  # raise:OK
                'TST: test file %s not found.' % relativeFileName)
    return f


def getTestFiles(
        relativeDirectory: str,
        relative:  bool = True,
        extension: Union[str, List[str]] = '',
        pattern='') \
        -> List[str]:

    def accept(filename):
        (core, ext)=os.path.splitext(filename)
        if pattern != '':
            m = re.search(pattern, core)
            if not m:
                return False
        if isinstance(extension, str):
            return ext == extension
        elif isinstance(extension, list):
            return ext in extension
        else:
            raise NotImplementedError( #raise:OK
                'TST: unexpected extension type: %s'
                % type(extension))

    absolute_test_dir=os.path.join(
        TEST_CASES_DIRECTORY,
        relativeDirectory)
    if not os.path.isdir(absolute_test_dir):
        raise ValueError(  # raise:OK
            'TST: Not a test directory : %s'
            % relativeDirectory)

    rel_files=[
        (os.path.join(
            relativeDirectory if relative else absolute_test_dir,
            simplename))
        for simplename in os.listdir(absolute_test_dir)
        if accept(simplename) ]
    return rel_files

#
# def getOutputGeneratedFile(testname):
#     return

def patternFromArgV():
    prefix = '-e='
    for arg in sys.argv:
        if arg.startswith(prefix):
            return arg[len(prefix):]
    else:
        return ''



def setup():
    pass



def teardown():
    pass