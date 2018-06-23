# coding=utf-8

import logging
import os

import modelscripts.use.engine.merger
from test.modelscripts import (
    getBuildDir,
    getTestDir,
)

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('test.'+__name__)


SEX_DIR=getBuildDir(os.path.join('gen','sex'))


# TODO:add this again
# def test_UseOclModel_Simple():
#     check_isValid('Demo.use')



def testGenerator_UseOclModel_full():
    test_dir=getTestDir('sex')

    for test in ['Demo6','Demo666.5']:

        soilfile=os.path.join(test_dir,'%s.soil'%test)
        tracefile=os.path.join(test_dir,'%s.stc'%test)
        sexfile=os.path.join(
            SEX_DIR,
            '%s.sex'%test
        )
        yield check_isValid, soilfile, tracefile, sexfile



def check_isValid(soilfile, tracefile, sexfile):
    modelscripts.use.engine.merger.merge(soilfile, tracefile, sexfile)

