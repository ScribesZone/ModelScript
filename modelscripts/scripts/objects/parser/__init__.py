# coding=utf-8

from __future__ import unicode_literals, print_function, absolute_import, division
from typing import Text, Union
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
from modelscripts.metamodels.objects import (
    ObjectModel,
    Object,
    PlainObject,
    Slot,
    Link,
    PlainLink,
    LinkObject,
    METAMODEL
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
    'OBJECT_NO_CLASS':'o.res.Object.NoClass',
    'SLOT_NO_OBJECT':'o.syn.Slot.NoObject',
    'SLOT_NO_ATTRIBUTE':'o.res.Slot.NoAttribute'
}
def icode(ilabel):
    return ISSUES[ilabel]


BasicValue=Union[Text, 'Bool', int, float]

class ObjectModelSource(ASTBasedModelSourceFile):

    def __init__(self, fileName):
        #type: (Text) -> None
        this_dir=os.path.dirname(os.path.realpath(__file__))
        super(ObjectModelSource, self).__init__(
            fileName=fileName,
            grammarFile=os.path.join(this_dir, 'grammar.tx')
        )

    @property
    def objectModel(self):
        #type: () -> ObjectModel
        # usefull for typing checking
        m=self.model #type: ObjectModel
        return m

    @property
    def classModel(self):
        return self.importBox.model('cl')

    @property
    def metamodel(self):
        return METAMODEL

    def fillModel(self):

        def define_plain_object(ast_node, name, className):
            #type: ('ASTNode', Text, Text) -> None
            #TODO: check that this name is not duplicated
            o=PlainObject(
                model=self.objectModel,
                name=name,
                class_=Placeholder(className, 'Class'),
                package=None,
                astNode=ast_node)
            o.description = astTextBlockToTextBlock(
                container=o,
                astTextBlock=ast_node.textBlock)

        def define_slot(ast_node, objectName, attributeName, value):
            #type: ('ASTNode', Text, Text, BasicValue) -> None
            print('ZZ'*10, 'define',objectName, attributeName, value)
            if objectName not in self.objectModel._objectNamed:
                ASTNodeSourceIssue(
                    code=icode('SLOT_NO_OBJECT'),
                    astNode=ast_node,
                    level=Levels.Error,
                    message=(
                        'Object "%s" does not exist.'
                        ' Attribute ignored.' % (
                            objectName)))
            else:
                object=self.objectModel._objectNamed[objectName]
                s=Slot(
                    object=object,
                    attribute=Placeholder(attributeName, 'Attribute'),
                    value=value,
                    astNode=ast_node
                )
                s.description = astTextBlockToTextBlock(
                    container=s,
                    astTextBlock=ast_node.textBlock)
                print('ZZ'*10, s)

        for declaration in self.ast.model.declarations:
            # pass
            type_=declaration.__class__.__name__
            print(type_)
            if type_=='SymbolicObject':
                define_plain_object(
                    ast_node=declaration,
                    name=declaration.name,
                    className=declaration.type)
            elif type_=='SpeechObject':
                define_plain_object(
                    ast_node=declaration,
                    name=declaration.name,
                    className=declaration.type)
            elif type_=='SymbolicSlot':
                define_slot(
                    ast_node=declaration,
                    objectName=declaration.object,
                    attributeName=declaration.attribute,
                    value=declaration.value)
            elif type_=='SpeechSlot':
                define_slot(
                    ast_node=declaration,
                    objectName=declaration.object,
                    attributeName=declaration.attribute,
                    value=declaration.value)
            else:
                raise NotImplementedError(
                    'declaration of %s not implemented' % type_)

    def resolve(self):

        def resolve_plain_object_content(object):

            def resolve_object_class():
                name=object.class_.placeholderValue
                print('LL' * 10, 'resolving', object, name)
                if name not in self.classModel.classNamed:
                    ASTNodeSourceIssue(
                        code=icode('OBJECT_NO_CLASS'),
                        astNode=object.astNode,
                        level=Levels.Fatal,
                        message=(
                            'Class "%s" does not exist. ' % name))
                else:
                    object.class_=self.classModel.classNamed[name]
                    print('KK'*10, 'resolved', object.class_)

            def resolve_slot_attribute(slot):
                attribute_name=slot.attribute.placeholderValue
                class_=object.class_
                if attribute_name not in class_.attributeNamed:
                    ASTNodeSourceIssue(
                        code=icode('SLOT_NO_ATTRIBUTE'),
                        astNode=slot.astNode,
                        level=Levels.Fatal,
                        message=(
                            'Object "%s" is of type "%s" but this class'
                            ' has no attribute "%s".' % (
                                object.name,
                                class_.name,
                            attribute_name)))
                else:
                    slot.attribute=class_.attributeNamed[attribute_name]

            print('FF'*10, 'resolving object %s' % object.name)
            resolve_object_class()
            for slot in object.slots:
                resolve_slot_attribute(slot)

        print('SS'*10, self.objectModel.plainObjects)
        for po in self.objectModel.plainObjects:
            print('LL' * 10, 'resolving', po)
            resolve_plain_object_content(po)

METAMODEL.registerSource(ObjectModelSource)
