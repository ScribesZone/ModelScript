# coding=utf-8
# coding=utf-8
import os
import glob
from typing import Text, Union, List
from distutils.dir_util import mkpath

TEST_CASES_DIRECTORY = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '..', 'testcases')
BUILD_DIRECTORY = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'build')

#=====================================================================
#                      Directory and files
#=====================================================================


def _getDir(absolutePath, relDir, ensure=True):
    dir=os.path.join(absolutePath, relDir)
    if not os.path.exists(dir):
        if ensure:
            mkpath(dir)
        else:
            raise IOError('Directory %s does not exist.' % dir)
    return dir

def getBuildDir(relDir, ensure=True):
    return _getDir(BUILD_DIRECTORY, relDir, ensure)

def getTestDir(relDir, ensure=True):
    return _getDir(TEST_CASES_DIRECTORY, relDir, ensure)


def getFile(name, prefixes):
    if os.path.isabs(name):
        return name
    else:
        return os.path.join(*[TEST_CASES_DIRECTORY] + prefixes + [name])

def getTestFile(relativeFileName, checkExist=True):
    f=os.path.join(
        TEST_CASES_DIRECTORY,
        relativeFileName
    )
    if checkExist:
        if not os.path.isfile(f):
            raise IOError('Test file %s not found' % relativeFileName)
    return f

def getTestFiles(relativeDirectory, relative=True, extension=''):
    #type: (Text, bool, Union[Text, List[Text]]) -> List[Text]
    def accept(filename):
        (core, ext)=os.path.splitext(filename)
        if isinstance(extension, (str, unicode)):
            return ext==extension
        elif isinstance(extension, list):
            return ext in extension
        else:
            raise NotImplementedError()

    absolute_test_dir=os.path.join(
        TEST_CASES_DIRECTORY,
        relativeDirectory)
    if not os.path.isdir(absolute_test_dir):
        raise ValueError('Not a test directory : %s' % relativeDirectory)

    rel_files=[
        (os.path.join(
            relativeDirectory if relative else absolute_test_dir,
            simplename))
        for simplename in os.listdir(absolute_test_dir)
        if accept(simplename) ]
    return rel_files






#----------- testing issues ------------------------------












def getUseFile(name):
    return getFile(name,['use'])

def getSoilFile(name):
    return getFile(name, ['soil'])

def getSoilFileList(nameOrList):
    if isinstance(nameOrList, (str, unicode)):
        # add the prefix if necessary
        with_prefix = getFile(nameOrList, ['soil'])
        return glob.glob(with_prefix)
    else:
        return map(getSoilFile, nameOrList)

def getZipFile(name):
    for prefix in ['http:','https:','ftp:','ftps:']:
        if name.startswith(prefix):

            return name
    return getFile(name, ['zip'])

def setup():
    pass
    # if not os.path.isdir(BUILD_DIRECTORY):
    #     os.mkdir(BUILD_DIRECTORY)

def teardown():
    pass
