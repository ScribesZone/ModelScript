# coding=utf-8

from modelscript.megamodels.metametamodel import MetaPackage
from modelscript.megamodels.metametamodel import MetaCheckerPackage
from modelscript.scripts.metamodels.parser import PyMetamodelParser
META_PACKAGES=(
    # accesses ?
    'aui',
    'classes',
    'classes.assocclasses',
    'classes.classes',
    'classes.core',
    'classes.invariants',
    'classes.types',
    'glossaries',
    'megamodels',
    'objects',
    'objects.linkobjects',
    'objects.links',
    'objects.objects',
    'objects',
    'participants',
    'permissions',
    'permissions.accesses',
    'permissions.gpermissions',
    'permissions.sar',
    'projects',
    'qa',
    'qc',
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
    'glossaries.checkers',
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
