# coding=utf-8

from modelscripts.megamodels.metametamodel import MetaPackage
from modelscripts.megamodels.metametamodel import MetaCheckerPackage
from modelscripts.scripts.metamodels.parser import PyMetamodelParser
META_PACKAGES=(
    'aui',
    'classes',
    'classes.expressions',
    'glossaries',
    'megamodels',
    'objects',
    'permissions',
    'permissions.accesses',
    'permissions.gpermissions',
    'permissions.sar',
    'relations',
    'scenarios',
    'stories',
    'stories.operations',
    'stories.evaluations',
    'stories.evaluations.operations',
    'tasks',
    'textblocks',
    'usecases',
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
