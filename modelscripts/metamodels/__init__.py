# coding=utf-8

from modelscripts.megamodels.metametamodel import MetaPackage
from modelscripts.megamodels.metametamodel import MetaCheckerPackage
from modelscripts.scripts.metamodels.parser import PyMetamodelParser
META_PACKAGES=(
    'glossaries',
    'classes',
    'classes.expressions',
    'objects',
    'permissions',
    'permissions.accesses',
    'permissions.gpermissions',
    'permissions.sar',
    'scenarios',
    'scenarios.operations',
    'textblocks',
    'usecases',
    'tasks',
    'megamodels',
)

META_CHECKER_PACKAGES=(
    'classes.checkers',
    'usecases.checkers',
)

def loadMetaPackages():
    for name in META_PACKAGES:
        mp=MetaPackage(name)
        # PyMetamodelParser().parsePyModule(mp.pyModule)

def loadMetaCheckerPackages():
    for name in META_CHECKER_PACKAGES:
        mp=MetaCheckerPackage(name)



loadMetaPackages()
loadMetaCheckerPackages()
