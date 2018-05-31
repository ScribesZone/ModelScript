# coding=utf-8
"""
Initialize the megamodel with
- all metamodels
- all scripts (parsers/printers/plantuml/...)
- the configuration

This module is called by the environant
"""

import modelscripts.metamodels
import modelscripts.scripts
import modelscripts.config

MEGAMODEL=None
# filled later with Megamodel.
# This allow to have a global access to megamodel without
# circular dependences
def finishMegamodel():
    from modelscripts.megamodels import (Megamodel, METAMODEL)
    Megamodel.model=Megamodel()
    Megamodel.model.name='megamodel'
    from modelscripts.metamodels.megamodels import _setMetaModel
    _setMetaModel(METAMODEL)
    global MEGAMODEL
    MEGAMODEL=Megamodel

finishMegamodel()