# coding=utf-8

from test.pyuseocl import getUseFile
import pyuseocl.use.use.printer
import pyuseocl.use.use.parser

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
    model = pyuseocl.use.use.parser.UseFile(useFile).model
    printer = pyuseocl.use.use.printer.UseOCLPrinter(model)
    print printer.do()
