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
from modelscripts.metamodels.participants import (
    METAMODEL,
    ParticipantModel,)
from modelscripts.megamodels.metamodels import Metamodel
from modelscripts.megamodels.sources import (
    ASTBasedModelSourceFile)
from modelscripts.scripts.textblocks.parser import (
    astTextBlockToTextBlock)
from modelscripts.base.exceptions import (
    UnexpectedCase)

__all__=(
    'ParticipantModelSource'
)


DEBUG=0

ISSUES={
    # 'ACTOR_TWICE':'us.syn.Actor.Twice',
    # 'ACTOR_NO_SUPER':'us.syn.Actor.NoSuper',
    # 'USECASE_TWICE': 'us.syn.Usecase.Twice'
}

def icode(ilabel):
    return ISSUES[ilabel]


class ParticipantModelSource(ASTBasedModelSourceFile):

    def __init__(self, relationFileName):
        #type: (Text) -> None
        this_dir=os.path.dirname(os.path.realpath(__file__))
        super(ParticipantModelSource, self).__init__(
            fileName=relationFileName,
            grammarFile=os.path.join(this_dir, 'grammar.tx')
        )


    @property
    def participantModel(self):
        #type: () -> ParticipantModel
        m=self.model #type: ParticipantModel
        return m


    @property
    def metamodel(self):
        #type: () -> Metamodel
        return METAMODEL

    def fillModel(self):
        pass

    def resolve(self):
        super(ParticipantModelSource, self).resolve()





METAMODEL.registerSource(ParticipantModelSource)
