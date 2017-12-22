# coding=utf-8

import modelscribes

from modelscribes.megamodels.megamodels import Megamodel
from modelscribes.scripts.megamodels.printer.megamodels import MegamodelPrinter


def test_megamodel_printer():
    MegamodelPrinter().display()



def test_display_megamodel():


    print('Metamodels:')

    print('  Metamodels by id')
    for (id,mm) in Megamodel._metamodelById.items():
        print('    %s -> %s' % (id, str(mm)))

    print('  Via metamodels()')
    for mm in Megamodel.metamodels():
        print('    %s' % mm.id)

    print('Metamodel dependencies:')
    for mmd in Megamodel.metamodelDependencies():
        print('  %s' % repr(mmd))

    Megamodel.checkMetamodelLevel()
