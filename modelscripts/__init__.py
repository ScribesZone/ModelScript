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


def finishMegamodel():
    from modelscripts.megamodels import (Megamodel, METAMODEL)
    Megamodel.model=Megamodel()
    Megamodel.model.name='megamodel'
    from modelscripts.metamodels.megamodels import _setMetaModel
    _setMetaModel(METAMODEL)


finishMegamodel()