# coding=utf-8

"""
Wrapper to the USE engine. Call the 'use' command.
If "use" command is not in the system path, then
the value UseEngine.USE_OCL_COMMAND should be set explicitely.
"""



from typing import Text, Optional

import logging
import os
import re
from modelscripts.config import Config
from modelscripts.interfaces.environment import Environment
from modelscripts.base.files import (
    replaceExtension,
    readFileLines,
    writeFileLines
)
__all__ = [
    'USEEngine',
]

# logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('test.' + __name__)

DEBUG=4

#: Path of to the use command binary.
#: If the default value (``"use"``) does not work,
# for instance if the use binary is not in the system
# path, you can change this value either in the source,
# or programmatically using something like ::
#:
#:     USEEngine.USE_OCL_COMMAND = \
#          r'c:\Path\To\UseCommand\bin\use'


USE_SYSTEM_INSTALLED_USE=False

if USE_SYSTEM_INSTALLED_USE:
    USE_OCL_COMMAND = 'use'
else:
    USE_OCL_COMMAND=os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'res','use-4.1.1','bin', 'model-use')


class USEEngine(object):
    """
    Wrapper to the "use" command.
    """

    #: Last command executed by the engine
    command = None

    #: Directory in which the last command was executed
    directory = None

    #: Exit code of last execution (or None for before any execution)
    commandExitCode = None

    #: Output of last execution in case of separated out/err
    out = None

    #: Errors of last execution in case of separated out/err
    err = None

    #: Combined output & errors for last execution if merged out/err
    outAndErr = None


    @classmethod
    def _soilHelper(cls, name):
        #type: (Text)->Text
        soil= os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'res', name)
        if not os.path.isfile(soil):
            raise EnvironmentError(
                'Wrong installation. %s not found!' %
                soil)
        else:
            return soil


    @classmethod
    def _execute(cls,
                 useSource,
                 soilSource,
                 basicFileName,
                 workerSpace=None,
                 errWithOut=False,
                 executionDirectory=None):
        #type: (Text, Text, Text, Text, bool, Text) -> int

        """
        Execute use command with the given model and given soil file.
        This method is private and is not expected to be used direcltly.
        The soil file **MUST** terminate by a 'quit' statement so that
        the process finish. There is therefore always a soil file, at least
        to quit and even if the goal is just to compile a model.

        # it seems that this is not necessary. So remove this.
        #    The process is executed in the specified 'executionDirectory'.
        #    If not specified the execution directory is set to the directory
        #    of the use file given as a parameter. This directory could be
        #    important if the soil files contains references to relative path.
        #    This is in particular the case of 'open file.soil' rules.
        """

        # def getWorkerFileLabel():
        #     if workerFileLabel is not None:
        #         worker_file_label=workerFileLabel
        #     else:
        #
        #         use_source_label=Environment.pathToLabel(
        #             originalUseSource if originalUseSource is not None
        #             else useSource)
        #         soil_source_label=Environment.pathToLabel(
        #             originalSoilSource if originalSoilSource is not None
        #             else soilSource)
        #         worker_file_label= '%s___%s' % (use_source_label, soil_source_label)
        #         # print('JJ' * 10 +(' %s - %s' % (useSource, soilSource)))
        #         print('JJ' * 10 +(' ==> %s' % (worker_file_label)))
        #     return worker_file_label


        def readAndRemove(filename):
            with open(filename, 'r') as f:
                _ = f.read()
            # FIXME os.remove(filename)
            return _

        # The tool will produce some errors if files
        # do not exist.
        # if not os.path.isfile(useSource):
        #     raise IOError('File %s not found' % useSource)
        # if not os.path.isfile(soilFile):
        #     raise IOError('File %s not found' % soilFile)

        # worker_file_label=getWorkerFileLabel()

        if errWithOut:
            #-- one unique output file for output and errors
            output_filename=Environment.getWorkerFileName(
                basicFileName=basicFileName+'.out',
                workerSpace=workerSpace)
            #
            # try:
            #     os.path.expanduser()
            #     (f, output_filename) = tempfile.mkstemp(suffix='.txt', text=True)
            #     os.close(f)
            # except Exception:
            #     raise IOError('Cannot create temporary file')
            errors_filename = None
            redirection = '>%s 2>&1' % output_filename
            cls.out = None
            cls.err = None
        else:
            # -- two temporary files for output and errors
            # (f, output_filename) = tempfile.mkstemp(suffix='.use', text=True)
            # os.close(f)
            output_filename = Environment.getWorkerFileName(
                basicFileName=basicFileName + '.utc',
                workerSpace=workerSpace)
            # output_filename=Environment.getWorkerFile(name=worker_file_label + '.use')
            # prepare temporary file for errors
            # (f, errors_filename) = tempfile.mkstemp(suffix='.err', text=True)
            # os.close(f)
            # errors_filename=Environment.getWorkerFile(name=worker_file_label + '.err')
            errors_filename = Environment.getWorkerFileName(
                basicFileName=basicFileName + '.err',
                workerSpace=workerSpace)

            redirection = '>%s 2>%s' % (output_filename, errors_filename)
            cls.outAndErr = None

        options=(
              '-extendedTypeSystemChecks:I'
            + '-oclAnyCollectionsChecks:I')
        commandPattern = '%s -nogui -nr %s %s %s '+ redirection
        cls.command = (commandPattern % (
            USE_OCL_COMMAND,
            options,
            useSource,
            soilSource))
        if DEBUG>=3 or Config.realtimeUSE>=1:
            print('USE: '+'.'*80)
            print('USE:    USE EXECUTION %s' % cls.command)
        cls.directory = executionDirectory if executionDirectory is not None \
                     else os.getcwd()
        # cls.directory = executionDirectory if executionDirectory is not None \
        #             else os.path.dirname(os.path.abspath(useSource))
        previousDirectory = os.getcwd()

        # Execute the command
        # log.info('Execute USE OCL in %s: %s', cls.directory, cls.command)
        if DEBUG>=2 or Config.realtimeUSE>=1:
            print('USE:    Execute USE OCL')
            print('USE:        working dir: %s' % cls.directory)
            print('USE:        use file   : %s' % useSource)
            print('USE:        soil file  : %s' % soilSource)
            print('USE:        errWithOut : %s' % errWithOut)
            print('USE:        output     : %s' % output_filename)
            if cls.outAndErr:
                print('USE:        output     : %s' % errors_filename)

        os.chdir(cls.directory)
        cls.commandExitCode = os.system(cls.command)
        os.chdir(previousDirectory)
        if DEBUG>=2 or Config.realtimeUSE>=1:
            print('USE:        exit code  : %s' % cls.commandExitCode)
        if errWithOut:
             if cls.commandExitCode != 0:   #FIXME: was != 0 but  with a bug
                 cls.outAndErr = None
             else:
                 cls.outAndErr = readAndRemove(output_filename)
        else:
            cls.out = readAndRemove(output_filename)
            if DEBUG >= 2 or Config.realtimeUSE >= 1:
                print('USE:        output of %s lines' %
                      len(cls.out.split('\n')))
            # log.debug('----- output -----')
            # log.debug(cls.out)
            # log.debug('----- end of output ------')

            cls.err = readAndRemove(errors_filename)
            if len(cls.err) > 0:
                if DEBUG >= 2 or Config.realtimeUSE >= 1:
                    print('USE:        WITH ERRORS of %s lines:'
                          '(first lines below)' %
                        len(cls.err.split('\n'))   )
                LINE_COUNT = 3
                for err_line in cls.err.split('\n')[:LINE_COUNT]:
                    if err_line != '':
                        if DEBUG >= 2 or Config.realtimeUSE >= 1:
                            print('USE:         ERROR: %s' % err_line)
            else:
                if DEBUG >= 2 or Config.realtimeUSE >= 1:
                    print('USE:        without anything in stderr')

            # log.debug('----- errors -----')
            # log.debug(cls.err)
            # log.debug('----- end of errors ------')
        if DEBUG >= 2 or Config.realtimeUSE >= 1:
            print('USE: ' + '.' * 80)
        return cls.commandExitCode

    @classmethod
    def useVersion(cls):
        """
        Get the version of use by executing it.
        Raise an exception if use cannot be executed.

        Returns (str): The version number.
        """
        use=cls._soilHelper('emptyModel.use')
        soil=cls._soilHelper('quit.soil')
        cls._execute(
            use,
            soil,
            basicFileName='useVersion',
            workerSpace='home')
        first_line = cls.out.split('\n')[0]
        m = re.match( r'(use|USE) version (?P<version>[0-9\.]+),', first_line)
        if m:
            return m.group('version')
        else:
            msg = "Cannot execute USE OCL or get its version. Is this program installed?\n"
            raise EnvironmentError(msg)

    @classmethod
    def withUseOCL(cls):
        """
        Indicates if use is installed and works properly.
        Returns (bool): True if use is installed properly, False otherwise.
        """
        try:
            cls.useVersion()
        except EnvironmentError:
            return False
        else:
            return True

    @classmethod
    def analyzeUSEModel(cls,
                        useFileName,
                        prequelFileName=None,
                        workerSpace=None):
        #type: (Text) -> int
        """
        Submit a ``.use`` model to use and indicates
        return the exit code.

        Args:
            useFileName (Text):
                The path of the ``.use`` file to analyze.

        Returns (int):
            use command exit code.
        """
        if prequelFileName is None:
            prequelFileName=useFileName
        soil=cls._soilHelper('infoModelAndQuit.soil')
        if DEBUG>=2:
            print('USE: '+' analyzeUSEModel '.center(80,'#'))
        cls._execute(
            useFileName,
            soil,
            basicFileName=prequelFileName,
            workerSpace=workerSpace)
        if DEBUG>=2:
            print('USE: '+' END analyzeUSEModel '.center(80,'#'))
        return cls.commandExitCode

    @classmethod
    def executeSoilFileAsTrace(cls,
                               useFile,
                               soilFile,
                               prequelFileName=None,
                               workerSpace=None):
        """
        Standard execution of a .soil file with a .use file.
        The result is saved in a temp .stc file whose name is returned
        """
        if prequelFileName is None:
            prequelFileName=soilFile
        abs_prequel_file=os.path.realpath(prequelFileName)
        abs_use_file=os.path.realpath(useFile)
        abs_soil_file=os.path.realpath(soilFile)
        # worker_file_label=Environment.pathToLabel(abs_soil_file)

        # create the driver file
        driver_sequence = "open '%s' \nquit\n" % abs_soil_file
        # (f, driver_filename) = tempfile.mkstemp(suffix='.soil', text=True)
        # os.close(f)
        driver_filename=Environment.getWorkerFileName(
            basicFileName=\
                replaceExtension(
                    abs_prequel_file,
                    '.driver.soil'),
            workerSpace=workerSpace
            )

        with open(driver_filename, 'w') as f:
            f.write(driver_sequence)

        # execute  use
        cls._execute(
            abs_use_file,
            driver_filename,
            basicFileName=replaceExtension(abs_prequel_file,'.use'),
            errWithOut=True,
            workerSpace=workerSpace)


        # save the result in a temp file
        # (f, trace_filename) = tempfile.mkstemp(suffix='.stc', text=True)
        # os.close(f)
        trace_filename=Environment.getWorkerFileName(
            basicFileName=\
                replaceExtension(
                    abs_prequel_file,
                    '.stc'),
            workerSpace=workerSpace)
        # print('NN'*10, type(cls.outAndErr))
        with open(trace_filename, 'w') as f:
            f.write(cls.outAndErr)
        return trace_filename

    @classmethod
    def executeSoilFileAsSex(cls, useFile, soilFile, prequelFileName=None):
        #type: (Text, Text, Optional[Text]) -> Text
        """
        Execute a .soil file with a .use file and get the result
        as a .sex file, that is, the file with the evaluation result
        embedded. Change outAndErr just like if the engine returned
        the text.

        The implementation is:
        1. first create the trace (.stc) with executeSoilFileAsTrace
        2. merge the soil file and trace file with merge
        If the file contains no soil statements at all the content is
        copied directly to the .sex file with 00001 like marker to
        mimics what happend with the regular process.
        """

        def is_empty_soil(abs_soil_file):
            """
            Indicates if there is at least a useful soil statement
            that is a line starting with ! ou ?.
            Check is not in the list because if there is no ! there
            is nothing to check anyway. Additionaly this is necessary
            since the scn preprocessor generate check for end statement
            so that there is check even in the case of just usecase or
            textual scenario.
            :param abs_soil_file:
            :return:
            """
            lines=readFileLines(
                file=abs_soil_file,
                issueOrigin=None)
            for line in lines:
                if re.match(
                    '^ *(!|\?)',
                    line):
                    return False
            return True

        def empty_soil_to_sex(abs_soil_file, sex_filename):

            lines=readFileLines(
                file=abs_soil_file,
                issueOrigin=None)
            out_lines=[]
            for (no, line) in enumerate(lines):
                out_lines.append('%05i:%s' % (
                    no,
                    line))
            writeFileLines(out_lines, sex_filename)

        def trace_and_merge_to_sex(
                prequel_file_name,
                abs_use_file,
                abs_soil_file,
                sex_filename
        ):
            """
            Create a trace (-> .stc) and then perform a merge (-> .sex)
            """
            if DEBUG>=3:
                print('USE: executeSoilFileAsSex: Soil file: %s'
                      % abs_soil_file)
                displayFileContent(abs_soil_file)
                print('USE: executeSoilFileAsSex: executeSoilFileAsTrace')
            trace_filename = cls.executeSoilFileAsTrace(
                abs_use_file,
                abs_soil_file,
                prequelFileName=prequel_file_name)
            if DEBUG>=3:
                print(
                    'USE: executeSoilFileAsSex: '
                    'TRACE RESULT saved in %s'
                    % trace_filename)
                displayFileContent(trace_filename, prefix='USE:    ')
                print('USE: executeSoilFileAsSex: now merging')
            from modelscripts.tools.use.engine.merger import merge
            merge(
                abs_soil_file,
                trace_filename,
                prequelFileName=prequel_file_name)
            if DEBUG>=3:
                print('USE: executeSoilFileAsSex: '
                    'SEX FILE saved in %s' % sex_filename)
                displayFileContent(sex_filename)
            return sex_filename

        if DEBUG>=2:
            print('USE: '+' executeSoilFileAsSex '.center(80,'#'))
        if prequelFileName is None:
            prequelFileName=soilFile
        abs_use_file=os.path.realpath(useFile)
        abs_soil_file=os.path.realpath(soilFile)
        sex_filename = Environment.getWorkerFileName(
            basicFileName=replaceExtension(prequelFileName, '.sex'))
        if is_empty_soil(abs_soil_file):
            empty_soil_to_sex(
                abs_soil_file=abs_soil_file,
                sex_filename=sex_filename)
        else:
            trace_and_merge_to_sex(
                prequel_file_name=prequelFileName,
                abs_use_file=abs_use_file,
                abs_soil_file=abs_soil_file,
                sex_filename=sex_filename)
        with open(sex_filename, 'rU') as f:
            cls.outAndErr=f.read()
        if DEBUG >= 2:
            print('USE: ' + ' END executeSoilFileAsSex '.center(80, '#'))
        return sex_filename

