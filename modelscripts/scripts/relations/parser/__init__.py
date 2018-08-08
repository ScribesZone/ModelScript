# coding=utf-8

from __future__ import (
    unicode_literals, print_function, absolute_import, division
)

import os

from typing import Text

from modelscripts.base.grammars import (
    # ModelSourceAST, \
    # ASTBasedModelSourceFile,
    ASTNodeSourceIssue
)
from modelscripts.base.issues import (
    Levels,
)
from modelscripts.metamodels.relations import (
    RelationModel,
    Relation,
    Column,
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
    'RelationModelSource'
)

#TODO:3 the name of the model is set to ''
#       it should be set to the name of the file
#       and this should be done in ModelOldSourceFile (???)

DEBUG=0

ISSUES={
    # 'ACTOR_TWICE':'us.syn.Actor.Twice',
    # 'ACTOR_NO_SUPER':'us.syn.Actor.NoSuper',
    # 'USECASE_TWICE': 'us.syn.Usecase.Twice'
}

def icode(ilabel):
    return ISSUES[ilabel]


class RelationModelSource(ASTBasedModelSourceFile):

    def __init__(self, relationFileName):
        #type: (Text) -> None
        this_dir=os.path.dirname(os.path.realpath(__file__))
        super(RelationModelSource, self).__init__(
            fileName=relationFileName,
            grammarFile=os.path.join(this_dir, 'grammar.tx')
        )


    @property
    def relationModel(self):
        #type: () -> RelationModel
        m=self.model #type: RelationModel
        return m


    @property
    def metamodel(self):
        #type: () -> Metamodel
        return METAMODEL


    def fillModel(self):

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
        pass





METAMODEL.registerSource(RelationModelSource)
