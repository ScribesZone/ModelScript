# coding=utf-8

import sys
import os

#------ add modescribes to the path -------------------
modelscribes_home=os.path.realpath(
    os.path.join(
        os.path.dirname(__file__),
        '..'))
sys.path.insert(0,modelscribes_home)
# sys.path.append("/home/jmfavre/.config/gedit")
# sys.path.append("/home/jmfavre/.local/share/gtksourceview-3.0/language-specs")
#------------------------------------------------------


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



print('ModelScribes Interpreter')
print('========================')