# coding=utf-8

from test.modelscripts import getUseFile
import modelscripts.use.use.printer
import modelscripts.use.use.parser

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
    model = modelscripts.use.use.parser.UseSource(useFile).classModel
    printer = modelscripts.use.use.printer.UsePrinter(model)
    print(printer.do())
