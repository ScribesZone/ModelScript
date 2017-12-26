# coding=utf-8

from modelscripts.megamodels.metametamodel import MetaPackage
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
    # 'scenarios.assertions'
    'scenarios.blocks',
    'scenarios.operations',
    'scenarios.evaluations',
    'scenarios.evaluations.blocks',
    'scenarios.evaluations.operations',
    'textblocks',
    'usecases',
)

import modelscripts.metamodels.classes.checks
import modelscripts.metamodels.scenarios.evaluations.checks



for m_name in META_PACKAGES:
    mp=MetaPackage(m_name)
    # PyMetamodelParser().parsePyModule(mp.pyModule)

