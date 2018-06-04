# coding=utf-8

import logging
import os

from nose.plugins.attrib import attr

import modelscripts.diagrams.plantuml.engine
import modelscripts.scripts.classes.plantuml
import modelscripts.use.use.parser
from modelscripts.base.modelprinters import (
    ModelSourcePrinter
)
from test.modelscripts import (
    TEST_CASES_DIRECTORY,
    getTestDir,
    getBuildDir,
)

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('test.'+__name__)

BUILD_CLASSES_DIR=getBuildDir(os.path.join('gen/diagrams/classes'))

# TODO: add this again
# def test_UseOclModel_Simple():
#     check_isValid('Demo.use')


@attr('slow')
def testGenerator_UseOclModel_full():
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
        # 3-ary assoc 'CarRental2.use',
        'Empty.use',
        'Grammar.use',
        'derived.use',
        'Job.use',
        'Lists.use',
        'Math.use',
        'MultipleInheritance.use',
        'MultipleInheritance_unrelated.use',
        # 3-ary assoc 'Person.use',
        'Polygon.use',
        'Project.use',
        'RecursiveOperations.use',
        'ReflexiveAssociation.use',
        'Student.use',
        'simpleSubset.use',
        # 'simpleSubsetUnion.use',
        # 'twoSubsets.use',
        # 'Sudoku.use',
        # 'Test1.use',
        # 'Tree.use',
        # 'CarRental.use',
        # 'RoyalAndLoyal.use',
        # 'OCLmetamodel.use',
        # 'EmployeeExtended.use',
        # 'bart.use',
    ]
    test_files1=[os.path.join('use',f) for f in test_file_names1]
    use4subdir = os.path.join('use','use4','test')
    test_dir_2 = getTestDir(use4subdir)
    # print test_dir_2
    test_files2 = [use4subdir + os.sep + f
                   for f in os.listdir(test_dir_2) if f.endswith('.use')]
    test_files2=[]
    # #print test_files2
    all_test_files = test_files1+test_files2

    plantUMLengine = modelscripts.diagrams.plantuml.engine.PlantUMLEngine()
    for test_file in all_test_files:
        yield check_isValid, test_file, plantUMLengine


def check_isValid(testFile, plantUMLengine):
    use_file = modelscripts.use.use.parser.UseModelSource(
        TEST_CASES_DIRECTORY + os.sep + testFile)
    puml_file_path = os.path.join(
        BUILD_CLASSES_DIR,
        os.path.splitext(os.path.basename(testFile))[0]+'.puml'
    )
    ModelSourcePrinter(use_file).display()
    assert use_file.isValid
    print('\n'*2+'='*80)
    print('Generating '+puml_file_path)
    out = modelscripts.scripts.classes.plantuml.ClassDiagramPrinter(use_file.classModel)
    print(out.do(outputFile=puml_file_path))
    print('\n'*2+'.'*80)
    plantUMLengine.generate(puml_file_path)

    # if useModel.isValid:
    #     print useModel.model
    # assert useModel.isValid
        #else:
    #    print >> sys.stderr, 'Failed to create canonical form'
    #    for error in use.errors:
    #        print >> sys.stderr, error
    #        # UseOCLConverter.convertCanOCLInvariants(use.canonicalLines)
