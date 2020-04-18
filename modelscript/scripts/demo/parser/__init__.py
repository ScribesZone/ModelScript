# coding=utf-8
"""Parser for ClassScript"""

from typing import cast
import os

from modelscript.base.grammars import (
    ASTNodeSourceIssue)
from modelscript.base.issues import (
    Levels)
from modelscript.base.exceptions import (
    UnexpectedCase)
from modelscript.metamodels.demo import (
    DemoModel,
    Class,
    Reference,
    METAMODEL)
from modelscript.megamodels.metamodels import Metamodel
from modelscript.megamodels.sources import (
    ASTBasedModelSourceFile)
from modelscript.scripts.textblocks.parser import (
    astTextBlockToTextBlock)
from modelscript.megamodels.models import (
    Placeholder)


__all__=(
    'ClassModelSource'
)


DEBUG = 0


ISSUES = {
#    'GNAME_TWICE': 'cl.syn.GlobalName.Twice',
}


def icode(ilabel):
    return ISSUES[ilabel]


class DemoModelSource(ASTBasedModelSourceFile):

    def __init__(self, fileName: str) -> None:
        this_dir = os.path.dirname(os.path.realpath(__file__))
        super(DemoModelSource, self).__init__(
            fileName=fileName,
            grammarFile=os.path.join(this_dir, 'grammar.tx')
        )

        # Here can be initialized parser-time variables

    @property
    def demoModel(self) -> DemoModel:
        # This method is useful for type checking. The return value
        # il a ClassModel not just a Model
        m = cast(DemoModel, self.model)
        return m

    @property
    def metamodel(self) -> Metamodel:
        return METAMODEL

    def fillModel(self):

        # def define_class(ast_class):
        #     if check_if_global_name(
        #             ast_class.name,
        #             ast_class,
        #             'Class ignored.' ):
        #         pass
        #     else:
        #         c = Class(
        #             name=ast_class.name,
        #             model=self.model,
        #             astNode=ast_class,
        #             isAbstract=ast_class.isAbstract,
        #             superclasses=[
        #                 Placeholder(s, 'Classifier')
        #                 for s in ast_class.superclasses],
        #             package=self.__current_package)
        #         c.description=astTextBlockToTextBlock(
        #             container=c,
        #             astTextBlock=ast_class.textBlock)
        #
        #         # attributes
        #         ast_ac=ast_class.attributeCompartment
        #         if ast_ac is not None:
        #             for ast_att in ast_ac.attributes:
        #                 define_attribute(c, ast_att)

        # def define_reference(class_, ast_attribute):
        #     owned_names=class_.ownedAttributeNames
        #     if ast_attribute.name in owned_names:
        #         ASTNodeSourceIssue(
        #             code=icode('ATT_DEFINED'),
        #             astNode=ast_attribute,
        #             level=Levels.Error,
        #             message=(
        #                 '"%s" already defined in class "%s".'
        #                 ' Attribute ignored.'
        #                 % (ast_attribute.name, class_.name)))
        #     else:
        #         deco=ast_attribute.decorations
        #         if deco is None:
        #             visibility='public'
        #             is_derived=False
        #         else:
        #             visibility={
        #                 None:'public',
        #                 '+':'public',
        #                 '-':'private',
        #                 '#':'protected',
        #                 '~':'package' } [deco.visibility]
        #             is_derived=deco.isDerived is not None
        #         if ast_attribute.metaPart is None:
        #             tags=[]
        #             stereotypes=[]
        #         else:
        #             tags=ast_attribute.metaPart.tags
        #             stereotypes=ast_attribute.metaPart.stereotypes
        #         is_optional=ast_attribute.isOptional is not None
        #         # The fact that the type is optional will come
        #         # later at resolution time.
        #         a=Attribute(
        #             name=ast_attribute.name,
        #             class_=class_,
        #             astNode=ast_attribute,
        #             visibility=visibility,
        #             isDerived=is_derived,
        #             type=Placeholder((ast_attribute.type),'Classifier'),
        #             tags=tags,
        #             stereotypes=stereotypes,
        #             isOptional=is_optional
        #         )
        #         a.description=astTextBlockToTextBlock(
        #             container=class_,
        #             astTextBlock=ast_attribute.textBlock)
        #
        # for declaration in self.ast.model.declarations:
        #     type_ = declaration.__class__.__name__
        #     if type_ == 'Class':
        #         define_class(declaration)
        #     else:
        #         raise UnexpectedCase(  # raise:OK
        #             'declaration of %s not implemented' % type_)
        pass

    # ----------------------------------------------------------------
    #                          Resolution
    # ----------------------------------------------------------------

    def resolve(self):


        # def resolve_class_content(classifier):
        #     # Works both for plainClass and associationClass
        #
        #     def resolve_superclasses():
        #         actual_super_classes=[]
        #         for class_placeholder in classifier.superclasses:
        #             name=class_placeholder.placeholderValue
        #             c=self.classModel.class_(name)
        #             if c is not None:
        #                 actual_super_classes.append(c)
        #             else:
        #                 ASTNodeSourceIssue(
        #                     code=icode('CLASS_NO_SUPER'),
        #                     astNode=classifier.astNode,
        #                     level=Levels.Error,
        #                     message=(
        #                         'Class "%s" does not exist. '
        #                         "'Can't be the superclass of %s."
        #                         % (name, classifier.name)))
        #         classifier.superclasses=actual_super_classes
        #
        #     def resolve_owned_attribute(attribute):
        #         type_name=attribute.type.placeholderValue
        #         if type_name in self.classModel.simpleTypeNamed:
        #             simple_type=(
        #                 self.classModel.simpleTypeNamed[type_name])
        #             att_type=AttributeType(
        #                 simpleType=simple_type,
        #                 isOptional=attribute.isOptional
        #             )
        #             attribute.type=att_type
        #         else:
        #             ASTNodeSourceIssue(
        #                 code=icode('ATTRIBUTE_NO_TYPE'),
        #                 astNode=classifier.astNode,
        #                 level=Levels.Fatal,
        #                 message=(
        #                     'Datatype "%s" does not exist.'
        #                     % (type_name)))
        #     resolve_superclasses()
        #     for a in classifier.ownedAttributes:
        #         resolve_owned_attribute(a)
        #
        #
        # super(DemoModelSource, self).resolve()
        #
        # def resolve_invariant_content(invariant):
        #     pass # TODO:2 Resolve invariant part of class
        #
        # for c in self.classModel.classes:
        #     resolve_class_content(c)

        pass


METAMODEL.registerSource(DemoModelSource)
