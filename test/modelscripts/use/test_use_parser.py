# coding=utf-8

from nose.plugins.attrib import attr

import logging
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('test.'+__name__)

from test.modelscripts import getUseFile

import os

# from modelscribes.base.printers import (
#     AnnotatedSourcePrinter
# )
from modelscribes.use.use.parser import (
    UseModelSource
)
# from modelscribes.use.use.printer import (
#     UseSourcePrinter
# )

from test.modelscripts import (
    getTestFile,
    getTestFiles,
    getTestDir
)

# TODO: add this again
# def test_UseOclModel_Simple():
#     check_isValid('Demo.use')


@attr('slow')
def testGenerator_selectedModels():
    test_file_names1 = [
        'civstatAnonymous.use',
        'CyberResidencesOCL.use',
        'AssociationClass.use',
        'Demo.use',
        'Employee.use',
        'NestedOperationCalls.use',
        'Graph.use',
        'civstat.use',
        'tollcoll.use',
        'actionsemantics.use',
        'OCL2MM.use',
        'UML13All.use',
        'UML13Core.use',
        'CarRental2.use',
        'Empty.use',
        'Grammar.use',
        'derived.use',
        'Job.use',
        'Lists.use',
        'Math.use',
        'MultipleInheritance.use',
        'MultipleInheritance_unrelated.use',
        'Person.use',
        'Polygon.use',
        'Project.use',
        'RecursiveOperations.use',
        'ReflexiveAssociation.use',
        'Student.use',
        'simpleSubset.use',
        'simpleSubsetUnion.use',
        'twoSubsets.use',
        'Sudoku.use',
        'Test1.use',
        'Tree.use',
        'CarRental.use',
        'RoyalAndLoyal.use',
        'OCLmetamodel.use',
        'EmployeeExtended.use',
        'bart.use',
    ]
    test_files1=[
        os.path.join('use',f) for f in test_file_names1]

    for test_file in test_files1:
        yield check_isValid, test_file

@attr('slow')
def testGenerator_use4Dir():
    relfiles=getTestFiles(
        'use/use4/test',
        relative=True,
        extension=['.use', '.clm'])
    for relfile in relfiles:
        yield check_isValid, relfile

def check_isValid(reltestfile):
    use_source = UseModelSource(getTestFile(reltestfile))
    # AnnotatedSourcePrinter(use_source).display()
    print('====='*20,'printer disabled')
    assert use_source.isValid

