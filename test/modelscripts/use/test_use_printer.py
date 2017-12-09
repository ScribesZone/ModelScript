# coding=utf-8

from test.modelscripts import getUseFile
# from  modelscribes.use.use.printer import (
#     UseModelPrinter
# )
from modelscribes.use.use.parser import (
    UseModelSource
)

def testGenerator_UseOCLPrinter():
    test_cases = [
        {'use': 'Demo.use'},
        {'use': 'AssociationClass.use'},
        {'use': 'CarRental.use'},
        {'use': 'Sudoku.use'},
    ]
    for test_case in test_cases:
        test_name = test_case['use']
        check_UseOCLPrinter.description = test_name
        yield check_UseOCLPrinter, test_case


def check_UseOCLPrinter(case):
    useFile = getUseFile(case['use'])
    model = UseModelSource(useFile).classModel
    print('====='*20,'printer disabled')
    assert model is not None

