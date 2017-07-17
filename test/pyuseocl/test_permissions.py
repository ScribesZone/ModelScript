# coding=utf-8

from nose.plugins.attrib import attr

import logging
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('test.'+__name__)

from test.pyuseocl import (
    TEST_CASES_DIRECTORY,
    BUILD_DIRECTORY,
)

import os
import pyuseocl.use.use.parser
import pyuseocl.umlscripts.usecases
import pyuseocl.metamodel.permissions
import pyuseocl.umlscripts.permissions

# TODO: add this again
# def test_UseOclModel_Simple():
#     check_isValid('Demo.use')



def testGenerator_UseOclModel_full():
    test_dir=os.path.join(
        TEST_CASES_DIRECTORY,'pmm')

    #--- get the class model ----------------------
    use_file_name=os.path.join(test_dir,'a.clm')
    use_file = pyuseocl.use.use.parser.UseSource(
        use_file_name)
    assert(use_file.isValid)
    class_model = use_file.model

    #--- get the class model ----------------------
    usecase_file_name=os.path.join(test_dir,'a.ucm')
    usecase_source = pyuseocl.umlscripts.usecases.UsecasesSource(
        usecase_file_name)
    assert(usecase_source.isValid)
    system = usecase_source.system

    #--- test all .pmm files ----------------------

    for short_name in ['a1']:
        permission_file=os.path.join(test_dir,short_name+'.pmm')
        yield check_isValid, class_model, system, permission_file


def check_isValid(class_model, system, permission_file):

    #--- parser: .soil -> scenario -------------------
    pms = pyuseocl.umlscripts.permissions.PermissionModelSource(
        system=system,
        classModel=class_model,
        filename=permission_file,
    )
    if not pms.isValid:
        pms.printStatus() # TODO: to be implemented
    assert pms.isValid
    print(len(pms.permissionModel.statements))
    permission_set=pms.permissionModel.interpret()
    for p in permission_set.permissions:
        print(p)
