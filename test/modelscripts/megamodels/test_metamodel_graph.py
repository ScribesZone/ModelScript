# coding=utf-8

import modelscribes.metamodels  # DO NOT REMOVE
import modelscribes.scripts.parsers # DO NOT REMOVE
import modelscribes.scripts.printers # DO NOT REMOVE

from modelscribes.megamodels.megamodels import Megamodel


def test_display_megamodel():


    print('Metamodels:')

    print('  By id')
    for (id,mm) in Megamodel._metamodelById.items():
        print('    %s -> %s' % (id, mm))

    print('  Via metamodels()')
    for mm in Megamodel.metamodels():
        print('    %s' % repr(mm))

    print('Metamodel dependencies:')
    for mmd in Megamodel.metamodelDependencies():
        print('  %s' % repr(mmd))

    Megamodel.checkMetamodelLevel()
