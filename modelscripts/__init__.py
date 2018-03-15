# coding=utf-8

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