# coding=utf-8

from modelscript.test.framework.assertions import (
    simpleTestDeneratorAssertions)
from modelscript.scripts.megamodels.printer.megamodels import \
    MegamodelPrinter

from modelscript.metamodels.participants import METAMODEL

def testGenerator_Assertions():
    for (v,f,m,eim, emm) in \
            simpleTestDeneratorAssertions(METAMODEL):
        yield (v,f,m,eim, emm)

def testFinalMegamodel():
    MegamodelPrinter().display()
