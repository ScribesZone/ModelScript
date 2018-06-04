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
    'SLOT_NO_ATTRIBUTE':'o.res.Slot.NoAttribute',
    'LINK_NO_OBJECT':'o.syn.Link.NoObject'
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

        def define_plain_object(ast_node, name, class_name):
            #type: ('ASTNode', Text, Text) -> None
            #TODO: check that this name is not duplicated
            o=PlainObject(
                model=self.objectModel,
                name=name,
                class_=Placeholder(class_name, 'Class'),
                package=None,
                astNode=ast_node)
            o.description = astTextBlockToTextBlock(
                container=o,
                astTextBlock=ast_node.textBlock)

        def define_slot(ast_node, object_name, attribute_name, value):
            #type: ('ASTNode', Text, Text, BasicValue) -> None
            print('ZZ' * 10, 'define', object_name, attribute_name, value)
            if object_name not in self.objectModel._objectNamed:
                ASTNodeSourceIssue(
                    code=icode('SLOT_NO_OBJECT'),
                    astNode=ast_node,
                    level=Levels.Error,
                    message=(
                        'Object "%s" does not exist.'
                        ' Attribute ignored.' % (
                            object_name)))
            else:
                object=self.objectModel._objectNamed[object_name]
                s=Slot(
                    object=object,
                    attribute=Placeholder(attribute_name, 'Attribute'),
                    value=value,
                    astNode=ast_node
                )
                s.description = astTextBlockToTextBlock(
                    container=s,
                    astTextBlock=ast_node.textBlock)
                print('ZZ'*10, s)

        def define_link(ast_node,
                        source_name, target_name, association_name):

            def is_object_name_defined(object_name):
                if object_name not in self.objectModel._objectNamed:
                    ASTNodeSourceIssue(
                        code=icode('SLOT_NO_OBJECT'),
                        astNode=ast_node,
                        level=Levels.Error,
                        message=(
                            'Object "%s" does not exist.'
                            ' Link ignored.' % (
                                object_name)))
                    return False
                else:
                    return True

            if (    is_object_name_defined(source_name)
                and is_object_name_defined(target_name)):
                source_object=self.objectModel._objectNamed[source_name]
                target_object=self.objectModel._objectNamed[target_name]
                l=Link(
                    model=self.objectModel,
                    name=None,
                    package=None,
                    association=Placeholder(association_name, 'Association'),
                    sourceObject=source_object,
                    targetObject=target_object,
                    astNode=ast_node)
                l.description = astTextBlockToTextBlock(
                    container=l,
                    astTextBlock=ast_node.textBlock)


        for declaration in self.ast.model.declarations:
            # pass
            type_=declaration.__class__.__name__
            print('XX'*10, 'Declaring %s' % type_)
            if type_ in ['SymbolicObjectDeclaration',
                        'SpeechObjectDeclaration']:
                define_plain_object(
                    ast_node=declaration,
                    name=declaration.name,
                    class_name=declaration.type)
            elif type_ in ['SymbolicSlotDeclaration',
                           'SpeechSlotDeclaration']:
                define_slot(
                    ast_node=declaration,
                    object_name=declaration.object,
                    attribute_name=declaration.attribute,
                    value=declaration.value)
            elif type_ in ['SpeechLinkDeclaration',
                           'SymbolicLinkDeclaration']:
                define_link(
                    ast_node=declaration,
                    source_name=declaration.source,
                    target_name=declaration.target,
                    association_name=declaration.association
                )
            else:
                raise NotImplementedError(
                    'declaration of %s not implemented' % type_)

    def resolve(self):

        def resolve_object_content(object):

            def resolve_object_class():
                name=object.class_.placeholderValue
                print('LL' * 10, 'resolving', object, name)
                if name not in self.classModel.classNamed:
                    ASTNodeSourceIssue(
                        code=icode('OBJECT_NO_CLASS'),
                        astNode=object.astNode,
                        level=Levels.Error,
                        message=(
                            'Class "%s" does not exist. Object ignored.'
                            % name))
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

            resolve_object_class()
            for slot in object.slots:
                resolve_slot_attribute(slot)

        def resolve_link_content(link):

            def resolve_link_association():
                name=link.association.placeholderValue
                if name not in self.classModel.associationNamed:
                    ASTNodeSourceIssue(
                        code=icode('OBJECT_NO_CLASS'),
                        astNode=link.astNode,
                        level=Levels.Error,
                        message=(
                            'Association "%s" does not exist.'
                            ' Link ignored ' % name))
                else:
                    # TODO: check that the association is compatible
                    #       with the class of the objects
                    link.association=(
                        self.classModel.associationNamed[name])

            resolve_link_association()

        print('SS'*10, self.objectModel.objects)
        for o in self.objectModel.objects:
            print('LL' * 10, 'resolving', o)
            resolve_object_content(o)
        for l in self.objectModel.links:
            resolve_link_content(l)

METAMODEL.registerSource(ObjectModelSource)
