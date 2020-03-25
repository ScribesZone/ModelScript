import os
import sys
import traceback

def setup():
    """
    Add the modelscript home to python PATH.
    """
    #------ add modescripts to the path -------------------
    modelscript_home=os.path.realpath(
        os.path.join(
            os.path.dirname(__file__),
            '..','..','..'))
    if modelscript_home not in sys.path:
        sys.path.insert(0,modelscript_home)
    #------------------------------------------------------

setup()

from modelscript.interfaces.modelc.build import BuildContext
from modelscript.libs.termcolor import cprint

try:
    bc=BuildContext(sys.argv[1:])
    bc.display()
except Exception as ex:
    title = ' SYSTEM ERROR in %s '
    cprint(title.center(80, '!'), 'red')
    cprint(unicode(ex), 'red')
    traceback.print_exc(ex)
    cprint('!' * 80, 'red')

