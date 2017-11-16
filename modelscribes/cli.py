# coding=utf-8

import modelscribes.all
from modelscribes.megamodels.megamodels import Megamodel

def source(filename):
    return Megamodel.loadFile(filename)
s=source

M=Megamodel

gl=Megamodel.metamodel(id='gl')
cl=Megamodel.metamodel(id='cl')
us=Megamodel.metamodel(id='us')
ob=Megamodel.metamodel(id='ob')
pe=Megamodel.metamodel(id='pe')
sc=Megamodel.metamodel(id='sc')



print('cli LOADED')