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
    # 'scenarios.assertions'  not yet
    'scenarios.blocks',
    'scenarios.operations',
    'scenarios.evaluations',
    'scenarios.evaluations.blocks',
    'scenarios.evaluations.operations',
    'textblocks',
    'usecases',
    'megamodels',
)

META_CHECKER_PACKAGES=(
    'classes.checkers',
    'usecases.checkers',
    'scenarios.evaluations.checkers'
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
