# coding=utf-8
"""
"""

# TODO: implement error management

from __future__ import absolute_import, division, print_function, unicode_literals
from future.utils import python_2_unicode_compatible
from typing import Text, List, Set, Dict, Optional, Union
import os
import re

from pyuseocl.metamodel.classes import (
    ClassModel,
    Class,
    Association,
    AssociationClass,
    Attribute,
    Role,
)

from pyuseocl.metamodel.usecases import (
    System,
    Actor,
    Usecase,
)

from pyuseocl.metamodel.permissions import (
    PermissionModel,
    PermissionStatement,
    Player,
    Resource,
    Entity
)


DEBUG=3

class PermissionModelSource(object):
    def __init__(self, system, classModel, filename):
        #type: (System, ClassModel, str)->None

        if not os.path.isfile(filename):
            raise Exception('File "%s" not found' % filename)
        self.fileName = filename  #type: str
        self.sourceLines = (   #type: List[str]
            line.rstrip()
            for line in open(self.fileName, 'rU'))
        self.directory = os.path.dirname(self.fileName) #type: str
        self.isValid = None #type: bool
        self.errors = [] # Todo, check errors, etc.
        self.lines = None # Todo, check errors, etc.
        self.ignoredLines = []
        self.system = system
        self.classModel = classModel
        self.permissionModel = PermissionModel(
            system=system,
            classModel=classModel,
        )
        self._parse()
        self.isValid=True # Todo, check errors, etc.

    def _parse(self):

        def begin(n): return '^'
        end = ' *$'

        if DEBUG>=1:
            print('\nParsing %s\n' % self.fileName)

        for (line_index, line) in enumerate(self.sourceLines):
            original_line = line
            # replace tabs by spaces
            line = line.replace('\t',' ')
            line_no = line_index+1

            if DEBUG>=2:
                print ('#%i : %s' % (line_no, original_line))

            #---- blank lines ---------------------------------------------
            r = '^ *$'
            m = re.match(r, line)
            if m:
                continue

            #---- comments -------------------------------------------------
            r = '^ *--.*$'
            m = re.match(r, line)
            if m:
                continue


            #--- permission statement ------------------------
            r = (begin(0)
                 +r' *(?P<players>[\w,]+)'
                 +r' +(?P<ops>C?R?U?D?)'
                 +r' +(?P<resources>[\w,\.]+)')
            m = re.match(r, line)
            if m:
                #---- players
                player_strs=m.group('players').split(',')
                players=_resolve_players(self.system, player_strs)
                if not isinstance(players, list):
                    raise ValueError(
                        'Error at line %i. Player "%s" does not exist' % (
                            line_no, players))

                #---- ops
                ops=set(m.group('ops'))
                if len(ops)==0 :
                    raise SyntaxError(
                        'Syntax error at line %i. No (CRUD) operation specified'
                        % line_no
                    )

                #---- resources
                resource_strs=m.group('resources').split(',')
                resources=_resolve_resources(self.classModel, resource_strs)
                if not isinstance(resources, list):
                    raise ValueError(
                        'Error at line %i. Resource "%s" does not exist' % (
                            line_no, resources))
                pstmt=PermissionStatement(
                    model=self.permissionModel,
                    players=players,
                    ops=ops,
                    resources=resources
                )
                self.permissionModel.statements.append(pstmt)
                continue


        if self.system is None:
            raise SyntaxError(
                'Error: no system defined'
            )


def _resolve_players(system, playersStrs):
    #type: (System,List[Text])->Union[List[Player],Text]
    """
    Resolve all list of players.
    Return the faulty string in case of error.
    This could serve to build an error message.
    """

    _ = []
    for ps in playersStrs:
        if ps is not '':
            p=_resolve_player(system, ps)
            if p is not None:
                _.append(p)
            else:
                return ps
    return _

def _resolve_resources(classModel, resourcesStrs):
    #type: (ClassModel,List[Text])->Union[List[Resource],Text]
    """
    Resolve all list of resources.
    Return the faulty string in case of error.
    This could serve to build an error message.
    """

    _ = []
    for rs in resourcesStrs:
        if rs is not '':
            r=_resolve_resource(classModel, rs)
            if r is not None:
                _.append(r)
            else:
                return rs
    return _


def _resolve_player(system, name):
    #type: (System,Text)->Optional[Player]
    """ Search the name in usecases or actors
    """
    print('resolve_player "%s' %  name)
    if name in system.actorNamed:
        return system.actorNamed[name]
    elif name in system.usecaseNamed:
        return system.usecaseNamed[name]
    else:
        return None

def _resolve_entity(classModel, name):
    #type: (ClassModel,Text)->Optional[Entity]
    """ Search the name in class/association/associationclass
    """
    print('resolve_entity "%s"' % name)
    if name in classModel.classNamed:
        return classModel.classNamed[name]
    elif name in classModel.associationNamed:
        return classModel.associationNamed[name]
    elif name in classModel.associationClassNamed:
        return classModel.associationClassNamed[name]
    else:
        return None

def _resolve_resource(classModel, expr):
    #type: (ClassModel,Text)->Optional[Resource]
    """ Search the expr in class/association/associationclass/attribute/role
        The expression could look like X or X.y
    """
    print('resolve_resource "%s"' % expr)
    parts=expr.split('.')
    if len(parts)>=3:
        return None
    entity_name=parts[0]
    member_name=None if len(parts)==1 else parts[1]
    entity=_resolve_entity(classModel, entity_name)
    if entity is None:
        return None
    if member_name is None:
        return entity
    if isinstance(entity, Class):
        if member_name in entity.attributeNamed:
            return entity.attributeNamed[member_name]
        else:
            return None
    elif isinstance(entity, Association):
        if member_name in entity.roleNamed:
            return entity.roleNamed[member_name]
        else:
            return None
    elif isinstance(entity, AssociationClass):
        if member_name in entity.attributeNamed:
            return entity.attributeNamed[member_name]
        elif member_name in entity.roleNamed:
            return entity.roleNamed[member_name]
        else:
            return None
    else:
        return None

