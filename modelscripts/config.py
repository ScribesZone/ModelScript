# coding=utf-8

print('AA'*100)
levels={
    'SXP':0,
    'USE':0,
    'MGR':0,
    'MM3':0,
    'CCK':0,
}

class Config(object):
    preprocessorPrint=0
    realtimeImportPrint=0
    realtimeIssuePrint=0
    realtimeUSE=0
    realtimeCheckers=0

modules={
    'USE':'modelscripts.use.engine',
    'MGR':'modelscripts.use.engine.merger',
    'MM3':'modelscripts.megamodels.metametamodel',
    'CCK':'modelscripts.megamodels.checkers',
    'SXP':'modelscripts.use.sex.parser',
}

# import modelscripts.use.engine
# import modelscripts.use.engine.merger
# import modelscripts.megamodels.metametamodel
# import modelscripts.megamodels.checkers
# import modelscripts.use.sex.parser


# def setDebugLevels():
#     for key in modules.keys():
#         print('BB' + key)
#
#         modname=modules[key]
#         module = __import__(modname, globals(), locals(), ['DEBUG'], 0)
#         module.DEBUG=levels[key]
#         print(modname+'.DEBUG='+str(levels[key]))
#
#
# setDebugLevels()
