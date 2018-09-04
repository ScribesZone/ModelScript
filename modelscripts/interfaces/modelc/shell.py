import os
import sys
import traceback

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

from modelscripts.interfaces.modelc.build import BuildContext
from modelscripts.libs.termcolor import cprint

try:
    bc=BuildContext(sys.argv[1:])
    bc.display()
except Exception as ex:
    title = ' SYSTEM ERROR in %s '
    cprint(title.center(80, '!'), 'red')
    cprint(str(ex), 'red')
    traceback.print_exc(ex)
    cprint('!' * 80, 'red')

