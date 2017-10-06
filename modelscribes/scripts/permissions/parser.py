# coding=utf-8
"""
"""

# TODO: implement error management

from __future__ import absolute_import, division, print_function, unicode_literals

import re

from typing import Text, List, Optional, Union

from modelscribes.megamodels.sources import ModelSourceFile
from modelscribes.metamodels.classes import (
    Entity,
    ClassModel,
    Class,
    Association,
    AssociationClass,
)
from modelscribes.metamodels.permissions import (
    UCPermissionModel,
    FactorizedPermissionRule,
    METAMODEL
)
from modelscribes.metamodels.permissions.sar import Subject, Action, Resource
from modelscribes.metamodels.usecases import (
    UsecaseModel,
)
from modelscribes.scripts.permissions.printer import (
    PermissionModelPrinter
)

DEBUG=4

class PermissionModelSource(ModelSourceFile):

    def __init__(self, fileName):
        #type: (Text)->None
        super(PermissionModelSource, self).__init__(
            fileName=fileName)

        self._parse()
        # Todo, check errors, etc.

    @property
    def permissionModel(self):
        #type: () -> UCPermissionModel
        m=self.model #type: UCPermissionModel
        return m

    @property
    def metamodel(self):
        return METAMODEL

    @property
    def megamodelStatementPrefix(self):
        return r' *(--)? *@'

    def printStatus(self):
        """
        Print the status of the file:

        * the list of errors if the file is invalid,
        * a short summary of entities (classes,
          attributes, etc.) otherwise
        """

        if self.isValid:
            p=PermissionModelPrinter(
                permissionModel=self.permissionModel,
                displayLineNos=True,
            )
            print(p.do())
        else:
            print('%s error(s) in the model' % len(self.issueBox))
            for e in self.issueBox:
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

            print(original_line)

            if DEBUG>=2:
                print ('#%i : %s' % (line_no, original_line))

            #---- blank lines ------------------------
            r = '^ *$'
            m = re.match(r, line)
            if m:
                continue

            #---- comments ----------------------------
            r = '^ *--.*$'
            m = re.match(r, line)
            if m:
                continue


            #--- permission statement ------------------
            r = (begin(0)
                 +r' *(?P<subjects>[\w,]+)'
                 +r' +(?P<actions>C?R?U?D?X?)'
                 +r' +(?P<resources>[\w,\.]+)$')
            m = re.match(r, line)
            if m:
                #---- subjects
                subject_strs=m.group('subjects').split(',')
                subjects=_resolve_subjects(self.usecaseModel, subject_strs)
                if not isinstance(subjects, list):
                    raise ValueError(
                        'Error at line %i. Subject "%s" does not exist' % (
                            line_no, subjects))

                #---- ops
                actions=[]
                for action_name in m.group('actions'):
                    action=Action.named(action_name)
                    if action not in actions:
                        actions.append(action)
                if len(actions)==0 :
                    raise SyntaxError(
                        'Syntax error at line %i. No action specified'
                        % line_no
                    )

                #---- resources
                resource_strs=m.group('resources').split(',')
                resources=_resolve_resources(self.classModel, resource_strs)
                if not isinstance(resources, list):
                    raise ValueError(
                        'Error at line %i. Resource "%s" does not exist' % (
                            line_no, resources))
                rule=FactorizedPermissionRule(
                    model=self.permissionModel,
                    subjects=subjects,
                    actions=actions,
                    resources=resources
                )
                self.permissionModel.rules.append(rule)
                # print ('******************',rule)
                # print (len(self.permissionModel.rules))

                continue

            raise SyntaxError(
                'Error: cannot parse line #%s: %s' % (
                    line_no,
                    original_line
                ))

        # TODO: is this a copy paste ?
        if self.usecaseModel.system is None:
            raise SyntaxError(
                'Error: no system defined'
            )



#---------------------------------------------------------
#   Model resolution
#---------------------------------------------------------

# TODO: this code should go elsewhere
# it is about naming, namespaces, etc. so more general


def _resolve_subjects(usecaseModel, subjectStrs):
    #type: (UsecaseModel, List[Text])->Union[List[Subject], Text]
    """
    Resolve all list of subjects.
    Return the faulty string in case of error.
    This could serve to build an error message.
    """

    _ = []
    for ss in subjectStrs:
        if ss is not '':
            p=_resolve_subject(usecaseModel, ss)
            if p is not None:
                _.append(p)
            else:
                return ss
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


def _resolve_subject(usecaseModel, name):
    #type: (usecaseModel,Text)->Optional[Subject]
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

# TODO: move this to metamodels.classes ?
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

# TODO: move this to metamodels.classes ?
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

METAMODEL.registerSource(PermissionModelSource)
