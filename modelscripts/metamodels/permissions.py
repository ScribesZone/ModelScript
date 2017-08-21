# coding=utf-8
"""

"""
from __future__ import absolute_import, division, print_function, unicode_literals
from future.utils import python_2_unicode_compatible
from typing import Text, List, Dict, Optional, Union, Set

from modelscripts.utils import Model
from modelscripts.source.sources import (
    SourceFile,
    SourceElement
)
from modelscripts.metamodels.classes import (
    ClassModel,
    Class,
    Association,
    AssociationClass,
    Attribute,
    Role,
)
from modelscripts.metamodels.usecases import (
    UsecaseModel,
    Actor,
    Usecase,
)

Player = Union[Actor, Usecase]
Entity = Union[Class, Association, AssociationClass]
Member = Union[Attribute, Role]
Resource = Union[Entity, Member]
Op=Union['C','R','U','D']
Ops=Set[Op]

#---------------------------------------------------------------
#  Abstract syntax
#---------------------------------------------------------------

class PermissionModel(Model):
    def __init__(self, usecaseModel, classModel, source=None):
        #type: (UsecaseModel, ClassModel, SourceFile) -> None
        super(PermissionModel, self).__init__(source=source)
        self.usecaseModel=usecaseModel
        self.classModel=classModel
        self.statements=[]      #type: List[PermissionStatement]

    def interpret(self):
        #type ()->PermissionSet
        pms=PermissionSet()

        for stmt in self.statements:
            for pl in stmt.players:
                for rc in stmt.resources:
                    pms.permissions.add(
                        Permission(pl,stmt.ops,rc))
        return pms

class PermissionStatement(SourceElement):
    def __init__(self, model, players, ops, resources, lineNo=None):
        #type: (PermissionModel, List[Player], Ops, List[Resource])->None
        super(PermissionStatement, self).__init__(lineNo=lineNo)

        self.model=model            #type: PermissionModel
        self.players=players        #type: List[Player]
        self.ops=ops                #type: Ops
        self.resources=resources    #type: List[Resource]



#---------------------------------------------------------------
#  Semantics
#---------------------------------------------------------------

@python_2_unicode_compatible
class Permission(object):
    def __init__(self, player, ops, resource):
        #type: (Player, Ops, Member) -> None
        self.player=player      #type: Player
        self.ops=ops            #type: Ops
        self.resource=resource  #type: Resource

    # def __str__(self):
    #     return ('Permission(%s,%s,%s)' % (
    #         self.player.name,
    #         opsStr(self.ops),
    #         self.resource.name
    #     ))


class PermissionSet(object):
    def __init__(self):
        #type: ()->None

        self.permissions = set()







