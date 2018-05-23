# coding=utf-8

"""
Generate a usecase model from a usecase script.
"""

from __future__ import (
    unicode_literals, print_function, absolute_import, division
)

import os

from typing import Text

from modelscripts.base.grammars import (
    ModelSourceAST, \
    ASTBasedModelSourceFile,
    ASTNodeSourceIssue
)
from modelscripts.base.issues import (
    Levels,
)
from modelscripts.metamodels.usecases import (
    UsecaseModel,
    Actor,
    Usecase,
    METAMODEL
)
from modelscripts.scripts.textblocks.parser import (
    astTextBlockToTextBlock
)

__all__=(
    'UsecaseModelSource'
)

#FIXME: the name of the model is set to ''
#       it should be set to the name of the file
#       and this should be done in ModelSourceFile

DEBUG=0

ISSUES={
    'ACTOR_TWICE':'us.syn.Actor.Twice',
    'ACTOR_NO_SUPER':'us.syn.Actor.NoSuper',
    'USECASE_TWICE': 'us.syn.Usecase.Twice'
}

def icode(ilabel):
    return ISSUES[ilabel]


class UsecaseModelSource(ASTBasedModelSourceFile):

    def __init__(self, usecaseFileName):
        #type: (Text) -> None
        this_dir=os.path.dirname(os.path.realpath(__file__))
        super(UsecaseModelSource, self).__init__(
            fileName=usecaseFileName,
            grammarFile=os.path.join(this_dir, 'grammar.tx')
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

        def _ensureActor(name, astnode, implicit):
            if name in self.usecaseModel.actorNamed:
                existing_actor=self.usecaseModel.actorNamed[name]
                if  (         not existing_actor.implicitDeclaration
                          and not implicit ):
                    ASTNodeSourceIssue(
                        code=icode('ACTOR_TWICE'),
                        astNode=astnode,
                        level=Levels.Error,
                        message=(
                             'Actor "%s" already declared at line %s' % (
                                 name,
                                 self.ast.line(existing_actor.astnode)))
                    )
                    return existing_actor
                else:
                    return existing_actor
            else:
                new_actor=Actor(
                            self.usecaseModel,
                            name=name,
                            astNode=astnode,
                            implicitDeclaration=implicit)
                return new_actor

        def _ensureUsecase(name, astnode, implicit):
            if name in (self.usecaseModel.system.usecaseNamed):
                existing_usecase=\
                    self.usecaseModel.system.usecaseNamed[name]
                if  (         not existing_usecase.implicitDeclaration
                          and not implicit ):
                    ASTNodeSourceIssue(
                        code=icode('USECASE_TWICE'),
                        astNode=astnode,
                        level=Levels.Error,
                        message=(
                             'Usecase "%s" already declared at line %s' % (
                                 name,
                                 self.ast.line(existing_usecase.astnode)))
                    )
                    return existing_usecase
                else:
                    return existing_usecase
            else:
                new_usecase=Usecase(
                    self.usecaseModel.system,
                    name=name,
                    astNode=astnode,
                    implicitDeclaration=implicit)
                return new_usecase


        if DEBUG>=1:
            print('\nParsing %s\n' % self.fileName)

        self.ast = ModelSourceAST(self.grammar, self)

        self.usecaseModel.docComment=astTextBlockToTextBlock(
            container=self.usecaseModel,
            astTextBlock=self.ast.model.testBlock)

        # self.usecaseModel.system.setInfo(
          #                  name=name   #,
                            # lineNo=line_no,
                       # )
        for declaration in self.ast.model.declarations:
            type_=declaration.__class__.__name__

            if type_=='Actor':
                actor_decl=declaration
                a=_ensureActor(
                    name=actor_decl.name,
                    astnode=actor_decl,
                    implicit=False)
                a.kind=(
                    'human' if actor_decl.kind is None
                    else actor_decl.kind)

                a.superActors=actor_decl.superActors
                a.docComment=astTextBlockToTextBlock(
                    container=a,
                    astTextBlock=actor_decl.testBlock)


            elif type_=='Usecase':
                usecase_decl=declaration
                u=_ensureUsecase(
                    name=usecase_decl.name,
                    astnode=usecase_decl,
                    implicit=False)
                u.docComment=astTextBlockToTextBlock(
                    container=u,
                    astTextBlock=usecase_decl.textBlock)

            elif type_=='Interactions':
                for interaction in declaration.interactions:
                    a=_ensureActor(
                        interaction.actor,
                        astnode=interaction,
                        implicit=True)
                    u=_ensureUsecase(
                        interaction.usecase,
                        astnode=interaction,
                        implicit=True)
                    a.addUsecase(u)
            else:
                raise NotImplementedError(
                    'Unexpected type %s' % type_)

        self._resolve()

    def _resolve(self):
        def resolve_super_actors():
            names_defined = self.usecaseModel.actorNamed
            for actor in self.usecaseModel.actors:
                for (isa, sa_name) in enumerate(
                        actor.superActors):
                    # try to solve the superactor name

                    if sa_name in names_defined:
                        super_actor = names_defined[sa_name]
                        # replace the string the by the actor
                        actor.superActors[isa] = super_actor
                    else:
                        ASTNodeSourceIssue(
                            code=icode('ACTOR_NO_SUPER'),
                            astNode=actor.astnode,
                            level=Levels.Error,
                            message=(
                                'Super actor %s is not defined' % (
                                    sa_name))
                        )
                        # #FIXME: convert this to ASTSourceIssue
                        # LocalizedSourceIssue(
                        #     sourceFile=self,
                        #     level=Levels.Error,
                        #     message=(
                        #         'Super actor %s is not defined in %s' % (
                        #             sa_name,
                        #             actor.name)),
                        #     line=self.ast.line(actor.astnode)
                        # )
                        # remove the super actor, just to continue
                        # without a fatal error
                        del actor.superActors[isa]

        resolve_super_actors()






METAMODEL.registerSource(UsecaseModelSource)
