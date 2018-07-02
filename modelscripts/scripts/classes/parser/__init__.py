# coding=utf-8

from __future__ import print_function
from typing import Text, Union
import os

from modelscripts.base.grammars import (
    # ModelSourceAST, \
    # ASTBasedModelSourceFile,
    ASTNodeSourceIssue
)
from modelscripts.base.issues import (
    Levels
)
from modelscripts.metamodels.classes import (
    ClassModel,
    DataType,
    Enumeration,
    EnumerationLiteral,
    Class,
    Attribute,
    Association,
    Role,
    METAMODEL
)
from modelscripts.megamodels.metamodels import Metamodel

from modelscripts.megamodels.sources import (
    ASTBasedModelSourceFile
)
from modelscripts.scripts.textblocks.parser import (
    astTextBlockToTextBlock
)
from modelscripts.megamodels.models import Model, Placeholder


__all__=(
    'ClassModelSource'
)


DEBUG=0

ISSUES={
    'CLASS_NO_SUPER':'cl.res.Class.NoSuper',
    'ATTRIBUTE_NO_TYPE':'cl.res.Attribute.NoType',
    'ROLE_NO_CLASS':'cl.res.Role.NoClass',
    'CARDINALITY_ERROR':'cl.syn.Cardinality.Error'
}

def icode(ilabel):
    return ISSUES[ilabel]


