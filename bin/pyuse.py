# coding=utf-8
import sys
import os
thisDir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(thisDir,'..'))

import pyuseocl.analyzer
import pyuseocl.tester
import pyuseocl.useengine

if len(sys.argv)==1:
    version = pyuseocl.useengine.USEEngine.useVersion()
    print "pyuse - based on use version %s - University of Bremen" % version
else:
    usefile = sys.argv[1]
    soilfiles = sys.argv[2:]

    model = pyuseocl.analyzer.UseOCLModel(usefile)
    print model
    if len(soilfiles) >= 1:
        r = pyuseocl.tester.UseEvaluationAndAssertionResults(model, soilfiles)
        print r