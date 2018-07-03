# coding=utf-8

from __future__ import unicode_literals, print_function, absolute_import, division
from typing import Text, Union, List, Optional
import os

from modelscripts.megamodels.models import Model, Placeholder
from modelscripts.base.grammars import (
    ASTNodeSourceIssue
)
from modelscripts.base.issues import (
    Levels,
)
from modelscripts.scripts.textblocks.parser import (
    astTextBlockToTextBlock
)
from modelscripts.metamodels.permissions.sar import (
    Subject,
    Action,
    Resource
)
from modelscripts.metamodels.permissions import (
    METAMODEL,
    PermissionModel,
    UCPermissionModel,
    FactorizedPermissionRule,
)

from modelscripts.metamodels.classes import (
    Entity,
    ClassModel,
    Class,
    Association,
    AssociationClass,
    DataValue
)
from modelscripts.metamodels.permissions.sar import (
    Subject,
    Action,
    Resource
)
from modelscripts.metamodels.usecases import (
    UsecaseModel,
)
from modelscripts.megamodels.sources import (
    ASTBasedModelSourceFile
)


__all__=(
    'PermissionModelSource'
)


ISSUES={
    'RULE_SUBJECT_NOT_FOUND': 'pe.syn.Rule.SubjectNotFound',
    'RULE_RESOURCE_NOT_FOUND': 'pe.syn.Rule.ResourceNotFound',
    'RULE_CLASSIFIER_NOT_FOUND': 'pe.syn.Rule.ClassifierNotFound',
    'RULE_ATTRIBUTE_NOT_FOUND': 'pe.syn.Rule.AttributeNotFound',
    'RULE_ROLE_NOT_FOUND': 'pe.syn.Rule.RoleNotFound',
    'RULE_MEMBER_NOT_FOUND': 'pe.syn.Rule.MemberNotFound',
}
def icode(ilabel):
    return ISSUES[ilabel]

DEBUG=3


class PermissionModelSource(ASTBasedModelSourceFile):

    def __init__(self, fileName):
        #type: (Text) -> None
        this_dir=os.path.dirname(os.path.realpath(__file__))
        super(PermissionModelSource, self).__init__(
            fileName=fileName,
            grammarFile=os.path.join(this_dir, 'grammar.tx')
        )

    @property
    def permissionModel(self):
        #type: () -> UCPermissionModel
        # usefull for typing checking
        m=self.model #type: UCPermissionModel
        return m

    @property
    def classModel(self):
        return self.importBox.model('cl')

    @property
    def usecaseModel(self):
        return self.importBox.model('us')


    @property
    def metamodel(self):
        return METAMODEL

    def fillModel(self):

        def define_rule_declaration(declaration):
            
            def action(name):
                SHORTCUTS={
                    'C':'create',
                    'R':'read',
                    'U':'update',
                    'D':'delete',
                    'X':'execute'
                }
                if name in SHORTCUTS:
                    return Action.named(SHORTCUTS[name])
                else:
                    return Action.named(name)

            subjects=[ _find_subject(
                        usecaseModel=self.usecaseModel,
                        name=name,
                        astNode=declaration)
                    for name in declaration.subjectNames]

            actions=[action(op)
                     for op in declaration.actionNames]

            resources=[ _find_resource(
                            classModel=self.classModel,
                            expr=expr,
                            astNode=expr)
                        for expr in declaration.resourceExprs]

            fpr=FactorizedPermissionRule(
                model=self.permissionModel,
                subjects=subjects,
                actions=actions,
                resources=resources,
                astNode=declaration
            )
            fpr.description = astTextBlockToTextBlock(
                container=fpr,
                astTextBlock=declaration.textBlock)
            # TODO: change the metamodel so that the addition is automatic
            #       In other metamodels, the component is always with
            #       a reference to the composite and always add itself.
            self.permissionModel.rules.append(fpr)

        for declaration in self.ast.model.declarations:
            # pass
            type_=declaration.__class__.__name__
            print(type_)
            if type_ in ['ENSpeechRuleDeclaration',
                         'FRSpeechRuleDeclaration']:
                define_rule_declaration(declaration)
            else:
                raise NotImplementedError(
                    'declaration of %s not implemented' % type_)

    def resolve(self):
        pass