class ClassModelSource(ASTBasedModelSourceFile):

    def __init__(self, fileName):
        #type: (Text) -> None
        this_dir=os.path.dirname(os.path.realpath(__file__))
        super(ClassModelSource, self).__init__(
            fileName=fileName,
            grammarFile=os.path.join(this_dir, 'grammar.tx')
        )


    @property
    def classModel(self):
        #type: () -> ClassModel
        # usefull for typing checking
        m=self.model #type: ClassModel
        return m

    @property
    def metamodel(self):
        #type: () -> Metamodel
        return METAMODEL

    def fillModel(self):

        def cardinality_min_max(ast_cardinality):

            min=ast_cardinality.min
            max=ast_cardinality.max
            if max is None:
                # [*] -> [0..*]
                if min=='*':
                    min=0
                    max='*'
                # [x] -> [x..x]
                else:
                    max=min
            if (min=='*'
                or min < 0
                or (max != '*' and (max < min))):
                ASTNodeSourceIssue(
                    code=icode('CARDINALITY_ERROR'),
                    astNode=ast_cardinality,
                    level=Levels.Fatal,
                    message=(
                        'Malformed cardinality "[%s..%s]".'
                        % (ast_cardinality.min, ast_cardinality)))
            return (
                min,
                max if max!='*' else None)

        # TODO: add check to avoid duplicate
        def define_datatype(ast_datatype):
            d=DataType(
                name=ast_datatype.name,
                model=self.model,
                astNode=ast_datatype
            )
            d.description=astTextBlockToTextBlock(
                container=d,
                astTextBlock=ast_datatype.textBlock)

        # TODO: add check to avoid duplicate
        def define_enumeration(ast_enumeration):
            e=Enumeration(
                name=ast_enumeration.name,
                model=self.model,
                package=None,
                astNode=ast_enumeration)
            e.description=astTextBlockToTextBlock(
                container=e,
                astTextBlock=ast_enumeration.textBlock)
            for ast_el in ast_enumeration.literals:
                define_enumeration_literal(e, ast_el)

        # TODO: add a check to avoid duplicate name
        #   in global space, enumerations, etc.
        def define_enumeration_literal(enumeration, ast_literal):
                el=EnumerationLiteral(
                    name=ast_literal.name,
                    enumeration=enumeration,
                    astNode=ast_literal
                )
                el.description=astTextBlockToTextBlock(
                    container=el,
                    astTextBlock=ast_literal.textBlock)

        # TODO: add a check to avoid duplicate name
        def define_class(ast_class):
            c=Class(
                name=ast_class.name,
                model=self.model,
                astNode=ast_class,
                isAbstract=ast_class.isAbstract,
                superclasses=[
                    Placeholder(s, 'Classifier')
                    for s in ast_class.superclasses]
            )
            c.description=astTextBlockToTextBlock(
                container=c,
                astTextBlock=ast_class.textBlock)


            # attributes
            ast_ac=ast_class.attributeCompartment
            if ast_ac is not None:
                for ast_att in ast_ac.attributes:
                    define_attribute(c, ast_att)

        # TODO: add check to avoid duplicate
        def define_attribute(class_, ast_attribute):
            visibility= {
                None:'public',
                '+':'public',
                '-':'private',
                '%':'protected',
                '~':'package' } [ast_attribute.visibility]

            # TODO: implement isOptional, isInit
            # TODO: implement isId, readonly,
            a=Attribute(
                name=ast_attribute.name,
                class_=class_,
                astNode=ast_attribute,
                isDerived=ast_attribute.isDerived,
                visibility=visibility,
                type=Placeholder((ast_attribute.type),'Classifier')
            )
            # TODO: convert visibiliy + to public, etc.
            a.description=astTextBlockToTextBlock(
                container=class_,
                astTextBlock=ast_attribute.textBlock)

        # TODO: add a check to avoid duplicate name
        def define_association(ast_association):
            a=Association(
                name=ast_association.name,
                model=self.classModel,
                astNode=ast_association,
                kind=ast_association.kind
            )
            a.description = astTextBlockToTextBlock(
                container=a,
                astTextBlock=ast_association.textBlock)
            define_role(a, ast_association.roleCompartment.source)
            define_role(a, ast_association.roleCompartment.target)

        def define_role(association, ast_role):
            (min, max)=cardinality_min_max(ast_role.cardinality)
            r=Role(
                astNode=ast_role,
                association=association,
                name=ast_role.name,
                type=Placeholder(ast_role.type.name,'Classifier'),
                cardMin=min,
                cardMax=max
            )
            r.description = astTextBlockToTextBlock(
                container=r,
                astTextBlock=ast_role.textBlock)

        def define_invariant(declaration):
            pass

        for declaration in self.ast.model.declarations:
            # pass
            type_=declaration.__class__.__name__
            if type_=='DataType':
                define_datatype(declaration)
            elif type_=='Enumeration':
                define_enumeration(declaration)
            elif type_=='Class':
                define_class(declaration)
            elif type_=='Association':
                define_association(declaration)
            elif type_=='Invariant':
                define_invariant(declaration)
            else:
                raise NotImplementedError(
                    'declaration of %s not implemented' % type_)

    #----------------------------------------------------------------
    #                          Resolution
    #----------------------------------------------------------------
    def resolve(self):

        def resolve_class_content(class_):

            def resolve_superclasses():
                actual_super_classes=[]
                for class_placeholder in class_.superclasses:
                    name=class_placeholder.placeholderValue
                    try:
                        c=self.classModel._findClassOrAssociationClass(
                            name)
                        actual_super_classes.append(c)
                    except:
                        ASTNodeSourceIssue(
                            code=icode('CLASS_NO_SUPER'),
                            astNode=class_.astNode,
                            level=Levels.Error,
                            message=(
                                'Class "%s" does not exist. '
                                "'Can't be the superclass of %s."
                                % (name, class_.name)))
                class_.superclasses=actual_super_classes

            def resolve_attribute(attribute):
                type_name=attribute.type.placeholderValue

                if type_name in self.classModel.simpleTypeNamed:
                    attribute.type=(
                        self.classModel.simpleTypeNamed[type_name])
                else:
                    ASTNodeSourceIssue(
                        code=icode('ATTRIBUTE_NO_TYPE'),
                        astNode=class_.astNode,
                        level=Levels.Error,
                        message=(
                            'Datatype "%s" does not exist. '
                            "'Can't be the type of %s."
                            "Replaced by 'String'."
                            % (type_name, attribute.name)))
                    attribute.type=(
                        self.classModel.simpleTypeNamed['String'])


            resolve_superclasses()
            for a in class_.attributes:
                resolve_attribute(a)

        def resolve_association_content(association):

            def resolve_role(role):
                #type: (Role) -> None
                try:
                    c=self.classModel._findClassOrAssociationClass(
                        role.type.placeholderValue)
                    role.type=c
                except:
                    ASTNodeSourceIssue(
                        code=icode('ROLE_NO_CLASS'),
                        astNode=role.astNode,
                        level=Levels.Fatal,
                        message=(
                            'Class "%s" does not exist. '
                            "'Can't be used in the role '%s'."
                            % (role.type.placeholderValue, role.name)))

            for r in association.roles:
                resolve_role(r)

        def registerBasicDataTypes():
            DATATYPES =   'Integer Boolean Real' \
                        + ' String Date DateTime Time'
            for name in DATATYPES.split(' '):
                DataType(
                    model=self.model,
                    name=name,
                    astNode=None,
                    package=None
                )

        registerBasicDataTypes()

        for c in self.classModel.classes:
            resolve_class_content(c)

        for a in self.classModel.associations:
            resolve_association_content(a)


METAMODEL.registerSource(ClassModelSource)