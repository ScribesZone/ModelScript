# coding=utf-8
"""
Initialize the megamodel with
- all metamodels
- all scripts (parsers/printers/plantuml/...)
- the configuration

This module is called by the environant
"""

import modelscript.metamodels
import modelscript.scripts
import modelscript.config

MEGAMODEL=None
# filled later with Megamodel.
# This allow to have a global access to megamodel without
# circular dependences
def finishMegamodel():
    from modelscript.megamodels import (Megamodel, METAMODEL)
    Megamodel.model=Megamodel()
    Megamodel.model.name='megamodel'
    from modelscript.metamodels.megamodels import _setMetaModel
    _setMetaModel(METAMODEL)
    global MEGAMODEL
    MEGAMODEL=Megamodel

finishMegamodel()