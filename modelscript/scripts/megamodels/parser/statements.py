from abc import ABCMeta
from typing import Text, List, Optional

from modelscript.megamodels.metamodels import (
    Metamodel
)

ModelSourceFile='ModelOldSourceFile'
ASTNode='ASTNode'

class MegamodelStatement(object):
    __metaclass__ = ABCMeta
    def __init__(self,
                 astNode,
                 metamodel,
                 modelSourceFile):
        # type: ('ASTNode', Metamodel, ModelSourceFile) -> None
        #self.astNode,
        self.astNode=astNode
        self.metamodel=metamodel
        self.modelSourceFile=modelSourceFile


class ImportStatement(MegamodelStatement):
    def __init__(self,
                 astNode,
                 modelSourceFile,
                 metamodel,
                 modifier,
                 absoluteTargetFilename,
                 literalTargetFileName):
        # type: (ASTNode, ModelSourceFile, Metamodel, Text, Text, Text) -> None
        super(ImportStatement, self).__init__(
            astNode=astNode,
            metamodel=metamodel,
            modelSourceFile=modelSourceFile)
        self.modifier=modifier,
        self.literalTargetFileName=literalTargetFileName
        self.absoluteTargetFilename=absoluteTargetFilename

    @property
    def lineNo(self):
        from modelscript.base.grammars import AST
        return AST.nodeLine(self.astNode)

    def __str__(self):
        return "%s %s model from '%s'" % (
            self.modifier,
            self.metamodel.label,
            self.literalTargetFileName
        )

    def __repr__(self):
        from modelscript.base.grammars import (AST)
        return '%s:%i: import %s model from "%s"' % (
            AST.ast(self.astNode).basename,
            AST.nodeLine(self.astNode),
            self.metamodel.label,
            self.literalTargetFileName
        )


class DefinitionStatement(MegamodelStatement):
    def __init__(self,
                 astNode,
                 metamodel,
                 modelSourceFile,
                 modelName,
                 modelKinds,
                 modelDescription):
        #type: ('ASTNode',  Metamodel, Text, Optional[Text], List[Text],'TextBlock') -> None
        super(DefinitionStatement, self).__init__(
            astNode=astNode,
            metamodel=metamodel,
            modelSourceFile=modelSourceFile)
        self.modelName=modelName
        self.modelKinds=modelKinds
        self.modelDescription=modelDescription
