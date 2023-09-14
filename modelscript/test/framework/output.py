# coding=utf-8
"""Comparator of the actual output with the reference one.
The functions in this file is used by the assertions module."""

from typing import Optional, List
from typing_extensions import Literal
import os
import codecs
import shutil

from modelscript.test.framework import (
    getTestFile,
    getAbolutePath)
from modelscript.base.files import ensureDir

__all__ = (
    'manageAndAssertOutput'
)
DEBUG = 0

def manageAndAssertOutput(
        reltestfile: str,
        stream: str,
        actualOutput: str) -> None:
    """Compare the given "output" to existing "output" and raise an
    assertion error if the "output" has changed. This comparison is
    performed for a given "stream", the most common being the "output".
    The notion of "stream" is in fact just a string to differentiate
    in which directories the content used for the comparison is saved.
    This makes it possible to compare not only the regular output
    but also other kind of textual output. In the description below
    examples are taken assuming that we consider output comparison.

    The following directories are involved :

    *   cmp-<stream>-actual/ (for instance cmp-output-actual).
        This content of this directory is update at each execution.
        This directory contains the last "output" for the stream
        <stream>, the one given as parameter. Having this "output"
        available is useful for file comparaison using an diff tool
        for instance.

    *   cmp-<stream>-generated/ (for instance cmp-output-generated).
        The content of this directory is updated
        only if the file is not existing. This directory serves
        at a generated reference, if the verified "output" is not
        available. Using the generated "output" is useful to check
        if the actual "output" has changed since the last update of
        the generated "output".

    *   cmp-<stream>-verified/ (for instance cmp-output-verified).
        By contrast to the other directories the content of this
        directory is updated by hand. If a file
        is present in this directory in takes precedence over
        the generated one. In other words the comparison is made
        with the verified output, if any, or with the generated
        output.

    DISABLING COMPARAISONS. To disable comparison a directory
    called cmp-no must be created. In this case no comparison are
    peformed and the directory cmp-<stream>-actual/ and
    cmp-<stream>-generated/ and deleted. The directory "verified"
    is never deleted.


    Args:
        reltestfile: The name of the file being tested. This name
            is relative to the testcases directory.
            It could be something like "des/de-ko01.des".
        actualOutput: The output to be compared.

    """
    # reltestfile looks like

    DIR_KIND = Literal['generated', 'verified', 'actual']

    def _output_dir(kind: DIR_KIND):
        """Something like /D/joe/ ... des/cmp-output-generated """
        return getTestFile(
            os.path.join(
                os.path.dirname(reltestfile),
                'cmp-%s-%s' % (stream, kind)),
            checkExist=False)

    def _output_file(kind: DIR_KIND):
        """Something like des/cmp-output-generated/de-ko01.des """
        return os.path.join(
            _output_dir(kind),
            os.path.basename(reltestfile))

    def _comparisons_enabled():
        # disabled if "cmp-no'
        d = getAbolutePath(
                os.path.join(
                    os.path.dirname(reltestfile),
                   'cmp-no'))
        has_no_cmp_dir = os.path.isdir(d)
        return not has_no_cmp_dir


    # ---- generation helpers -------------------

    def _must_generate_file():
        return not os.path.isfile(_output_file('generated'))

    def _create_output_file(kind: DIR_KIND):
        """Save the actual output in the "actual" or "generated"""
        ensureDir(_output_dir(kind))
        output_file = _output_file(kind=kind)
        with codecs.open(output_file, "w", "utf-8") as f:
            f.write(actualOutput)

    # ---- comparison helpers --------------------

    def _reference_kind() -> Optional[DIR_KIND]:
        """Indicate what should be the reference for the comparison.
        Could be None, verified or generated. """
        kinds: List[DIR_KIND] = ['verified', 'generated']
        for kind in kinds:
            if os.path.isfile(_output_file(kind)):
                return kind
        else:
            return None

    def _print_message(msg: str) -> None:
        print('<>'*10, msg)

    def _clean_tmp_directories():
        for kind in ['actual', 'generated']:
            d = _output_dir(kind)
            if os.path.isdir(d):
                shutil.rmtree(d)

    def _compare(actual: str, kind: DIR_KIND) -> Optional[bool]:
        """Compares the actual output with the reference output.
        Display the error if any, but do not raise the exception.
        Returns None if there is no comparison to be made.
        Otherwise returns the True if the actual output and the
        generated output are the some.
        If comparison is enabled then remove the directories
        'actual' and 'generated'.
        """
        if kind is None:
            return None
        # lines of the actual output
        actual_lines = actual.splitlines()

        if DEBUG > 1:
            print('OU'*10, 'reference is "%s"' % kind)
        # get the lines from the reference content
        with open(_output_file(kind), 'r') as content_file:
            reference_content = content_file.read()
        reference_lines = reference_content.splitlines()

        # check first nb of lines
        if len(actual_lines) != len(reference_lines):
            _print_message(
                'Actual output is different from %s output.' % kind)
            _print_message(
                'Number of lines does\'t match. actual output: %i, %s output: %i'%
                (len(actual_lines), kind, len(reference_lines)))
            return False
        else:
            if DEBUG:
                print('OU'*10, 'same nb of lines: %i' % len(actual_lines))
            # check lines by lines
            same = True
            for i in range(0, len(actual_lines)):
                al = actual_lines[i]
                rl = reference_lines[i]
                if al != rl:
                    if same:
                        _print_message(
                            'Actual output is different from %s output.'
                            % kind)
                    _print_message(
                        '---- Line %i differs ----------------------' % i)
                    _print_message('ACTUAL:      %s' % al)
                    _print_message('REFERENCE:   %s' % rl)
                    same = False
            return same

    if not _comparisons_enabled():
        _clean_tmp_directories()
        return

    # ---- save the actual output -----------------------------------------
    _create_output_file('actual')

    # ---- generate the generated output if necessary ---------------------
    if _must_generate_file():
        _create_output_file('generated')

    # ---- check which is the comparison element --------------------------
    reference = _reference_kind()
    if reference is not None:
        same = _compare(actualOutput, reference)
        if same is not None:
            assert same, \
               'Output comparison failed for %s.' \
               ' See message above.' % reltestfile

