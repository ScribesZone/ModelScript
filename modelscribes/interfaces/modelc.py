# coding=utf-8
import sys
import os
import argparse
import traceback

def setup():
    #------ add modescribes to the path -------------------
    modelscribes_home=os.path.realpath(
        os.path.join(
            os.path.dirname(__file__),
            '..','..'))
    sys.path.insert(0,modelscribes_home)
    #------------------------------------------------------

setup()
from typing import List, Text
import modelscribes

from modelscribes.base.files import (
    extension,
    replaceExtension
)
from modelscribes.interfaces.environment import Environment
from modelscribes.locallibs.termcolor import cprint
from modelscribes.scripts.base.printers import ModelPrinterConfig
from modelscribes.megamodels.megamodels import Megamodel
from modelscribes.config import Config
from modelscribes.use.engine import (
    USEEngine
)
from modelscribes.interfaces.environment import Environment

OPTIONS=[
    ('Dpre','preprocessorPrint'),
    ('Dimp','realtimeImportPrint'),
    ('Diss','realtimeIssuePrint'),
    ('Duse','realtimeUSE'),
]

def getArguments():
    parser = argparse.ArgumentParser(
        prog='modelc',
        description='Compile the given sources.')
    for (parameter,_) in OPTIONS:
        parser.add_argument(
            '--'+parameter,
            dest=parameter,
            const=1,
            # default=0,
            type=int,
            nargs='?')
    parser.add_argument(
        '-bw',
        dest='bw',
        action='store_true',
        default=False
    )
    parser.add_argument(
        '-dg',
        dest='dg',
        action='store_true',
        default=False
    )
    parser.add_argument(
        '--verbose', '-v',
        dest='verbose',
        action='store_true',
        default=False
    )
    parser.add_argument(
        '--quiet', '-q',
        dest='quiet',
        action='store_true',
        default=False
    )
    parser.add_argument(
        '-i', '--issues',
        dest='issues',
        const='top',
        default='inline',
        choices=['top','inline','bottom'],
        type=str,
        nargs='?'
    )
    parser.add_argument(
        '--list', '-l',
        dest='listing',
        const='source',
        default='no',
        choices=['no', 'source', 'model'],
        type=str,
        nargs='?'
    )
    parser.add_argument(
        '--summary', '-s',
        dest='summary',
        const='bottom',
        default='no',
        choices=['no', 'top', 'bottom'],
        type = str,
        nargs = '?'
    )
    parser.add_argument(
        'sources',
        metavar='source',
        nargs='*',
        help='A source file for a model.')
    parser.add_argument(
        '-use',
        dest='use',
        const='version',
        default=None,
        choices=['version', 'c', 'cli', 'gui'],
        type = str,
        nargs = '?'
    )
    args = parser.parse_args()
    return args

def updateConfig(args):
    for (parameter, configOption) in OPTIONS:
        val = getattr(args, parameter)
        if val is not None:
            # update config only if value is specified
            print('%s(%s)=%s' % (configOption, parameter, val))
            setattr(Config, configOption, val)

def processUseCommand(command, sources):

    def _useInterface(interface, files):
        terminal_cmd = 'gnome-terminal -e "%s"'
        if interface=='gui':
            use_cmd='use -nr %s' % ' '.join(files)
            full_cmd=terminal_cmd % use_cmd
        elif interface=='cli':
            use_cmd='use -nogui -nr %s' % ' '.join(files)
            full_cmd=terminal_cmd % use_cmd
        elif interface=='c':
            if len(files)==0:
                full_cmd='use -V'
            elif len(files)==1: # means use
                full_cmd='use -c %s' % files[0]
            elif len(files)==2: # means use soil
                full_cmd='use -qv %s %s' % (files[0], files[1])
            else:
                assert False
        else:
            raise NotImplementedError('"%s" invalid USE interface')
        print('mdc: %s' % full_cmd)
        os.system(full_cmd)


    def _getSourcesForUSE(sources):
        #type: (List[Text]) -> List[Text]
        def _toUse(files, originalExtensions, useExtension):
            return [Environment.getWorkerFileName(
                        replaceExtension(f, useExtension))
                    for f in sources
                    if extension(f) in originalExtensions]
        uses=_toUse(sources, ['.cls'], '.use')
        soils=_toUse(sources, ['.obs','.scs'], '.soil')

        (nu,ns)=(len(uses), len(soils))
        if len(sources)>len(uses)+len(soils):
            raise ValueError('ERROR: USE can only process .cls/.obs/.scs sources')
        if (nu,ns)==(0,0):
            return []
        elif (nu,ns)==(1,0):
            return uses
        elif (nu,ns)==(1,1):
            # order matter
            return uses+soils
        elif (nu,ns)==(0,1):
            raise ValueError('ERROR: .cls source is missing')
        else:
            raise ValueError('ERROR: too many .cls/.obs/.scs sources for USE')


    if command=='version':
        print('USE OCL version %s -- %s' % (
            USEEngine.useVersion(),
            'Copyright (C) 1999-2015 University of Bremen'))
    elif command in ['c', 'cli', 'gui']:
        files_for_use=_getSourcesForUSE(sources)
        _useInterface(
            interface=command,
            files=files_for_use
        )



def processSourceFile(filename, manySourceFiles, args):
    try:
        source=Megamodel.loadFile(filename)
    except Exception as e:
        traceback.print_exc(e)
        cprint(str(e),'red')
        return str(e)
    if manySourceFiles:
        cprint('#' * 30 + ' ' + filename + ' ' + '#' * 30, 'blue')
    printer_config=ModelPrinterConfig(# ContentPrinterConfig(  # TODO: check if creating a ModelPrinterConfig is better
        #  for models
        styled=not args.bw,
        verbose=args.verbose,
        quiet=args.quiet,
        title=source.basename,
        issuesMode=args.issues,
        contentMode=args.listing,
        summaryMode=args.summary,
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
        cprint(
            '#'*28+' END '+filename+' '+'#'*28+'\n'*2,
            'blue')
    return None


args=getArguments()
updateConfig(args)

try:
    manySourceFiles=len(args.sources)>=2
    for filename in args.sources:
        processSourceFile(filename, manySourceFiles, args)
    if args.use is not None:
        processUseCommand(args.use, args.sources)
except Exception as e:
    traceback.print_exc(e)
    cprint(str(e), 'red')


