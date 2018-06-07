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
from modelscripts.metamodels.objects import (
    ObjectModel,
    PlainObject,
    BasicValue,
    Slot,
    PlainLink,
    LinkObject,
    AnnotatedTextBlock,
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

        def define_plain_object(ast_node, name, class_name, container):
            #type: ('ASTNode', Text, Text) -> None
            #TODO: check that this name is not duplicated
            o=PlainObject(
                model=self.objectModel,
                name=name,
                class_=Placeholder(class_name, 'Class'),
                container=container,
                package=None,
                astNode=ast_node)
            o.description = astTextBlockToTextBlock(
                container=o,
                astTextBlock=ast_node.textBlock)

        def define_slot(ast_node, object_name,
                        attribute_name, value, container):
            #type: ('ASTNode', Text, Text, BasicValue) -> None
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
                    container=container,
                    astNode=ast_node
                )
                s.description = astTextBlockToTextBlock(
                    container=s,  # not the container of the slot
                    astTextBlock=ast_node.textBlock)

        def define_link(ast_node,
                        source_name, target_name,
                        association_name, container):

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
                l=PlainLink(
                    model=self.objectModel,
                    name=None,
                    package=None,
                    association=Placeholder(association_name, 'Association'),
                    sourceObject=source_object,
                    targetObject=target_object,
                    container=container,
                    astNode=ast_node)
                l.description = astTextBlockToTextBlock(
                    container=l,
                    astTextBlock=ast_node.textBlock)


        def define_annotated_text_block_body(declaration):
            # create the Annotated Text Block but
            # do not add definitions in it
            atb=AnnotatedTextBlock(
                model=self.objectModel,
                astNode=declaration
            )
            atb.textBlock=astTextBlockToTextBlock(
                    container=self.objectModel,
                    astTextBlock=declaration.textBlock)
            return atb

        def define_core_declaration(declaration, container):
            #type: ('ASTCoreOBDeclaration', Optional[AnnotatedTextBlock]) -> None
            type_=declaration.__class__.__name__
            if type_ in ['SymbolicObjectDeclaration',
                        'SpeechObjectDeclaration']:
                define_plain_object(
                    ast_node=declaration,
                    name=declaration.name,
                    class_name=declaration.type,
                    container=container)
            elif type_ in ['SymbolicSlotDeclaration',
                           'SpeechSlotDeclaration']:
                define_slot(
                    ast_node=declaration,
                    object_name=declaration.object,
                    attribute_name=declaration.attribute,
                    value=declaration.value,
                    container=container)
            elif type_ in ['SpeechLinkDeclaration',
                           'SymbolicLinkDeclaration']:
                define_link(
                    ast_node=declaration,
                    source_name=declaration.source,
                    target_name=declaration.target,
                    association_name=declaration.association,
                    container=container
                )
            else:
                raise NotImplementedError(
                    '%s is not a core definition' % type_)

        # for some strange reason body can be None = > test
        if self.ast.model.body is not None:
            for declaration in self.ast.model.body.declarations:
                # pass
                type_=declaration.__class__.__name__
                if type_ in [
                        'SymbolicObjectDeclaration',
                        'SpeechObjectDeclaration',
                        'SymbolicSlotDeclaration',
                        'SpeechSlotDeclaration',
                        'SpeechLinkDeclaration',
                        'SymbolicLinkDeclaration']:
                    define_core_declaration(declaration, container=None)
                elif type_=='ATextBlockOBDeclaration':
                    atb=define_annotated_text_block_body(declaration)
                    for sub_decl in declaration.declarations:
                        define_core_declaration(sub_decl, container=atb)
                else:
                    raise NotImplementedError(
                        'declaration of %s not implemented' % type_)

    def resolve(self):

        def resolve_object_content(object):

            def resolve_object_class():
                name=object.class_.placeholderValue
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

        for o in self.objectModel.objects:
            resolve_object_content(o)
        for l in self.objectModel.links:
            resolve_link_content(l)

METAMODEL.registerSource(ObjectModelSource)
