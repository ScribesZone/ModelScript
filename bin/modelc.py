# coding=utf-8
import sys
import os
import logging
from collections import OrderedDict


#TODO: add support for diagram generation (-d ?)
#TODO: add support for summary (-s ?)
#TODO: add support for source printing (-p ?)
#TODO: add support for code generation/transformation
#TODO: finish object model management
#TODO: add permission/access management
#TODO: -v / -e -w to display errors/suppress warning


thisDir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(thisDir,'..'))

import modelscripts.use.use.parser
# import modelscript.use.eval.tester
import modelscripts.use.engine

from modelscripts.scripts.glossaries.parser import (
    GlossaryModelSource
)
from modelscripts.scripts.glossaries.printer import (
    GlossaryModelPrinter
)

from modelscripts.scripts.classes.parser import (
    ClassModelSource
)
import modelscripts.scripts.classes.printer

from modelscripts.scripts.usecases.parser import (
    UsecaseModelSource
)
from modelscripts.scripts.permissions.parser import (
    PermissionModelSource
)
from modelscripts.scripts.scenarios.parser import (
    ScenarioModelSource,
    ScenarioEvaluationModelSource
)
from modelscripts.scripts.objects.parser import (
    ObjectModelSource
)

logging.basicConfig(level=logging.ERROR)


def missingFiles(files):
    return [
        f for f in files
        if not os.path.isfile(f)
    ]

def withExtension(files, extension):
    return [f for f in files if f.endswith(extension)]


class MegaModelCLI(object):

    def __init__(self, filenames):
        self.filenames=filenames
        self.checkFilenames()

        self.glossaryModelSource=None
        self.classModelSource=None
        self.usecaseModelSource=None
        self.permissionModelSource=None
        self.scenarioModelSources=[]
        self.objectModelSources=[]

    def checkFilenames(self):
        mf = missingFiles(self.filenames)
        if mf:
            print('These files do not exist : %s' % (
                ', '.join(mf)
            ))

    def processGlossaryModel(self):
        fs=withExtension(self.filenames,'.glm')
        if len(fs)==0:
            return
        elif len(fs)>=2:
            raise ValueError(
                'At most one .glm file.')
        self.glossaryModelSource=(
            GlossaryModelSource(fs[0])
        )
        # Is this test useful??? if self.glossaryModelSource is not None:
        GlossaryModelPrinter(self.glossaryModelSource).display()


    def processClassModelSource(self):
        fs=withExtension(self.filenames,'.use')
        if len(fs)==0:
            fs = withExtension(self.filenames, '.clm')
        if len(fs)==0:
            return
        elif len(fs)>=2:
            raise ValueError(
                'At most one .clm file.')
        else:
            self.classModelSource=(
                ClassModelSource(fs[0])
            )
            modelscripts.scripts.classes.printer.ClassSourcePrinter(
                theSource=self.classModelSource
            ).display()
            # # Is this test useful???   if self.classModelSource is not None:
            #
            # if not self.classModelSource.isValid:
            #     print('ERROR: model file is invalid')

    def processUsecaseModelSource(self):
        fs=withExtension(self.filenames,'.ucm')
        if len(fs)==0:
            return
        elif len(fs)>=2:
            raise ValueError(
                'At most one .ucm file.')
        else:
            self.usecaseModelSource=(
                UsecaseModelSource(fs[0])
            )
            # Is this test useful???   if self.usecaseModelSource is not None:
            self.usecaseModelSource.printStatus()
            if not self.usecaseModelSource.isValid:
                print('ERROR: model file is invalid.')


    def processPermissionModelSource(self):
        fs=withExtension(self.filenames,'.pmm')
        if len(fs)==0:
            return None
        elif len(fs)>=2:
            raise ValueError(
                'At most one .pmm file.')
        else:
            if self.classModelSource is None:
                print(
                    'ERROR: .pmm depends on unvailable .clm')
                return None
            elif not self.classModelSource.isValid:
                print(
                    'ERROR: .pmm depends on invalid .clm'
                )
                return None
            if self.usecaseModelSource is None:
                print(
                    'ERROR: .pmm depends on unvailable .ucm')
                return None
            elif not self.classModelSource.isValid:
                print(
                    'ERROR: .pmm depends on invalid .ucm'
                )
                return None

            self.permissionModelSource=(
                PermissionModelSource(permissionFileName=fs[0], usecaseModel=self.usecaseModelSource.usecaseModel,
                                      classModel=self.classModelSource.classModel)
            )
            # Is this test useful???  if self.permissionModelSource is not None:
            self.permissionModelSource.printStatus()
            if not self.permissionModelSource.isValid:
                print('ERROR: model file is invalid.')

    def processScenarioModelSources(self):
        fs=withExtension(self.filenames,'.scm')
        if len(fs)==0:
            fs = withExtension(self.filenames, '.soil')
        if len(fs)==0:
            return None
        else:
            if self.classModelSource is None:
                print(
                    'ERROR: .scm depends on unvailable .clm')
                return None
            elif not self.classModelSource.isValid:
                print(
                    'ERROR: .scm depends on invalid .clm'
                )
                return None
            if False:
                # only if usecase model is compulsory
                if self.usecaseModelSource is None:
                    print(
                        'ERROR: .scm depends on unvailable .ucm')
                    return None
                elif not self.classModelSource.isValid:
                    print(
                        'ERROR: .scm depends on invalid .ucm'
                    )
                    return None
            for snfile in fs:
                scnsource= ScenarioEvaluationModelSource(soilFileName=self.classModelSource.classModel,
                                                         classModel=self.classModelSource.classModel, usecaseModel=(
                        None if self.usecaseModelSource is None
                        else self.usecaseModelSource.usecaseModel))
                # Is this test useful???  if scnsource is None:
                #    print('Error: %s is invalid. Ignored.' % snfile)
                # else:
                self.scenarioModelSources.append(scnsource)
                scnsource.printStatus()
                if not scnsource.isValid:
                    print('ERROR: model file is invalid.')

    def processObjectModelSources(self):
        fs=withExtension(self.filenames,'.obm')
        if len(fs)==0:
            fs = withExtension(self.filenames, '.soil')
        if len(fs)==0:
            return None
        else:
            if self.classModelSource is None:
                print(
                    'ERROR: .obm depends on unvailable .clm')
                return None
            elif not self.classModelSource.isValid:
                print(
                    'ERROR: .obm depends on invalid .clm'
                )
                return None
            for obfile in fs:
                obsource= ObjectModelSource(soilFileName=self.classModelSource.classModel,
                                            classModel=self.classModelSource.classModel)
                # Is this test useful???   if obsource is None:
                #    print('Error: %s is invalid. Ignored.' % obfile)
                # else:
                self.objectModelSources.append(obsource)
                obsource.printStatus()
                if not obsource.isValid:
                    print('ERROR: model file is invalid.')



def printVersion():
    version = modelscripts.use.engine.USEEngine.useVersion()
    print("modelc - based on use version %s - University of Bremen" % version)


def main():
    if len(sys.argv)==1:
        printVersion()
    else:
        filenames=sys.argv[1:]
        mgm=MegaModelCLI(filenames)
        mgm.processGlossaryModel()
        mgm.processClassModelSource()
        mgm.processUsecaseModelSource()
        mgm.processObjectModelSources()
        mgm.processPermissionModelSource()
        mgm.processScenarioModelSources()

main()