# coding=utf-8

from __future__ import print_function
from typing import Text
import os

from modelscripts.base.grammars import (
    # ModelSourceAST, \
    # ASTBasedModelSourceFile,
    ASTNodeSourceIssue
)
from modelscripts.base.issues import (
    Levels,
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

__all__=(
    'ClassModelSource'
)


DEBUG=0

ISSUES={
    'CLASS_NO_SUPER':'cl.syn.Class.NoSuper',
}

def icode(ilabel):
    return ISSUES[ilabel]


class _Placeholder(object):
    """
    Used just to put some symbol value in the metamodel
    waiting for symbol resolution. this will be replaced
    by an actual reference to a model element.
    """
    def __init__(self, value):
        self.value=value


class ClassModelSource(ASTBasedModelSourceFile):

    def __init__(self, usecaseFileName):
        #type: (Text) -> None
        this_dir=os.path.dirname(os.path.realpath(__file__))
        super(ClassModelSource, self).__init__(
            fileName=usecaseFileName,
            grammarFile=os.path.join(this_dir, 'grammar.tx')
        )
        self.registerBasicDataTypes()


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

        def define_datatype(ast_datatype):
            d=DataType(
                name=ast_datatype.name,
                model=self.model,
                astNode=ast_datatype
            )
            d.description=astTextBlockToTextBlock(
                container=d,
                astTextBlock=ast_datatype.textBlock)

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

        # TODO: add a check to avoid duplicate nams
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

        def define_class(ast_class):
            c=Class(
                name=ast_class.name,
                model=self.model,
                astNode=ast_class,
                isAbstract=ast_class.isAbstract,
                superclasses=[
                    _Placeholder(s) for s in ast_class.superclasses]
            )
            print('AA'*10, 'Adding class %s' %c )
            print('AA',self.classModel.classes)
            c.description=astTextBlockToTextBlock(
                container=c,
                astTextBlock=ast_class.textBlock)


            # attributes
            ast_ac=ast_class.attributeCompartment
            if ast_ac is not None:
                for ast_att in ast_ac.attributes:
                    define_attribute(c, ast_att)

        def define_attribute(class_, ast_attribute):
            # TODO: implement isOptional, isInit
            # TODO: implement isId, readonly,
            a=Attribute(
                name=ast_attribute.name,
                class_=class_,
                astNode=ast_attribute,
                isDerived=ast_attribute.isDerived,
            )
            # TODO: convert visibiliy + to public, etc.
            a.description=astTextBlockToTextBlock(
                container=class_,
                astTextBlock=ast_attribute.textBlock)


        def define_association(declaration):
            pass

        def define_invariant(declaration):
            pass

        for declaration in self.ast.model.declarations:
            # pass
            type_=declaration.__class__.__name__
            print(type_)
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

            # if type_=='Actor':

            # elif type_=='Usecase':
            #     usecase_decl=declaration
            #     u=_ensureUsecase(
            #         name=usecase_decl.name,
            #         astnode=usecase_decl,
            #         implicit=False)
            #     u.description=astTextBlockToTextBlock(
            #         container=u,
            #         astTextBlock=usecase_decl.textBlock)
            #
            # elif type_=='Interactions':
            #     for interaction in declaration.interactions:
            #         a=_ensureActor(
            #             interaction.actor,
            #             astnode=interaction,
            #             implicit=True)
            #         u=_ensureUsecase(
            #             interaction.usecase,
            #             astnode=interaction,
            #             implicit=True)
            #         a.addUsecase(u)
            # else:
            #     raise NotImplementedError(
            #         'Unexpected type %s' % type_)

    def resolve(self):

        def resolve_class_content(class_):
            actual_super_classes=[]
            print('NN'*10, "resolving class", class_, type(class_))
            for class_placeholder in class_.superclasses:
                name=class_placeholder.value
                print('NN'*20, 'processing %s in %s' %(name,class_.name) )
                try:
                    c=self.classModel._findClassOrAssociationClass(name)
                    actual_super_classes.append(c)
                except:
                    ASTNodeSourceIssue(
                        code=icode('CLASS_NO_SUPER'),
                        astNode=class_.astNode,
                        level=Levels.Error,
                        message=(
                            'Class "%s" does not exist as a superclass of %s'
                            % (name, class_.name))
                    )
            class_.superclasses=actual_super_classes
            print('SS'*10,'after:',class_.superclasses)


        print('XX'*10,'resolving',self.classModel.classes)
        for c in self.classModel.classes:
            resolve_class_content(c)


            # resolve class attributes
        #     for a in class_.attributes:
        #         __resolveAttribute(a)
        #     # resolve class operations
        #     for op in class_.operations:
        #         __resolveOperation(op)
        # pass
        # def resolve_super_actors():
        #     names_defined = self.classModel.actorNamed
        #     for actor in self.classModel.actors:
        #         for (isa, sa_name) in enumerate(
        #                 actor.superActors):
        #             # try to solve the superactor name
        #
        #             if sa_name in names_defined:
        #                 super_actor = names_defined[sa_name]
        #                 # replace the string the by the actor
        #                 actor.superActors[isa] = super_actor
        #             else:
        #                 ASTNodeSourceIssue(
        #                     code=icode('ACTOR_NO_SUPER'),
        #                     astNode=actor.astnode,
        #                     level=Levels.Error,
        #                     message=(
        #                         'Super actor %s is not defined' % (
        #                             sa_name))
        #                 )
        #                 del actor.superActors[isa]
        #
        # super(ClassModelSource, self).resolve()
        # resolve_super_actors()




    def registerBasicDataTypes(self):
        DATATYPES='Integer Boolean Real String Date DateTime Time'
        for name in DATATYPES.split(' '):
            DataType(
                model=self.model,
                name=name,
                astNode=None,
                package=None
            )







METAMODEL.registerSource(ClassModelSource)