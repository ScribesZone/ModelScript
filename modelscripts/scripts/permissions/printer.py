# coding=utf-8
from __future__ import unicode_literals, print_function, absolute_import, division

from typing import Text, List, Optional

from modelscripts.scripts.base.printers import (
    ModelPrinter,
    ModelSourcePrinter,
    ModelPrinterConfig,
)
from modelscripts.metamodels.permissions import (
    UCPermissionModel,
    METAMODEL
)
from modelscripts.metamodels.permissions.sar import Action


class PermissionModelPrinter(ModelPrinter):

    def __init__(self,
                 theModel,
                 config=None):
        #type: (UCPermissionModel, Optional[ModelPrinterConfig]) -> None
        super(PermissionModelPrinter, self).__init__(
            theModel=theModel,
            config=config
        )
        self.theModel=theModel

    def doModelContent(self):
        super(PermissionModelPrinter, self).doModelContent()
        self.doPermissionModel(self.theModel)
        return self.output

    def doPermissionModel(self, permissionModel):
        self.doModelTextBlock(permissionModel.description)
        for rule in permissionModel.rules:
            self.doFactorizedPermissionRule(rule)

    def doFactorizedPermissionRule(self, rule):
        separator=self.kwd(',')
        subjects_str=separator.join([
            self.getSubject(s)
            for s in rule.subjects])
        actions_str=separator.join([
            self.getAction(s)
            for s in rule.actions])
        resources_str = separator.join([
            self.getResource(s)
            for s in rule.resources])
        self.outLine('%s %s %s %s' %(
            subjects_str,
            self.kwd('can'),
            actions_str,
            resources_str
        ))
        self.doModelTextBlock(rule.description)


    def getSubject(self, subject):
        return subject.subjectLabel

    def getAction(self, action):
        return action.actionLabel

    def getResource(self, resource):
        return resource.resourceLabel




# def playerString(player):
#     if isinstance(player, (Usecase, Actor)):
#         return player.name
#     else:
#         raise NotImplementedError(
#             'ERROR: playerString(%s) is not implemented' % (
#                 type(player)
#         ))
#
# def resourceString(resource):
#     if isinstance(resource, (Class, AssociationClass, Association)):
#         return resource.name
#     elif isinstance(resource, Attribute):
#         return '%s.%s' % (
#             resource.class_.name,
#             resource.name
#         )
#     elif isinstance(resource, Role):
#         return '%s.%s' % (
#             resource.association.name,
#             resource.name
#         )
#     else:
#         raise NotImplementedError(
#             'ERROR: playerString(%s) is not implemented' % (
#                 type(resource)
#         ))

def actionName(action):
    #type:  (Action)->Text
    return action.name

def actionNames(actions):
    #type: (List[Action])->Text
    _=[]
    names=[a.name for a in actions]
    # TODO: add the case with other labels
    return ''.join(
        [ name if names in names else ""
          for name in 'CRUDX']
    )

METAMODEL.registerModelPrinter(PermissionModelPrinter)
METAMODEL.registerSourcePrinter(ModelSourcePrinter)