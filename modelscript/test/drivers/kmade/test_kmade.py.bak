# coding=utf-8
from __future__ import print_function

from modelscript.scripts.tasks.printer import (
    TaskModelPrinter
)
from modelscript.tools.kmade.engine import (
    KmadeReader
)
from modelscript.test.framework import getTestFile, getTestFiles


def testGenerator_Assertions():
    test_files=getTestFiles(
        relativeDirectory='kxml',
        relative=True,
        extension=['.kxml'])
    for test_file in test_files:
        yield (
            checkKmadeFile,
            test_file)


def checkKmadeFile(test_file):
    print('CHECKING %s' % test_file)
    print('FILE %s' % getTestFile(test_file))
    abs_test_file=getTestFile(test_file)
    reader = KmadeReader(abs_test_file)
    model = reader.taskModel()
    print(TaskModelPrinter(model).doModelContent())
#
# def checkValidIssues(reltestfile):
#     file=' %s %s ' % (
#         metamodel.label,
#         os.path.basename(reltestfile)
#     )
#     print('\nTST:'+'=='*10+' testing '+file+'='*35+'\n' )
#     source = metamodel.sourceClass(getTestFile(reltestfile))
#
#     print('\n'+'TST:'+'==' * 10 + ' printing source '+file+'='*35+'\n')
#     metamodel.sourcePrinterClass(source).display()
#
#     print('\n'+'TST:'+'==' *10 + ' printing model '+'='*40+'\n')
#     metamodel.modelPrinterClass(source.model).display()
#
#     if expectedIssues is None:
#         expectedIssues={F: 0, E: 0, W: 0, I: 0, H: 0}
#
#     assertIssueBox(source.fullIssueBox, expectedIssues)
#     assertMetrics(source.fullMetrics, expectedMetrics)
#
#     print('\n'+'TST:'+'==' *10 + ' printing model '+'='*40+'\n')
#     print(source.fullMetrics)
#     print('TST:'+'=='*10+' tested '+file+'='*35+'\n' )
#
#
#
#
#
#
# # def testGenerator_Issues():
# #     res = checkAllAssertionsForDirectory(
# #         'uss',
# #         ['.uss'],
# #         EXPECTED_ISSUES)
# #     for (file , ex) in res:
# #         yield (checkValidIssues, file, usecases.METAMODEL, ex)
#
# # def testFinalMegamodel():
#     MegamodelPrinter().display()