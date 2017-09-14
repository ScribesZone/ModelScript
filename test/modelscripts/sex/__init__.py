# coding=utf-8
import os
from test.modelscripts import (
    getTestFile,
)

from modelscribes.scripts.usecases.parser import UsecaseModelSource
from modelscribes.use.use.parser import UseSource
from modelscribes.scripts.permissions.parser import (
    PermissionModelSource
)

def _getModelsForScenario(soilDir, fuse, fucm=None, fpmm=None):
    usefilename = getTestFile(os.path.join(soilDir, fuse))
    uf=UseSource(usefilename)
    assert(uf.isValid)
    clm=uf.classModel

    if fucm is None:
        ucm=None
    else:
        ucmfilename=getTestFile(os.path.join(soilDir, fucm))
        ucs=UsecaseModelSource(ucmfilename)
        assert(ucs.isValid)
        ucm=ucs.usecaseModel
        assert(ucm is not None)

    if fpmm is None:
        pmm=None
    else:
        assert(ucm is not None)
        pmmfilename=os.path.join(os.path.join(soilDir, fpmm))
        if os.path.isfile(pmmfilename):
            pms=PermissionModelSource(
                permissionFileName=pmmfilename,
                usecaseModel=ucm,
                classModel=clm)
            assert(pms.isValid)
            pmm=pms.permissionModel
            assert(pmm is not None)
        else:
            pmm=None

    return (clm, ucm, pmm)