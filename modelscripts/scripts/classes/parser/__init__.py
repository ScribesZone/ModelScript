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
    METAMODEL
)
from modelscripts.metamodels.classes.assocclasses import (
    AssociationClass)
from modelscripts.metamodels.classes.associations import (
    PlainAssociation,
    Role)
from modelscripts.metamodels.classes.classes import (
    PlainClass,
    Attribute)
from modelscripts.metamodels.classes.types import (
    DataType,
    AttributeType,
    Enumeration,
    EnumerationLiteral)
from modelscripts.metamodels.classes.invariants import (
    Invariant,
    OCLInvariant,
    OCLContext,
    OCLLine)
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
    'NO_COMPO': 'cl.syn.Association.NoCompo',
    'NO_AGGREG': 'cl.syn.Association.NotAggreg',
    'NO_ABSTRACT': 'cl.syn.Association.NoAbstract',
    'NO_ATT': 'cl.syn.Association.NoAttribute',
    'NO_OP': 'cl.syn.Association.NoOperation',
    'NO_SUPER': 'cl.syn.Association.NoSuper',
    'NO_ATT_ROLE': 'cl.syn.Association.AttRole',

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
            p=self.classModel.package(full_name)
            if p is not None:
                # package already exists : reuse it
                print('AA'*10,'reuse')
                self.__current_package=p
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
                c=PlainClass(
                    name=ast_class.name,
                    model=self.model,
                    astNode=ast_class,
                    isAbstract=ast_class.isAbstract,
                    superclasses=[
                        Placeholder(s, 'Classifier')
                        for s in ast_class.superclasses],
                    package=self.__current_package)
                c.description=astTextBlockToTextBlock(
                    container=c,
                    astTextBlock=ast_class.textBlock)

                # attributes
                ast_ac=ast_class.attributeCompartment
                if ast_ac is not None:
                    for ast_att in ast_ac.attributes:
                        define_attribute(c, ast_att)

        def define_attribute(class_, ast_attribute):
            owned_names=class_.ownedAttributeNames
            if ast_attribute.name in owned_names:
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
                is_optional=ast_attribute.isOptional is not None
                # The fact that the type is optional will come
                # later at resolution time.
                a=Attribute(
                    name=ast_attribute.name,
                    class_=class_,
                    astNode=ast_attribute,
                    visibility=visibility,
                    isDerived=is_derived,
                    type=Placeholder((ast_attribute.type),'Classifier'),
                    tags=tags,
                    stereotypes=stereotypes,
                    isOptional=is_optional
                )
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
                kind=ast_association.kind
                # could be 'association', 'composition',
                #          'aggregation' but not 'associationclass'
                a=PlainAssociation(
                    name=ast_association.name,
                    model=self.classModel,
                    astNode=ast_association,
                    kind=kind,
                    package=self.__current_package
                )
                a.description = astTextBlockToTextBlock(
                    container=a,
                    astTextBlock=ast_association.textBlock)
                define_role(a, ast_association.roleCompartment.source)
                define_role(a, ast_association.roleCompartment.target)
                if ast_association.isAbstract:
                    ASTNodeSourceIssue(
                        code=icode('NO_ABSTRACT'),
                        astNode=ast_association,
                        level=Levels.Warning,
                        message=(
                            'A %s cannot be "abstract". Ignored ' %
                            kind))
                if ast_association.attributeCompartment:
                    ASTNodeSourceIssue(
                        code=icode('NO_ATT'),
                        astNode=ast_association,
                        level=Levels.Error,
                        message=(
                            'A %s cannot be have attributes. Ignored.' %
                            kind))
                if ast_association.superclasses:
                    ASTNodeSourceIssue(
                        code=icode('NO_SUPER'),
                        astNode=ast_association,
                        level=Levels.Error,
                        message=(
                            'A %s cannot be have superclasses.'
                            ' Ignored.' %
                            kind))
                if ast_association.operationCompartment:
                    ASTNodeSourceIssue(
                        code=icode('NO_OP'),
                        astNode=ast_association,
                        level=Levels.Error,
                        message=(
                            'A %s cannot be have operations. Ignored.' %
                            kind))
                if kind=='composition':
                    ASTNodeSourceIssue(
                        code=icode('NO_COMPO'),
                        astNode=ast_association,
                        level=Levels.Warning,
                        message=(
                            'Composition not implemented yet. '
                            'Replaced by "association".'))
                if kind=='aggregation':
                    ASTNodeSourceIssue(
                        code=icode('NO_AGGREG'),
                        astNode=ast_association,
                        level=Levels.Warning,
                        message=(
                            'Aggregation not implemented yet. '
                            'Replaced by "association".'))

        def define_association_class(ast_association):
            if check_if_global_name(
                    ast_association.name,
                    ast_association,
                    'Association class ignored.' ):
                pass
            else:
                a=AssociationClass(
                    name=ast_association.name,
                    model=self.classModel,
                    isAbstract=ast_association.isAbstract,
                    superclasses=[
                        Placeholder(s, 'Classifier')
                        for s in ast_association.superclasses],
                    package=self.__current_package,
                    astNode=ast_association
                )
                a.description = astTextBlockToTextBlock(
                    container=a,
                    astTextBlock=ast_association.textBlock)
                define_role(a, ast_association.roleCompartment.source)
                define_role(a, ast_association.roleCompartment.target)

                # attributes
                ast_ac=ast_association.attributeCompartment
                if ast_ac is not None:
                    for ast_att in ast_ac.attributes:
                        # check that attributes have diffrent
                        # names that roles
                        if ast_att.name in a.roleNames:
                            ASTNodeSourceIssue(
                                code=icode('NO_ATT_ROLE'),
                                astNode=ast_att,
                                level=Levels.Error,
                                message=(
                                    'Attribute "%s" already defined '
                                    'as role.'
                                    % (ast_att.name)))
                        define_attribute(a, ast_att)

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

        def define_invariant(ast_invariant):

            def recursive_add_ocl_lines(ocl_inv, ast_ocl_line):
                # For some strange reason the textLine can
                # be None. This is due to the parser.
                # Just filter out these cases.
                if ast_ocl_line.textLine is not None:
                    OCLLine(
                        oclInvariant=ocl_inv,
                        textLine=str(ast_ocl_line.textLine),
                        astNode=ast_ocl_line
                    )
                for ast_sublines in ast_ocl_line.oclLines:
                    recursive_add_ocl_lines(ocl_inv, ast_sublines)

            #-- fill scopeItems
            if ast_invariant.scope is None:
                scopeItems=[]
            else:
                scopeItems=[]
                #TODO:3 deal with item.derived to support derived
                for item in ast_invariant.scope.items:
                    scopeItems.append(
                        (item.entity, item.member))

            #-- fill invariant
            inv=Invariant(
                name=ast_invariant.name,
                model=self.classModel,
                derivedItem=None, #TODO:3 fill with proper values
                scopeItems=scopeItems,
                astNode=ast_invariant)
            inv.description = astTextBlockToTextBlock(
                container=inv,
                astTextBlock=ast_invariant.textBlock)
            #-- fill invariant lines
            for ast_ocl_inv in ast_invariant.oclInvariants:
                ocl_inv=OCLInvariant(
                    invariant=inv,
                    astNode=ast_ocl_inv
                )
                OCLContext(
                    invariant=ocl_inv,
                    class_=ast_ocl_inv.oclContext.class_,
                    astNode=ast_ocl_inv.oclContext)
                for ast_ocl_line in ast_ocl_inv.oclLines:
                    recursive_add_ocl_lines(ocl_inv, ast_ocl_line)

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
            elif (type_=='Association'
                  and declaration.kind!='associationclass'):
                define_association(declaration)
            elif (type_=='Association'
                  and declaration.kind=='associationclass'):
                define_association_class(declaration)
            elif type_=='Invariant':
                define_invariant(declaration)
            else:
                raise NotImplementedError(
                    'declaration of %s not implemented' % type_)

    #----------------------------------------------------------------
    #                          Resolution
    #----------------------------------------------------------------

    def resolve(self):


        def resolve_class_content(classifier):
            # Works both for plainClass and associationClass

            def resolve_superclasses():
                actual_super_classes=[]
                for class_placeholder in classifier.superclasses:
                    name=class_placeholder.placeholderValue
                    c=self.classModel.class_(name)
                    if c is not None:
                        actual_super_classes.append(c)
                    else:
                        ASTNodeSourceIssue(
                            code=icode('CLASS_NO_SUPER'),
                            astNode=classifier.astNode,
                            level=Levels.Error,
                            message=(
                                'Class "%s" does not exist. '
                                "'Can't be the superclass of %s."
                                % (name, classifier.name)))
                classifier.superclasses=actual_super_classes

            def resolve_owned_attribute(attribute):
                type_name=attribute.type.placeholderValue
                if type_name in self.classModel.simpleTypeNamed:
                    simple_type=(
                        self.classModel.simpleTypeNamed[type_name])
                    att_type=AttributeType(
                        simpleType=simple_type,
                        isOptional=attribute.isOptional
                    )
                    attribute.type=att_type
                else:
                    ASTNodeSourceIssue(
                        code=icode('ATTRIBUTE_NO_TYPE'),
                        astNode=classifier.astNode,
                        level=Levels.Fatal,
                        message=(
                            'Datatype "%s" does not exist.'
                            % (type_name)))
            resolve_superclasses()
            for a in classifier.ownedAttributes:
                resolve_owned_attribute(a)

        def resolve_association_content(association):

            def resolve_role(role):
                #type: (Role) -> None
                c=self.classModel.class_(role.type.placeholderValue)
                if c is not None:
                    role.type=c
                else:
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

        # association classes are both in .classes and .associations
        # so they will be processed twice. First as classes and
        # then as associations.

        def resolve_invariant_content(invariant):
            pass # TODO:2 Resolve invariant part of class

        for c in self.classModel.classes:
            resolve_class_content(c)

        for a in self.classModel.associations:
            resolve_association_content(a)

        for i in self.classModel.invariants:
            resolve_invariant_content(i)

METAMODEL.registerSource(ClassModelSource)