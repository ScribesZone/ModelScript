# coding=utf-8

from __future__ import print_function
from typing import Text
import os

from modelscripts.base.grammars import (
    # ModelSourceAST, \
    # ASTBasedModelSourceFile,
    ASTNodeSourceIssue
)
from modelscripts.base.issues import (
    Levels,
)
from modelscripts.metamodels.classes import (
    ClassModel,
    Class,
    Attribute,
    Association,
    Role,
    METAMODEL
)
from modelscripts.megamodels.metamodels import Metamodel

from modelscripts.megamodels.sources import (
    ASTBasedModelSourceFile
)
from modelscripts.scripts.textblocks.parser import (
    astTextBlockToTextBlock
)

__all__=(
    'ClassModelSource'
)


DEBUG=0

ISSUES={
    'ACTOR_TWICE':'us.syn.Actor.Twice',
    'ACTOR_NO_SUPER':'us.syn.Actor.NoSuper',
    'USECASE_TWICE': 'us.syn.Usecase.Twice'
}

def icode(ilabel):
    return ISSUES[ilabel]


class ClassModelSource(ASTBasedModelSourceFile):

    def __init__(self, usecaseFileName):
        #type: (Text) -> None
        this_dir=os.path.dirname(os.path.realpath(__file__))
        super(ClassModelSource, self).__init__(
            fileName=usecaseFileName,
            grammarFile=os.path.join(this_dir, 'grammar.tx')
        )


    @property
    def classModel(self):
        #type: () -> ClassModel
        m=self.model #type: ClassModel
        return m


    @property
    def metamodel(self):
        #type: () -> Metamodel
        return METAMODEL


    def fillModel(self):

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
                a.description=astTextBlockToTextBlock(
                    container=a,
                    astTextBlock=actor_decl.textBlock)


            elif type_=='Usecase':
                usecase_decl=declaration
                u=_ensureUsecase(
                    name=usecase_decl.name,
                    astnode=usecase_decl,
                    implicit=False)
                u.description=astTextBlockToTextBlock(
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

    def resolve(self):
        def resolve_super_actors():
            names_defined = self.classModel.actorNamed
            for actor in self.classModel.actors:
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
                        del actor.superActors[isa]

        super(ClassModelSource, self).resolve()
        resolve_super_actors()












METAMODEL.registerSource(ClassModelSource)