# coding=utf-8
from __future__ import unicode_literals, print_function, absolute_import, division

from typing import Text, List

from modelscribes.base.printers import (
    ModelPrinter,
    SourcePrinter
)
from modelscribes.metamodels.permissions import (
    UCPermissionModel,
    METAMODEL
)
from modelscribes.metamodels.permissions.sar import Action


class PermissionModelPrinter(ModelPrinter):  # TODO: check implementation

    def __init__(self,
                 theModel,
                 summary=False,
                 displayLineNos=True):
        #type: (UCPermissionModel, bool, bool) -> None
        super(PermissionModelPrinter, self).__init__(
            theModel=theModel,
            summary=summary,
            displayLineNos=displayLineNos)
        self.permissionModel=theModel

    def do(self):
        super(PermissionModelPrinter, self).do()
        self._permissionModel(self.permissionModel)
        return self.output

    def _permissionModel(self, permissionModel):
        self.outLine(
            'permission model',
            lineNo=None, #usecaseModel.lineNo)  # TODO: change parser
            linesAfter=1 )
        self.outLine(
            str(permissionModel),
            indent=0,
            lineNo=None)
    #
    # def _rule(self, rule):
    #     self.outLine(str(rule))

# TODO: to be replaced by a generic version
class PermissionSourcePrinter(SourcePrinter):

    def __init__(self,
                 theSource,
                 summary=False,
                 displayLineNos=True):
        super(PermissionSourcePrinter, self).__init__(
            theSource=theSource,
            summary=summary,
            displayLineNos=displayLineNos)

    def do(self):
        self.output=''
        if self.theSource.isValid:
            p=PermissionModelPrinter(
                theModel=self.theSource.model,
                summary=self.summary,
                displayLineNos=self.displayLineNos
            ).do()
            self.out(p)
        else:
            self._issues()
        return self.output




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
METAMODEL.registerSourcePrinter(PermissionSourcePrinter)