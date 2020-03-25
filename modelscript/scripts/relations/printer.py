# coding=utf-8


from typing import Optional

from modelscript.base.modelprinters import (
    ModelPrinter,
    ModelSourcePrinter,
    ModelPrinterConfig,
)
from modelscript.metamodels.relations import (
    RelationModel,
    METAMODEL
)

__all__ = [
    'RelationModelPrinter',
]

class RelationModelPrinter(ModelPrinter):

    def __init__(self,
                 theModel,
                 config=None):
        #type: (RelationModel, Optional[ModelPrinterConfig]) -> None
        super(RelationModelPrinter, self).__init__(
            theModel=theModel,
            config=config)

    def doModelContent(self):
        super(RelationModelPrinter, self).doModelContent()
        self.doRelationModel(self.theModel)
        return self.output

    def doRelationModel(self, relationModel):
        self.doModelTextBlock(relationModel.description)

        for relation in relationModel.relations:
            self.doRelation(relation)

        return self.output


    def doRelation(self, relation):
        self.outLine(
            '%s %s' %(
                self.kwd('relation'),
                relation.name),
        )
        self.doModelTextBlock(relation.description)
        return self.output


METAMODEL.registerModelPrinter(RelationModelPrinter)
METAMODEL.registerSourcePrinter(ModelSourcePrinter)


