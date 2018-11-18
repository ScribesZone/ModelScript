# coding=utf-8

from __future__ import (
    unicode_literals, print_function, absolute_import, division
)

import os

from typing import Text

from modelscript.base.grammars import (
    # ModelSourceAST, \
    # ASTBasedModelSourceFile,
    ASTNodeSourceIssue
)
from modelscript.base.issues import (
    Levels,
)
from modelscript.metamodels.relations import (
    RelationModel,
    Relation,
    Column,
    METAMODEL
)
from modelscript.megamodels.metamodels import Metamodel

from modelscript.megamodels.sources import (
    ASTBasedModelSourceFile
)
from modelscript.scripts.textblocks.parser import (
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
        pass

    def resolve(self):
        super(RelationModelSource, self).resolve()





METAMODEL.registerSource(RelationModelSource)
