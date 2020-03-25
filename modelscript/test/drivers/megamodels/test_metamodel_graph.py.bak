# coding=utf-8

import modelscript

from modelscript.megamodels import Megamodel
from modelscript.scripts.megamodels.printer.megamodels import MegamodelPrinter


def test_megamodel_printer():
    MegamodelPrinter().display()



def test_display_megamodel():


    print('Metamodels:')

    print('  Metamodels by id')
    for (id,mm) in Megamodel._metamodelById.items():
        print('    %s -> %s' % (id, unicode(mm)))

    print('  Via metamodels()')
    for mm in Megamodel.metamodels():
        print('    %s' % mm.id)

    print('Metamodel dependencies:')
    for mmd in Megamodel.metamodelDependencies():
        print('  %s' % repr(mmd))

    Megamodel.checkMetamodelLevel()
