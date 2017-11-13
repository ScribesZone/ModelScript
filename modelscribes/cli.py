# coding=utf-8

import modelscribes.all
from modelscribes.megamodels.megamodels import Megamodel

def c(filename):
    return Megamodel.loadFile(filename)

M=Megamodel

print('cli LOADED')