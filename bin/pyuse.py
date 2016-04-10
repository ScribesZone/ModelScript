# coding=utf-8
import sys
import os
import logging
thisDir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(thisDir,'..'))

import pyuseocl.analyzer
import pyuseocl.tester
import pyuseocl.useengine

logging.basicConfig(level=logging.ERROR)

if len(sys.argv)==1:
    version = pyuseocl.useengine.USEEngine.useVersion()
    print "pyuse - based on use version %s - University of Bremen" % version
else:
    usefile = sys.argv[1]
    soilfiles = sys.argv[2:]

    if not os.path.isfile(usefile):
        print usefile + " not found"
        sys.exit(2)
    else:
        model_file = pyuseocl.analyzer.UseOCLModelFile(usefile)
        model_file.printStatus()
        if not model_file.isValid:
            print 'ERROR: model file is invalid'
            sys.exit(1)

        if len(soilfiles) >= 1:
            r = pyuseocl.tester.UseEvaluationAndAssertionResults(model_file, soilfiles)
            print r
            r.showAssertionEvaluationByStateFile()