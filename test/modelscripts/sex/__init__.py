# coding=utf-8
import os
from test.modelscripts import (
    getTestFile,
)

from modelscripts.scripts.usecases.parser import UsecaseModelSource
from modelscripts.use.use.parser import UseModelSource
from modelscripts.scripts.permissions.parser import (
    PermissionModelSource
)

def _getModelsForScenario(soilDir, fuse, fusm=None, fpem=None):
    usefilename = getTestFile(os.path.join(soilDir, fuse))
    uf=UseModelSource(usefilename)
    assert(uf.isValid)
    clm=uf.classModel

    if fusm is None:
        usm=None
    else:
        usmfilename=getTestFile(os.path.join(soilDir, fusm))
        ucs=UsecaseModelSource(usmfilename)
        assert(ucs.isValid)
        usm=ucs.usecaseModel
        assert(usm is not None)

    if fpem is None:
        pem=None
    else:
        assert(usm is not None)
        pemfilename=os.path.join(os.path.join(soilDir, fpem))
        if os.path.isfile(pemfilename):
            pes=PermissionModelSource(
                permissionFileName=pemfilename)
            assert(pes.isValid)
            pem=pes.permissionModel
            assert(pem is not None)
        else:
            pem=None

    return (clm, usm, pem)