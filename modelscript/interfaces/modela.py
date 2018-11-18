#!/D2/ScribesZone/ModelScript/.venv/bin/python
"""
This script can be called either
- from a shell, with the filename to annotate as a parameter
- from gedit external tool interface, with the file name as env variables.
It first remove the annotations from the file given, then process
the file.
"""
from __future__ import print_function
import os
import sys
import traceback

def setup():
    """
    Add the modelscript home to python PATH.
    """
    #------ add modescripts to the path -------------------
    modelscribes_home=os.path.realpath(
        os.path.join(
            os.path.dirname(__file__),
            '..', '..'))
    if modelscribes_home not in sys.path:
        sys.path.insert(0,modelscribes_home)
    #------------------------------------------------------

setup()

# This could be useful, not sure
        # # use sys.prefix to check which python is used
        # import os
        # import sys
        # thisDir = os.path.dirname(os.path.realpath(__file__))
        # sys.path.append(os.path.join(thisDir,'..'))
        # virtual_env=os.path.expanduser('~/DEV/ScribesVirtualEnvs/WebAppScribes')
        # activate_file=os.path.join(
        #     virtual_env, "bin/activate_this.py")
        # execfile(activate_file, dict(__file__=activate_file))

class Environment(object):

    def __init__(self):
        self.who=None
        # Filled by getFileName

    def _getGEditFileName(self):
        """
        Get the GEdit filename provided by GEdit.
        Raise an exception if this code is not executed from GEdit
        """
        name=(os.environ['GEDIT_CURRENT_DOCUMENT_NAME'])
        dir=(os.environ['GEDIT_CURRENT_DOCUMENT_DIR'])
        return os.path.join(dir, name)

    def _getParameterFileName(self):
        """
        Return the filename provided as the first shell parameter.
        It there is no such parameter then raise an exception.
        :return:
        """
        if len(sys.argv)==2:
            return sys.argv[1]
        else:
            raise ValueError('No argument') #raise:TODO:2

    def getFileName(self):
        try:
            self.who='gedit'
            return self._getGEditFileName()
        except Exception: #except:OK
            try:
                self.who='shell'
                return self._getParameterFileName()
            except ValueError: #except:OK
                raise ValueError( #raise:TODO:2
                    'No file given as parameter')

from modelscript.base.annotations import (
    Annotations
)
env=Environment()
filename=env.getFileName()

# remove annotations from document (if any)
filtered_filename=Annotations.filterFile(filename)
file_to_parse=(
    filtered_filename if filtered_filename is not None
    else  filename)

# parse the file without any annotation
from modelscript.megamodels import Megamodel
try:
    source = Megamodel.loadFile(filename)
except Exception as e:
    traceback.print_exc(e)
    print(unicode(e))

# annotated the source
#TODO:2 Find the class AnnotatedSourcePrinter
#   This class no longer exist and cannot be found easily in
#   old version. Check where this features has gone.

AnnotatedSourcePrinter(source).display(
    removeLastEOL=False if env.who == 'gedit' else True
)

sys.stderr.write(source.fullIssueBox.str())