def _find_subject(usecaseModel, name, astNode):
    #type: (usecaseModel, Text, 'ASTNode')->Subject
    """
    Search the name in usecases or actors.
    Return the subject or raise a fatal issue otherwise.
    """
    if DEBUG>=2:
        print('Find_subject("%s")' %  name)
    if name in usecaseModel.actorNamed:
        return usecaseModel.actorNamed[name]
    elif name in usecaseModel.system.usecaseNamed:
        return usecaseModel.system.usecaseNamed[name]
    else:
        ASTNodeSourceIssue(
            code=icode('RULE_SUBJECT_NOT_FOUND'),
            astNode=astNode,
            level=Levels.Fatal,
            message=(
                '"%s" is neither an actor nor a usecase.'
                % name))







# # TODO: move this to metamodels.classes ?
# def _find_resource(classModel, name, astNode):
#     #type: (ClassModel, Text, 'ASTNode')->Entity
#     """ Search the name in class/association/associationclass
#     """
#     if DEBUG>=2:
#         print('Find_resource("%s")' % name)
#     if name in classModel.classNamed:
#         return classModel.classNamed[name]
#     elif name in classModel.associationNamed:
#         return classModel.associationNamed[name]
#     elif name in classModel.associationClassNamed:
#         return classModel.associationClassNamed[name]
#     else:
#         ASTNodeSourceIssue(
#             code=icode('RULE_RESOURCE_NOT_FOUND'),
#             astNode=astNode,
#             level=Levels.Fatal,
#             message=(
#                 '"%s" is neither an association, nor a class.'))
#
#
#

# TODO: move this to metamodels.classes ?
def _find_entity(classModel, name):
    #type: (ClassModel, Text)->Optional[Entity]
    """ Search the name in class/association/associationclass
    """
    if DEBUG>=2:
        print('resolve_entity "%s"' % name)
    if name in classModel.classNamed:
        return classModel.classNamed[name]
    elif name in classModel.associationNamed:
        return classModel.associationNamed[name]
    elif name in classModel.associationClassNamed:
        return classModel.associationClassNamed[name]
    else:
        return None

# TODO: move this to metamodels.classes ?
def _find_resource(classModel, expr, astNode):
    #type: (ClassModel, 'ASTResourceExpr', 'ASTNode')->Optional[Resource]
    """ Search the expr in class/association/associationclass/attribute/role
        The expression could look like X or X.y
    """
    if DEBUG>=2:
        print('_find_resource ("%s")' % expr)
    entity_name=expr.entityName
    member_name=expr.memberName

    entity=_find_entity(classModel, entity_name)
    if entity is None:
        ASTNodeSourceIssue(
            code=icode('RULE_CLASSIFIER_NOT_FOUND'),
            astNode=astNode,
            level=Levels.Fatal,
            message=(
                '"%s" is neither an actor nor a usecase.' % entity_name))
    if member_name is None:
        return entity
    # TODO: to be changed when Plain Class/Association is impl
    #       currently the metamodel of classes is ill defined
    #       when changed update this (care for AssociationClass)
    if isinstance(entity, Class):
        if member_name in entity.attributeNamed:
            return entity.attributeNamed[member_name]
        else:
            ASTNodeSourceIssue(
                code=icode('RULE_ATTRIBUTE_NOT_FOUND'),
                astNode=astNode,
                level=Levels.Fatal,
                message=(
                    '"Attribute %s.%s" not found.' % (
                        entity_name, member_name)))
    elif isinstance(entity, Association):
        if member_name in entity.roleNamed:
            return entity.roleNamed[member_name]
        else:
            ASTNodeSourceIssue(
                code=icode('RULE_ROLE_NOT_FOUND'),
                astNode=astNode,
                level=Levels.Fatal,
                message=(
                    '"Role %s.%s" not found.' % (
                        entity_name, member_name)))
    elif isinstance(entity, AssociationClass):
        if member_name in entity.attributeNamed:
            return entity.attributeNamed[member_name]
        elif member_name in entity.roleNamed:
            return entity.roleNamed[member_name]
        else:
            ASTNodeSourceIssue(
                code=icode('RULE_MEMBER_NOT_FOUND'),
                astNode=astNode,
                level=Levels.Fatal,
                message=(
                    '"%s.%s" not found.' % (
                        entity_name, member_name)))
    else:
        raise NotImplementedError(
            'Unexpected entity type: %s' % type(entity))



METAMODEL.registerSource(PermissionModelSource)
