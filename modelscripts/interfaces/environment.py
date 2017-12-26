# coding=utf-8
import os
import tempfile
from modelscripts.base.files import (
    ensureDir,
    extension,
    writeFileLines,
    writeFile
)



class Environment(object):

    workerDirName='.mdls'
    workerSpace='inline' # inline | tmp | home | self
    _userHomeDir=os.path.expanduser("~")
    _userModelDir=None
    _workerDir=None

    @classmethod
    def getUserModelDir(cls):
        if cls._userModelDir is not None:
            return cls._userModelDir
        dir=os.path.join(
            cls._userHomeDir,
            '.mdl')
        ensureDir(dir)
        cls._userModelDir=dir
        return cls._userModelDir

    @classmethod
    def getHomeWorkerDir(cls):
        if cls._workerDir is not None:
            return cls._workerDir
        dir=os.path.join(
            cls.getUserModelDir(),
            'tmp')
        ensureDir(dir)
        cls._workerDir=dir
        return cls._workerDir

    @classmethod
    def getInlineWorkerDir(cls, filename):
        d=os.path.dirname(
                os.path.realpath(filename))
        dir=os.path.join(d,cls.workerDirName, 'tmp')
        ensureDir(dir)
        return dir


    @classmethod
    def getWorkerFileName(cls, basicFileName, workerSpace=None):
        space=cls.workerSpace if workerSpace is None else workerSpace
        if space=='self':
            # do not change anything
            return basicFileName
        elif space=='inline':
            # basicFileName will go in .modelscripts/tmp/base
            return os.path.join(
                cls.getInlineWorkerDir(basicFileName),
                os.path.basename(basicFileName)
            )
        elif space=='tmp':
            # basicFileName will go in temp directory with
            # arbitrary name
            # the extension if kept though from
            # given basicFileName
            try:
                (f, tmp_file) = tempfile.mkstemp(
                    suffix=extension(basicFileName),
                    text=True)
                os.close(f)
                return tmp_file
            except:
                raise IOError('Cannot create worker file.')
        elif space=='home':
            # TODO:5 could be use if need to flatten names
            # @classmethod
            # def pathToLabel(cls, path, last=1):
            #     all=path.split(os.path.sep)
            #     if last is not None:
            #         all=all[-last:]
            #     return '_'.join(all)

            worker_home=cls.getHomeWorkerDir()
            # do not use os.path.join as it remove the first
            # dir if the second is absolute
            dir=os.path.normpath(os.path.sep.join(
                [os.path.sep]
                + worker_home.split(os.path.sep)
                + os.path.dirname(basicFileName).split(os.path.sep)))
            ensureDir(dir)
            return os.path.join(dir, os.path.basename(basicFileName))
        else:
            raise NotImplementedError(
                'WorkerSpace not implemented: %s' % space )



    # @classmethod
    # def getWorkerFile(cls, tempDir=False, extension=None, name=None):
    #     assert (tempDir and name is None) or (not tempDir and name is not None)
    #     if tempDir:
    #         # create a temp file
    #         try:
    #             (f, worker_file) = tempfile.mkstemp(
    #                 suffix=extension,
    #                 text=True)
    #             os.close(f)
    #             return worker_file
    #         except:
    #             raise IOError('Cannot create build file.')
    #     else:
    #         assert name is not None
    #         worker_file=os.path.join(cls.getHomeWorkerDir(), name)
    #         print('UU'*10+' %s '% worker_file)
    #         return worker_file

    @classmethod
    def writeWorkerFile(cls,
                        text,
                        basicFileName,
                        workerSpace=None,
                        # tempDir=False,
                        # extension=None,
                        issueOrigin=None):
        filename=cls.getWorkerFileName(
            basicFileName=basicFileName,
            workerSpace=workerSpace)
        writeFile(
            text=text,
            filename=filename,
            issueOrigin=issueOrigin)
        return filename

    @classmethod
    def writeWorkerFileLines(cls, lines, basicFileName, workerSpace=None,
                        issueOrigin=None):
        filename=cls.getWorkerFileName(
            basicFileName=basicFileName,
            workerSpace=workerSpace)
        writeFileLines(
            lines=lines,
            filename=filename,
            issueOrigin=issueOrigin)
        return filename










