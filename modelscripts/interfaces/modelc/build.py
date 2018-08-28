# coding=utf-8
import argparse
import os
import sys
import traceback
from typing import List, Text

# While the virtual env is set by the shell script it is
# still necessary to add the modelscript package to python path.



# initialize the megamodel with metamodels and scripts

from modelscripts.libs.termcolor import cprint
from modelscripts.base.modelprinters import ModelPrinterConfig
from modelscripts.megamodels import Megamodel
from modelscripts.interfaces.modelc.options import getOptions

#-------------- Command Line Interface -----------------------------




def processSourceFile(filename, manySourceFiles, options):  #TODO:0 rename to optios
    """
    Parse a file and display directly the results.
    If manySourceFiles the output is enclosed with
    proper markers
    """
    basename=os.path.basename(filename)
    try:
        source = Megamodel.loadFile(filename)
        # source could be None here, if some FatalError detected
    except Exception as e: #except:OK
        title=' INTERNAL ERROR in %s ' %  basename
        cprint(title.center(80, '#'), 'red')
        cprint(str(e),'red')
        traceback.print_exc(e)
        cprint('#'*80, 'red')
        return str(e)
    else:
        if manySourceFiles:
            title = ' %s ' % filename
            cprint(title.center(80, '#'), 'blue')
        if source is None:
            print('TODO:2 XXX An issue has to be printed')
        else:
            #  TODO:4 check if creating a ModelPrinterConfig is better
            printer_config = ModelPrinterConfig(
                #  for models
                styled=not options.bw,
                verbose=options.verbose,
                quiet=options.quiet,
                title=basename,
                issuesMode=options.issues,
                contentMode=options.listing,
                summaryMode=options.summary,
                # styled=True,
                # width=120,
                # baseIndent=0,
                # displayLineNos=True,
                # lineNoPadding=' ',
                # verbose=0,
                # quiet=False,
                # # ------------------------
                # title=None,
                # issuesMode='top',
                # # ------------------------
                # contentMode='self',  # self|source|model|no
                # summaryMode='top',  # top | down | no
            )
            Megamodel.displaySource(
                source=source,
                config=printer_config)
        if manySourceFiles:
            title=' END %s ' % filename
            cprint(title.center(80, '#'), 'blue')


def build(args):
    """
    produce the result of the compilation for a given list of arguments.
    Typically this list is filled from sys.args if this function is
    called from a shell.
    """
    options=getOptions(args)
    try:
        manySourceFiles=len(options.sources)>=2
        for filename in options.sources:
            processSourceFile(filename, manySourceFiles, options)
        if Megamodel.model.hasIssues:
            cprint(' Global issues '.center(80, '#'), 'blue')
            print(Megamodel.model.issues)
            cprint('#'*80, 'blue')

    except Exception as e:
        traceback.print_exc(e)
        cprint(str(e), 'red')


