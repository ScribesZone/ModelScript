# coding=utf-8
"""
"""

# TODO: implement error management

from __future__ import absolute_import, division, print_function, unicode_literals
from future.utils import python_2_unicode_compatible
from typing import Text, List, Set, Dict, Optional, Union
import os
import re

from modelscripts.source.sources import SourceFile

from modelscripts.scripts.permissions.printer import (
    Printer
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

from modelscripts.metamodels.permissions import (
    PermissionModel,
    PermissionStatement,
    Player,
    Resource,
    Entity
)



DEBUG=0

class PermissionModelSource(SourceFile):
    def __init__(self, usecaseModel, classModel, filename):
        #type: (UsecaseModel, ClassModel, str)->None
        super(PermissionModelSource, self).__init__()

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
        self.usecaseModel = usecaseModel
        self.classModel = classModel
        self.permissionModel = PermissionModel(
            usecaseModel=usecaseModel,
            classModel=classModel,
        )
        self._parse()
        self.isValid=True # Todo, check errors, etc.


    def printStatus(self):
        """
        Print the status of the file:

        * the list of errors if the file is invalid,
        * a short summary of entities (classes, attributes, etc.) otherwise
        """

        if self.isValid:
            p=Printer(
                permissionModel=self.permissionModel,
                displayLineNos=True,
            )
            print(p.do())
        else:
            print('%s error(s) in the model'  % len(self.errors))
            for e in self.errors:
                print(e)


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
                players=_resolve_players(self.usecaseModel, player_strs)
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


        if self.usecaseModel.system is None:
            raise SyntaxError(
                'Error: no system defined'
            )



#---------------------------------------------------------
#   Model resolution
#---------------------------------------------------------

# TODO: this code should go elsewhere
# it is about naming, namespaces, etc. so more general


def _resolve_players(usecaseModel, playersStrs):
    #type: (UsecaseModel, List[Text])->Union[List[Player], Text]
    """
    Resolve all list of players.
    Return the faulty string in case of error.
    This could serve to build an error message.
    """

    _ = []
    for ps in playersStrs:
        if ps is not '':
            p=_resolve_player(usecaseModel, ps)
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


def _resolve_player(usecaseModel, name):
    #type: (usecaseModel,Text)->Optional[Player]
    """ Search the name in usecases or actors
    """
    if DEBUG>=2:
        print('resolve_player "%s' %  name)
    if name in usecaseModel.actorNamed:
        return usecaseModel.actorNamed[name]
    elif name in usecaseModel.system.usecaseNamed:
        return usecaseModel.system.usecaseNamed[name]
    else:
        return None

def _resolve_entity(classModel, name):
    #type: (ClassModel,Text)->Optional[Entity]
    """ Search the name in class/association/associationclass
    """
    if DEBUG>=2:
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
    if DEBUG>=2:
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

