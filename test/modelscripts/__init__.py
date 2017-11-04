# coding=utf-8
import os
import glob
from typing import Text, Union, List, Dict

TEST_CASES_DIRECTORY = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'testcases')
BUILD_DIRECTORY = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'build')


def getFile(name, prefixes):
    if os.path.isabs(name):
        return name
    else:
        return os.path.join(*[TEST_CASES_DIRECTORY] + prefixes + [name])

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

def getTestFile(relativeFileName, checkExist=True):
    f=os.path.join(
        TEST_CASES_DIRECTORY,
        relativeFileName
    )
    if checkExist:
        if not os.path.isfile(f):
            raise IOError('Test file %s not found' % relativeFileName)
    return f

def getTestDir(relativeDir, exist=True):
    d=os.path.join(
        TEST_CASES_DIRECTORY,
        relativeDir
    )
    if exist:
        if not os.path.isdir(d):
            raise IOError('Test directory %s not found' % relativeDir)
    return d


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
    if not os.path.isdir(BUILD_DIRECTORY):
        os.mkdir(BUILD_DIRECTORY)

def teardown():
    pass