def displayFileContent(filename, prefix='    ', length=5):
    import io
    with io.open(filename,
                 'rU',
                 encoding='utf8') as f:
        lines = list(
            line.rstrip() for line in f.readlines())

    print(prefix+'%i line(s) in %s :' % (len(lines), filename))
    prefixed_lines=[
        prefix+str(n+1)+' | ' +l
        for (n,l) in enumerate(lines[:length])]
    print('\n'.join(prefixed_lines))
    if len(lines)>length:
        print(prefix+'  | ... %s more lines ...' %(len(lines)-length))

















    # Not sure if this is safe.
    # ------------------------
    # Tests never really worked for batch processing of many file at once
    # We can execute file per file for each soil file.
    # Performance is not really an issue.
    #
    # @classmethod
    # def evaluateSoilFilesWithUSEModel(cls, useFile, stateFiles):
    #
    #     def __generateSoilValidationDriver(stateFilePaths):
    #         """
    #         Create a soil sequence with the necessary statements to drive the
    #         sequence of snapshot validation. That is, it loads and checks each
    #         state one after each other.
    #
    #         The soil driver sequence generated looks like:
    #                 reset
    #                 open file1.soil
    #                 check
    #                 reset
    #                 open file2.soil
    #                 check
    #                 ...
    #                 quit
    #
    #         The output with error messages can be found after the execution
    #         in the variable outAndErr.
    #         :param stateFilePaths: A list of .soil files corresponding
    #         to states.
    #         :type stateFilePaths: [str]
    #         :return: The soil text
    #         :rtype: str
    #         """
    #         if len(stateFiles) == 0:
    #             raise Exception('Error: no state file to evaluate')
    #         lines = reduce(operator.add,
    #                        map(
    #                            lambda file: ['reset', 'open ' + file,
    #                                          'check -d'],
    #                            stateFilePaths))
    #         lines.append('quit')
    #         return '\n'.join(lines)
    #
    #     #-- generate soil driver
    #     if len(stateFiles) == 0:
    #         raise Exception('Error: no state file to evaluate')
    #     driver_sequence = __generateSoilValidationDriver(stateFiles)
    #     (f, driver_filename) = tempfile.mkstemp(suffix='.soil', text=True)
    #     os.close(f)
    #     with open(driver_filename, 'w') as f:
    #         f.write(driver_sequence)
    #
    #     cls.__execute(
    #         useFile,
    #         driver_filename,
    #         errWithOut=True)
    #
    #     return cls.commandExitCode
