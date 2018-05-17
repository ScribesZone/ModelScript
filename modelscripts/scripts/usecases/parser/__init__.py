# coding=utf-8

"""
Generate a usecase model from a usecase script.
"""

from __future__ import (
    unicode_literals, print_function, absolute_import, division
)
from typing import Text
import re

import os
import logging

from modelscripts.megamodels.sources import ModelSourceFile

from modelscripts.scripts.megamodels.parser import (
    isMegamodelStatement
)

from modelscripts.base.issues import (
    LocalizedSourceIssue,
    Levels,
)
from modelscripts.metamodels.usecases import (
    UsecaseModel,
    Actor,
    Usecase,
    METAMODEL
)

from textx import metamodel_from_file
from modelscripts.scripts.base.grammars import (
    Grammar,
    AST
)




__all__=(
    'initModule'
    'UsecaseModelSource'
)

DEBUG=0

def initModule():
    pass

class UsecaseModelSource(ModelSourceFile):

    def __init__(self, usecaseFileName):
        #type: (Text) -> None
        this_dir=os.path.dirname(os.path.realpath(__file__))
        print('CC'*20,this_dir)
        self.grammar=Grammar(
            'usecases',
            this_dir
        )
        self.ast=None
        super(UsecaseModelSource, self).__init__(
            fileName=usecaseFileName
        )


    @property
    def usecaseModel(self):
        #type: () -> UsecaseModel
        m=self.model #type: UsecaseModel
        return m


    @property
    def metamodel(self):
        return METAMODEL

    def parseToFillModel(self):

        # def _checkSystemExist(isLast=False):
        #     if not self.usecaseModel.isSystemDefined:
        #         LocalizedSourceIssue(
        #             sourceFile=self,
        #             level=Levels.Fatal,
        #             message='System is not defined %s' %
        #                     (' yet.' if not isLast else '!'),
        #             line=line_no,
        #         )

        def _ensureActor(name):
            # _checkSystemExist(isLast=False)
            if name in self.usecaseModel.actorNamed:
                return self.usecaseModel.actorNamed[name]
            else:
                return Actor(self.usecaseModel, name)

        def _ensureUsecase(name):
            # _checkSystemExist(isLast=False)
            if name in (self.usecaseModel.system.usecaseNamed):
                return self.usecaseModel.system.usecaseNamed[name]
            else:
                return Usecase(self.usecaseModel.system, name)


        if DEBUG>=1:
            print('\nParsing %s\n' % self.fileName)

        print('Hello usecases')


        self.ast = AST(self.grammar, self.fileName)

        # self.usecaseModel.system.setInfo(
          #                  name=name   #,
                            # lineNo=line_no,
                       # )
        for declaration in self.ast.model.declarations:
            type_=declaration.__class__.__name__
            if type_=='Usecase':
                usecase_decl=declaration
                _ensureUsecase(usecase_decl.name)
            elif type_=='Actor':
                actor_decl=declaration
                _ensureUsecase(actor_decl.name)
            elif type_=='Interactions':
                for interaction in declaration.interactions:
                    a=_ensureActor(interaction.actor)
                    u=_ensureUsecase(interaction.usecase)
                    a.addUsecase(u)
            else:
                raise NotImplementedError(
                    'Unexpected type %s' % type_)


#         current_actor=None
#         current_usecase=None
#         #FIXME: use doc-for in all the parser
#         current_element=self.usecaseModel
#         current_scope='model'
# # model | system | actor | usecase | actor.usecases
#
#         for (line_index, line) in enumerate(self.sourceLines):
#             original_line = line
#             # replace tabs by spaces
#             line = line.replace('\t',' ')
#             line_no = line_index+1
#
#             if DEBUG>=2:
#                 print ('#%i : %s' % (line_no, original_line))
#
#             #---- blank lines ---------------------------------
#             r = '^ *$'
#             m = re.match(r, line)
#             if m:
#                 continue
#
#             #---- comments -------------------------------------
#             r = '^ *--.*$'
#             m = re.match(r, line)
#             if m:
#                 continue
#
#             #---- description ----------------------------------
#             r = '^ *\|(?P<line>.*)$'
#             m = re.match(r, line)
#             if m:
#                 current_element.description.addNewLine(
#                     stringLine=m.group('line'),
#                     lineNo=line_no,
#                 )
#                 continue
#
#
#             #---- megamodel statements -------------
#             is_mms=isMegamodelStatement(
#                 lineNo=line_no,
#                 modelSourceFile=self)
#             if is_mms:
#                 # megamodel statements have already been
#                 # parse so silently ignore them
#                 continue
#
#
#             #--- system X -------------------------
#             r = begin(0)+r'system +(?P<name>\w+)'+end
#             m = re.match(r, line)
#             if m:
#                 if self.usecaseModel.isSystemDefined:
#                     LocalizedSourceIssue(
#                         sourceFile=self,
#                         level=Levels.Warning,
#                         message='System defined twice',
#                         line=line_no,
#                     )
#                 name=m.group('name')
#                 self.usecaseModel.system.setInfo(
#                     name=name,
#                     lineNo=line_no,
#                 )
#                 current_element=self.usecaseModel.system
#                 current_scope='system'
#                 continue
#
#             #--- actor X --------------------------
#             r =(begin(0)
#                 +r'(?P<kind>(human|system))?'
#                 +' *actor +(?P<name>\w+)'+end)
#             m = re.match(r, line)
#             if m:
#                 current_usecase=None
#                 name=m.group('name')
#                 current_actor=_ensureActor(name)
#                 current_actor.kind=m.group('kind'),
#                 current_actor.lineNo=line_no
#                 current_element=current_actor
#                 current_scope='actor'
#                 continue
#
#             #--- usecase X --------------------------
#             r = begin(0)+r'usecase +(?P<name>\w+)'+end
#             m = re.match(r, line)
#             if m:
#                 current_actor=None
#                 name=m.group('name')
#                 current_usecase=_ensureUsecase(name)
#                 current_usecase.lineNo = line_no
#                 current_element=current_usecase
#                 current_scope='usecase'
#                 continue
#
#             if current_scope=='actor':
#
#                 # --- ....usecases ------------------------
#                 r = begin(1)+r'usecases'+end
#                 m = re.match(r, line)
#                 if m:
#                     current_scope='actor.usecases'
#                     continue
#
#             if current_scope=='actor.usecases':
#                 r = begin(2)+r'(?P<name>\w+)'+end
#                 m = re.match(r, line)
#                 if m:
#                     uc=_ensureUsecase(m.group('name'))
#                     current_actor.addUsecase(uc)
#                     current_element=uc
#                     uc.lineNo=line_no
#                 continue
#
#
#             LocalizedSourceIssue(
#                 sourceFile=self,
#                 level=Levels.Error,
#                 message=(
#                     'Syntax error. Line ignored.'),
#                 line=line_no
#             )
#
#         # End of file
#         line_no=len(self.sourceLines)
#        _checkSystemExist(isLast=True)


METAMODEL.registerSource(UsecaseModelSource)
