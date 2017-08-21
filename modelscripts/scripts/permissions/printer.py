# coding=utf-8
from __future__ import unicode_literals, print_function, absolute_import, division
from typing import Text, Union, Optional, Dict, List

from modelscripts.source.printer import (
    AbstractPrinter
)

from modelscripts.metamodels.permissions import (
    PermissionModel,
    PermissionStatement,
    Ops,
    Op,
)
from modelscripts.metamodels.usecases import (
    Usecase,
    Actor,
)
from modelscripts.metamodels.classes import (
    Class,
    Association,
    AssociationClass,
    Attribute,
    Role,
)



class Printer(AbstractPrinter):

    def __init__(self, permissionModel, displayLineNos=True):
        #type: (PermissionModel, bool) -> None
        super(Printer,self).__init__(
            displayLineNos=displayLineNos)
        self.permissionModel=permissionModel

    def do(self):
        super(Printer,self).do()
        self._permissionModel(self.permissionModel)
        return self.output

    def _permissionModel(self, permissionModel):
        self.outLine(
            'permission model',
            lineNo=None, #usecaseModel.lineNo)  # TODO: change parser
            linesAfter=1 )
        for stmt in permissionModel.statements:
            self._statement(stmt)


    def _statement(self, stmt):

        self.outLine(
            '%s %s %s' % (
                ','.join([playerString(p) for p in stmt.players]),
                opsString(stmt.ops),
                ','.join([resourceString(r) for r in stmt.resources]
        )))




def playerString(player):
    if isinstance(player, (Usecase, Actor)):
        return player.name
    else:
        raise NotImplementedError(
            'ERROR: playerString(%s) is not implemented' % (
                type(player)
        ))

def resourceString(resource):
    if isinstance(resource, (Class, AssociationClass, Association)):
        return resource.name
    elif isinstance(resource, Attribute):
        return '%s.%s' % (
            resource.class_.name,
            resource.name
        )
    elif isinstance(resource, Role):
        return '%s.%s' % (
            resource.association.name,
            resource.name
        )
    else:
        raise NotImplementedError(
            'ERROR: playerString(%s) is not implemented' % (
                type(resource)
        ))

def opString(op):
    #type:  (Op)->Text
    return op

def opsString(ops):
    #type: (Ops)->Text
    return ''.join(
        [ c if c in ops else ""
          for c in "CRUD"]
    )