# coding=utf-8
import os
import tempfile
from modelscript.base.files import (
    ensureDir,
    extension,
    writeFileLines,
    writeFile
)
from modelscript.base.exceptions import (
    FileSystemError,
    UnexpectedCase)


def replaceExtension(filename, extension):
    return os.path.splitext(filename)[0] + extension

class Environment(object):
    """
    Given access to various directories. These
    directories can serve for user preferences and configuration
    files (~/.mdl directory), but also for the "worker" to
    save final and intermediate files.

    The last case is for the "worker". A worker can save files
    in different "spaces", with 4 possible spaces:

    *   "self". the same directory as the original files.
    *   "inline". the ".mdl/tmp" in the original dir.
    *   "tmp". the system temporary directory.
    *   "home". the directory ~/.mdl/tmp
    """

    workerDirName='.mdl'
    workerSpace='inline' # inline | tmp | home | self
    _userHomeDir=os.path.expanduser("~")
    _userModelDir=None  # ~/.mdl
    _workerDir=None     # ~/.mdl/tmp

    @classmethod
    def getUserModelDir(cls):
        """
        The user .mdl directory, "~/.mdl", created on demand
        """
        if cls._userModelDir is not None:
            return cls._userModelDir
        dir=os.path.join(
            cls._userHomeDir,
            '.mdl')
        ensureDir(dir)
        cls._userModelDir=dir
        return cls._userModelDir

    @classmethod
    def _getHomeWorkerDir(cls):
        """
        The worker directory with "home" option: ~/.mdl/tmp
        """
        if cls._workerDir is not None:
            return cls._workerDir
        dir=os.path.join(
            cls.getUserModelDir(),
            'tmp')
        ensureDir(dir)
        cls._workerDir=dir
        return cls._workerDir

    @classmethod
    def getWorkerFileName(cls,
                          basicFileName,
                          extension=None,
                          workerSpace=None):
        """
        Return
        :param basicFileName: The original filename.
        :param workerSpace: the work space choosen ('inline', 'home', etc.)
            If not given, select the environment wide default.
        :return: The full file name for the worker.
        """

        def _getInlineWorkerDir(filename):
            """
            Return the directory .mdl/tmp relative to the file
            given. Create the directory if not existing
            """
            d = os.path.dirname(
                os.path.realpath(filename))
            dir = os.path.join(d, cls.workerDirName, 'tmp')
            ensureDir(dir)
            return dir

        if extension is None:
            filename=basicFileName
        else:
            filename=replaceExtension(basicFileName, extension)

        space=cls.workerSpace if workerSpace is None else workerSpace

        if space=='self':
            # do not change anything
            return filename
        elif space=='inline':
            # filename will go in .mdl/tmp/base
            return os.path.join(
                _getInlineWorkerDir(filename),
                os.path.basename(filename)
            )

        elif space=='tmp':
            # filename will go in temp directory with
            # arbitrary name
            # the extension if kept though from
            # given filename
            try:
                (f, tmp_file) = tempfile.mkstemp(
                    suffix=extension(filename),
                    text=True)
                os.close(f)
                return tmp_file
            except Exception: #except:OK
                raise FileSystemError( #raise:OK
                    'Cannot create file in'
                    ' system temporary directory.')
        elif space=='home':
            # TODO:4 could be use if need to flatten names
            # @classmethod
            # def pathToLabel(cls, path, last=1):
            #     all=path.split(os.path.sep)
            #     if last is not None:
            #         all=all[-last:]
            #     return '_'.join(all)

            worker_home=cls._getHomeWorkerDir()
            # do not use os.path.join as it remove the first
            # dir if the second is absolute
            dir=os.path.normpath(os.path.sep.join(
                [os.path.sep]
                + worker_home.split(os.path.sep)
                + os.path.dirname(filename).split(os.path.sep)))
            ensureDir(dir)
            return os.path.join(dir, os.path.basename(filename))
        else:
            raise UnexpectedCase(
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
            origin=issueOrigin)
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










