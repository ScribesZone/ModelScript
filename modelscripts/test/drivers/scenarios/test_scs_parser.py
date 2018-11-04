# coding=utf-8
from __future__ import print_function
from modelscripts.test.framework.assertions import (
    simpleTestDeneratorAssertions)
from modelscripts.scripts.megamodels.printer.megamodels import \
    MegamodelPrinter

from modelscripts.metamodels.scenarios import METAMODEL

def testGenerator_Assertions():
    for (v,f,m,eim, emm) in \
            simpleTestDeneratorAssertions(METAMODEL):
        yield (v,f,m,eim, emm)

def testFinalMegamodel():
    MegamodelPrinter().display()