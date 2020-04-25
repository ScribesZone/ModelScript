# coding=utf-8
"""Comparator of the actual output with the reference one."""

from typing import Optional, List
from typing_extensions import Literal
import os
import codecs

from modelscript.test.framework import getTestFile
from modelscript.base.files import ensureDir

DEBUG = 2

def ManageAndCompareOutput(reltestfile, actualOutput):
    # reltestfile looks like "des/de-ko01.des"

    DIR_KIND = Literal['generated', 'verified', 'actual']

    def _output_dir(kind: DIR_KIND):
        """Something like des/output-generated """
        return getTestFile(
            os.path.join(
                os.path.dirname(reltestfile),
                'output-%s' % kind),
            checkExist=False)

    def _output_file(kind: DIR_KIND):
        """Something like des/output-generated/de-ko01.des """
        return os.path.join(
            _output_dir(kind),
            os.path.basename(reltestfile))

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

    def _compare(actual: str, kind: DIR_KIND) -> Optional[bool]:
        """Compares the actual output with the reference output.
        Display the error if any, but do not raise the exception.
        Returns None if there is no comparison to be made.
        Otherwise returns the True if the actual output and the
        generated output are the some.
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

