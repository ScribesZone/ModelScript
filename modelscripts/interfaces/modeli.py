# coding=utf-8

import sys
import os

#------ add modescribes to the path -------------------
modelscribes_home=os.path.realpath(
    os.path.join(
        os.path.dirname(__file__),
        '..','..'))
sys.path.insert(0,modelscribes_home)
# sys.path.append("/home/jmfavre/.config/gedit")
# sys.path.append("/home/jmfavre/.local/share/gtksourceview-3.0/language-specs")
#------------------------------------------------------


import modelscripts
from modelscripts.megamodels import Megamodel

def source(filename):
    return Megamodel.loadFile(filename)

s=source

M=Megamodel

gl=Megamodel.theMetamodel(id='gl')
cl=Megamodel.theMetamodel(id='cl')
us=Megamodel.theMetamodel(id='us')
ob=Megamodel.theMetamodel(id='ob')
pe=Megamodel.theMetamodel(id='pe')
sc=Megamodel.theMetamodel(id='sc')
mg=Megamodel.theMetamodel(id='mg')



print('ModelScripts Interpreter')
print('========================')
print("source('foo.cls')   to load the file 'foo.cls'")
print('quit()              to quit this session')
print('M                   to get the megamodel')
