# coding=utf-8


from __future__ import unicode_literals, print_function, absolute_import, division
from typing import Text, Union, Optional
import os

from modelscripts.megamodels.models import Model, Placeholder
from modelscripts.base.grammars import (
    # ModelSourceAST, \
    # ASTBasedModelSourceFile,
    ASTNodeSourceIssue
)
from modelscripts.base.issues import (
    Levels,
)
from modelscripts.metamodels.scenarios import (
    ScenarioModel,
    METAMODEL
)
from modelscripts.metamodels.classes import (
    ClassModel
)
from modelscripts.metamodels.usecases import (
    UsecaseModel
)
from modelscripts.metamodels.glossaries import (
    GlossaryModel
)
from modelscripts.metamodels.permissions import (
    PermissionModel
)
from modelscripts.megamodels.sources import (
    ASTBasedModelSourceFile
)
from modelscripts.megamodels.metamodels import Metamodel
from modelscripts.scripts.textblocks.parser import (
    astTextBlockToTextBlock
)

__all__=(
    'ObjectModelSource'
)


DEBUG=0


ISSUES={
    # 'OBJECT_NO_CLASS':'o.res.Object.NoClass',
}
def icode(ilabel):
    return ISSUES[ilabel]

class ScenarioEvaluationModelSource(ASTBasedModelSourceFile):

    def __init__(self, fileName):
        #type: (Text) -> None
        this_dir=os.path.dirname(os.path.realpath(__file__))
        super(ScenarioEvaluationModelSource, self).__init__(
            fileName=fileName,
            grammarFile=os.path.join(this_dir, 'grammar.tx')
        )

    @property
    def scenarioModel(self):
        #type: () -> ScenarioModel
        # usefull for typing checking
        m=self.model #type: ScenarioModel
        return m

    @property
    def classModel(self):
        #type: () -> Optional[ClassModel]
        # TODO: the optional stuff should come from metamdel
        return self.importBox.model('cl', optional='True')

    @property
    def usecaseModel(self):
        #type: () -> Optional[UsecaseModel]
        # TODO: the optional stuff should come from metamdel
        return self.importBox.model('us', optional='True')

    @property
    def glossaryModel(self):
        # TODO: the optional stuff should come from metamdel
        #type: () -> Optional[GlossaryModel]
        return self.importBox.model('gl', optional='True')

    @property
    def permissionModel(self):
        #type: () -> Optional[PermissionModel]
        # TODO: the optional stuff should come from metamdel
        return self.importBox.model('pe', optional='True')


    @property
    def metamodel(self):
        return METAMODEL

    def fillModel(self):
        pass

    def resolve(self):
        pass

METAMODEL.registerSource(ScenarioEvaluationModelSource)