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
    Package,
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
    'GNAME_TWICE': 'cl.syn.GlobalName.Twice',
    'ENUMLIT_TWICE': 'cl.syn.EnumLit.Twice',
    'ATT_DEFINED': 'cl.syn.Attribute.Defined',
    'ROLE_DEFINED': 'cl.syn.Role.Defined',
    'CARDINALITY_ERROR': 'cl.syn.Cardinality.Error',

    'CLASS_NO_SUPER':'cl.res.Class.NoSuper',
    'ATTRIBUTE_NO_TYPE':'cl.res.Attribute.NoType',
    'ROLE_NO_CLASS':'cl.res.Role.NoClass',
}

def icode(ilabel):
    return ISSUES[ilabel]


class ClassModelSource(ASTBasedModelSourceFile):

    def __init__(self, fileName):
        #type: (Text) -> None
        this_dir=os.path.dirname(os.path.realpath(__file__))

        # used just during parsing to have a class level access to
        # the current package.


        super(ClassModelSource, self).__init__(
            fileName=fileName,
            grammarFile=os.path.join(this_dir, 'grammar.tx')
        )

        # used just during parsing to have a class level access to
        # the current package.
        self.__current_package = None


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

        def define_package(ast_package):
            full_name='.'.join(ast_package.names)
            if full_name in self.classModel.packageNamed:
                # package already exists : reuse it
                print('AA'*10,'reuse')
                self.__current_package=\
                    self.classModel.packageNamed[full_name]
            else:
                if len(ast_package.names)==0:
                    # this case must not exist anyway since
                    # the default package is create at the beginning.
                    pass
                    print('BB'*10,'!!!')

                else:
                    if check_if_global_name(
                            ast_package.names[0],
                            ast_package,
                            'Package ignored.'):
                        # the first name of the package is already
                        # defined in the model. Just ignore the package
                        pass
                        print('CC'*10,'!!!')

                    else:
                        # define the new package
                        print('DD'*10,'new', full_name)

                        self.__current_package=\
                            Package(
                                name=full_name,
                                model=self.classModel)

        def check_if_global_name(name, ast_node, message):
            if name in self.classModel.globalNames():
                ASTNodeSourceIssue(
                    code=icode('GNAME_TWICE'),
                    astNode=ast_node,
                    level=Levels.Error,
                    message=(
                        'Symbol "%s" is already defined'
                        ' in class model. %s' % (
                            name,
                            message
                        )))
                return True
            else:
                return False

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
                        'Wrong cardinality "[%s..%s]".'
                        % (ast_cardinality.min,
                           ast_cardinality.max)))
            return (
                min,
                max if max!='*' else None)

        def define_datatype(ast_datatype):
            if check_if_global_name(
                    ast_datatype.name,
                    ast_datatype,
                    'Datatype ignored.' ):
                pass
            else:
                print('ZZ'*10, self.__current_package, type(self.__current_package))
                d=DataType(
                    name=ast_datatype.name,
                    model=self.model,
                    package=self.__current_package,
                    astNode=ast_datatype
                )
                d.description=astTextBlockToTextBlock(
                    container=d,
                    astTextBlock=ast_datatype.textBlock)

        def define_enumeration(ast_enumeration):
            if check_if_global_name(
                    ast_enumeration.name,
                    ast_enumeration,
                    'Enumeration ignored.' ):
                pass
            else:
                e=Enumeration(
                    name=ast_enumeration.name,
                    model=self.model,
                    package=self.__current_package,
                    astNode=ast_enumeration)
                e.description=astTextBlockToTextBlock(
                    container=e,
                    astTextBlock=ast_enumeration.textBlock)
                for ast_el in ast_enumeration.literals:
                    define_enumeration_literal(e, ast_el)

        def define_enumeration_literal(enumeration, ast_literal):
                if ast_literal.name in enumeration.literalNames:
                    ASTNodeSourceIssue(
                        code=icode('ENUMLIT_TWICE'),
                        astNode=ast_literal,
                        level=Levels.Warning,
                        message=(
                            'Enumeration literal "%s" already defined.'
                            ' Ignored.'
                            % (ast_literal.name)))
                else:
                    el=EnumerationLiteral(
                        name=ast_literal.name,
                        enumeration=enumeration,
                        astNode=ast_literal
                    )
                    el.description=astTextBlockToTextBlock(
                        container=el,
                        astTextBlock=ast_literal.textBlock)

        def define_class(ast_class):
            if check_if_global_name(
                    ast_class.name,
                    ast_class,
                    'Class ignored.' ):
                pass
            else:
                print('ZZ'*10, self.__current_package, type(self.__current_package))
                c=Class(
                    name=ast_class.name,
                    model=self.model,
                    astNode=ast_class,
                    isAbstract=ast_class.isAbstract,
                    superclasses=[
                        Placeholder(s, 'Classifier')
                        for s in ast_class.superclasses],
                    package=self.__current_package,
                )
                c.description=astTextBlockToTextBlock(
                    container=c,
                    astTextBlock=ast_class.textBlock)

                print('CC'*10, '"', c.package,'"')

                # attributes
                ast_ac=ast_class.attributeCompartment
                if ast_ac is not None:
                    for ast_att in ast_ac.attributes:
                        define_attribute(c, ast_att)

        def define_attribute(class_, ast_attribute):
            if ast_attribute.name in class_.names:
                ASTNodeSourceIssue(
                    code=icode('ATT_DEFINED'),
                    astNode=ast_attribute,
                    level=Levels.Error,
                    message=(
                        '"%s" already defined in class "%s".'
                        ' Attribute ignored.'
                        % (ast_attribute.name, class_.name)))
            else:
                deco=ast_attribute.decorations
                if deco is None:
                    visibility='public'
                    is_derived=False
                else:
                    visibility={
                        None:'public',
                        '+':'public',
                        '-':'private',
                        '%':'protected',
                        '~':'package' } [deco.visibility]
                    is_derived=deco.isDerived is not None
                if ast_attribute.metaPart is None:
                    tags=[]
                    stereotypes=[]
                else:
                    tags=ast_attribute.metaPart.tags
                    stereotypes=ast_attribute.metaPart.stereotypes
                a=Attribute(
                    name=ast_attribute.name,
                    class_=class_,
                    astNode=ast_attribute,
                    visibility=visibility,
                    isDerived=is_derived,
                    type=Placeholder((ast_attribute.type),'Classifier'),
                    tags=tags,
                    stereotypes=stereotypes,
                    isOptional=ast_attribute.isOptional is not None
                )
                # TODO: convert visibiliy + to public, etc.
                a.description=astTextBlockToTextBlock(
                    container=class_,
                    astTextBlock=ast_attribute.textBlock)

        def define_association(ast_association):
            if check_if_global_name(
                    ast_association.name,
                    ast_association,
                    'Association ignored.' ):
                pass
            else:
                a=Association(
                    name=ast_association.name,
                    model=self.classModel,
                    astNode=ast_association,
                    kind=ast_association.kind,
                    package=self.__current_package
                )
                a.description = astTextBlockToTextBlock(
                    container=a,
                    astTextBlock=ast_association.textBlock)
                define_role(a, ast_association.roleCompartment.source)
                define_role(a, ast_association.roleCompartment.target)

        def define_role(association, ast_role):
            if ast_role.name in association.roleNames:
                ASTNodeSourceIssue(
                    code=icode('ROLE_DEFINED'),
                    astNode=ast_role,
                    level=Levels.Fatal,
                    message=(
                        'Role "%s" already defined.'
                        ' Role names must be different.'
                        % (ast_role.name)))
            else:
                (min, max)=cardinality_min_max(ast_role.cardinality)
                if ast_role.metaPart is None:
                    tags=[]
                    stereotypes=[]
                else:
                    tags=ast_role.metaPart.tags
                    stereotypes=ast_role.metaPart.stereotypes
                print('LL'*20,ast_role.name,ast_role.navigability)
                r=Role(
                    astNode=ast_role,
                    association=association,
                    name=ast_role.name,
                    type=Placeholder(ast_role.type,'Classifier'),
                    cardMin=min,
                    cardMax=max,
                    navigability=ast_role.navigability,
                    tags=tags,
                    stereotypes=stereotypes)
                r.description = astTextBlockToTextBlock(
                    container=r,
                    astTextBlock=ast_role.textBlock)

        def define_invariant(declaration):
            pass

        self.__current_package=\
            Package(
                name='',
                model=self.classModel)

        for declaration in self.ast.model.declarations:
            type_=declaration.__class__.__name__
            if type_=='Package':
                define_package(declaration)
            elif type_=='DataType':
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
            #
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
                    type=(
                        self.classModel.simpleTypeNamed[type_name])
                    # Optional : Attribute to type
                    type.isOptional=attribute.isOptional
                    attribute.type=type
                else:
                    ASTNodeSourceIssue(
                        code=icode('ATTRIBUTE_NO_TYPE'),
                        astNode=class_.astNode,
                        level=Levels.Error,
                        message=(
                            'Datatype "%s" does not exist.'
                            " Trying with 'String'."
                            % (type_name)))
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

        for c in self.classModel.classes:
            resolve_class_content(c)

        for a in self.classModel.associations:
            resolve_association_content(a)

METAMODEL.registerSource(ClassModelSource)