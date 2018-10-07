# coding=utf-8

from __future__ import (
    unicode_literals, print_function, absolute_import, division)

import os
from typing import Text
from modelscripts.base.grammars import (
    # ModelSourceAST, \
    # ASTBasedModelSourceFile,
    ASTNodeSourceIssue)
from modelscripts.base.issues import (
    Levels)
from modelscripts.metamodels.aui import (
    METAMODEL)
from modelscripts.metamodels.relations import (
    RelationModel,
    Relation,
    Column,)
from modelscripts.megamodels.metamodels import Metamodel
from modelscripts.megamodels.sources import (
    ASTBasedModelSourceFile)
from modelscripts.scripts.textblocks.parser import (
    astTextBlockToTextBlock)
from modelscripts.base.exceptions import (
    UnexpectedCase)

__all__=(
    'AUIModelSource'
)

#TODO:- the name of the model is set to ''
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


class AUIModelSource(ASTBasedModelSourceFile):

    def __init__(self, relationFileName):
        #type: (Text) -> None
        this_dir=os.path.dirname(os.path.realpath(__file__))
        super(AUIModelSource, self).__init__(
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
        pass

    def resolve(self):
        super(AUIModelSource, self).resolve()





METAMODEL.registerSource(AUIModelSource)
