# coding=utf-8

from nose.plugins.attrib import attr

import logging
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('test.'+__name__)

from test.modelscripts import (
    TEST_CASES_DIRECTORY,
    BUILD_DIRECTORY,
)

import os
import modelscribes.use.use.parser
import modelscribes.scripts.usecases.parser
import modelscribes.metamodels.permissions
import modelscribes.scripts.permissions.parser

# TODO: add this again
# def test_UseOclModel_Simple():
#     check_isValid('Demo.use')



def testGenerator_UseOclModel_full():
    test_dir=os.path.join(
        TEST_CASES_DIRECTORY,'pmm')

    #--- get the class model ----------------------
    use_file_name=os.path.join(test_dir,'a.clm')
    use_file = modelscribes.use.use.parser.UseSource(
        use_file_name)
    assert(use_file.isValid)
    class_model = use_file.classModel

    #--- get the usecase model ----------------------
    usecase_file_name=os.path.join(test_dir,'a.ucm')
    usecase_source = modelscribes.scripts.usecases.parser.UsecaseModelSource(
        usecase_file_name)
    assert(usecase_source.isValid)
    usecase_model = usecase_source.usecaseModel

    #--- test all .pmm files ----------------------

    for short_name in ['a1']:
        permission_file=os.path.join(test_dir,short_name+'.pmm')
        yield check_isValid, class_model, usecase_model, permission_file


def check_isValid(class_model, usecaseModel, permission_file):

    #--- parser: .soil -> scenario -------------------
    pmsource = modelscribes.scripts.permissions.parser.PermissionModelSource(permissionFileName=permission_file,
                                                                             usecaseModel=usecaseModel,
                                                                             classModel=class_model)
    if not pmsource.isValid:
        pmsource.printStatus() # TODO: to be implemented
    assert pmsource.isValid
    pmmodel=pmsource.permissionModel
    permission_set=pmmodel.permissionSet
    # print('***********',permission_set)
    # print('%i rules -> %i permissions' % (
    #     len(pmmodel.rules),
    #     len(permission_set.permissions)))
    for p in permission_set.permissions:
        print(p)
