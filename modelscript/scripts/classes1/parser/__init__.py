# coding=utf-8

from __future__ import (
    unicode_literals, print_function, absolute_import, division)

import os
from typing import Text
from modelscript.base.grammars import (
    # ModelSourceAST, \
    # ASTBasedModelSourceFile,
    ASTNodeSourceIssue)
from modelscript.base.issues import (
    Levels)
from modelscript.metamodels.classes1 import (
    METAMODEL,
    Class1Model,)
from modelscript.megamodels.metamodels import Metamodel
from modelscript.megamodels.sources import (
    ASTBasedModelSourceFile)
from modelscript.scripts.textblocks.parser import (
    astTextBlockToTextBlock)
from modelscript.base.exceptions import (
    UnexpectedCase)

__all__=(
    'Class1ModelSource'
)


DEBUG=0

ISSUES={
    # 'ACTOR_TWICE':'us.syn.Actor.Twice',
    # 'ACTOR_NO_SUPER':'us.syn.Actor.NoSuper',
    # 'USECASE_TWICE': 'us.syn.Usecase.Twice'
}

def icode(ilabel):
    return ISSUES[ilabel]


class Class1ModelSource(ASTBasedModelSourceFile):

    def __init__(self, class1FileName):
        #type: (Text) -> None
        this_dir=os.path.dirname(os.path.realpath(__file__))
        super(Class1ModelSource, self).__init__(
            fileName=class1FileName,
            grammarFile=os.path.join(this_dir, 'grammar.tx')
        )


    @property
    def class1Model(self):
        #type: () -> Class1Model
        m=self.model #type: Class1Model
        return m


    @property
    def metamodel(self):
        #type: () -> Metamodel
        return METAMODEL

    def fillModel(self):
        pass

    def resolve(self):
        super(Class1ModelSource, self).resolve()





METAMODEL.registerSource(Class1ModelSource)
