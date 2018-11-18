# coding=utf-8
#
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
    'USE':'modelscript.use.engine',
    'MGR':'modelscript.use.engine.merger',
    'MM3':'modelscript.megamodels.metametamodel',
    'CCK':'modelscript.megamodels.checkers',
    'SXP':'modelscript.use.sex.parser',
}
# from modelscript.base.issues import DEBUG
# print(DEBUG)
# ISS=0

# import modelscript.megamodels.metametamodel
# import modelscript.megamodels.checkers
# import modelscript.use.sex.parser
#
#
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
