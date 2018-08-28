import os
import sys

def setup():
    """
    Add the modelscripts home to python PATH.
    """
    #------ add modescripts to the path -------------------
    modelscripts_home=os.path.realpath(
        os.path.join(
            os.path.dirname(__file__),
            '..','..','..'))
    if modelscripts_home not in sys.path:
        sys.path.insert(0,modelscripts_home)
    #------------------------------------------------------

setup()

from modelscripts.interfaces.modelc.build import build

build(sys.argv)

