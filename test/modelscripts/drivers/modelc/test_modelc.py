# coding=utf-8
import os

from modelscripts.interfaces.modelc.build import (
    build)

from test.modelscripts.framework import TEST_CASES_DIRECTORY

def f(lang, file):
    return os.path.join(
        TEST_CASES_DIRECTORY, lang, file)

def testModelc():
    build([
        'a'])
    print f('uss','us-actor02.uss')
    build([
        f('uss','us-actor02.uss'),
        '-i'])
