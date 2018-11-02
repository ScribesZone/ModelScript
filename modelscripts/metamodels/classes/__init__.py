# coding=utf-8

"""
Class metamodel.

The structure of this package is::

    ClassModel
    <>--* Package
        <>--* Enumeration
        <>--* Class
              <>--* Attribute
              <>--* Operation
                    <>--* OperationCondition
              <>--* Invariant
        <>--* Association
              <>--2 Role
        <>--* AssociationClass
              <>--2 Role
              <>--* Attribute
              <>--* Operation
                    <>--* OperationCondition
        <>--* DataType

    Association, Class
    <|--  AssociationClass

    PackagableElement
    <|-- Enumeration

    SimpleType
    <|--  DataType
    <|--  Enumeration

"""
from __future__ import print_function

import abc
import collections
import logging

from typing import Text, Dict

from modelscripts.base.graphs import (
    genPaths
)
from modelscripts.base.grammars import (
    # ModelSourceAST, \
    # ASTBasedModelSourceFile,
    ASTNodeSourceIssue
)
from modelscripts.base.issues import (
    Levels
)




# TODO:3 metastuff to be continued
from modelscripts.megamodels.py import (
    MComposition,
    MAttribute
)
from modelscripts.megamodels.elements import SourceModelElement
from modelscripts.base.metrics import Metrics
from modelscripts.megamodels.metamodels import Metamodel
from modelscripts.megamodels.dependencies.metamodels import (
    MetamodelDependency
)
from modelscripts.megamodels.models import Model
# from modelscripts.metamodels.classes.associations import Association
# from modelscripts.metamodels.classes.classes import Class
# from modelscripts.metamodels.classes.types import (
#     Enumeration )

from modelscripts.metamodels.permissions.sar import Resource

META_CLASSES=( # could be in __all__ (not used by PyParse)
    'ClassModel',
    'PackagableElement',
    'Entity',
    'Member',
    'SimpleType',
    'DataType',
    'Enumeration',
    'EnumerationLiteral',
    'Class',
    'Attribute',
    'Operation',
    'Association',
    'Role',
    'RolePosition',
    'opposite',
    'AssociationClass',
)

__all__= META_CLASSES


ISSUES={
    'SUPER_CYCLES_MSG': 'cl.fin.Cycle.One',
    'SUPER_CYCLES_STOP': 'cl.fin.Cycle.Final',
    'SUPER_ATT_INH_HORIZ': 'cl.fin.Attribute.InhHorizontal',
    'SUPER_ATT_INH_VERT': 'cl.fin.Attribute.InhVertical',
    'SUPER_OROLE_INH_VERT': 'cl.fin.Attribute.InhVertical',
    'SUPER_OROLE_INH_HORIZ': 'cl.fin.Attribute.InhHorizontal',
}

def icode(ilabel):
    return ISSUES[ilabel]

#TODO:1 check if cardinality handling is ok
# It seems that there is a bug with * ou 1..*

# logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('test.' + __name__)


class ClassModel(Model):
    """
    Class model.
    """
    # metaMembers = [
    #       MComposition('enumerations : Enumeration[*] inv model'),
    #       MComposition('plainClasses : Class [*] inv model'),
    #       MComposition(
    #           'associationsClasses : Association[*] inv model'),
    #       MComposition('dataTypes : DataType[*] inv model'),
    # ]


    #TODO:4 convert this to MComposition when ready
    META_COMPOSITIONS=[
        'enumerations',
        'plainClasses',
        'plainAssociations',
        'associationClasses',
        'dataTypes',
        'invariants',
        'packages',
    ]
    def __init__(self):
        #type: () -> None
        super(ClassModel, self).__init__()

        self._isResolved=False
        self._isClassModelFinalized=False

        self._enumerationNamed=collections.OrderedDict()
        #type: Dict[Text, 'Enumeration']
        #: Map of enumerations, indexed by name.

        #: Map of data types. Indexed by type names/
        #: populated during the resolution phase
        self._dataTypeNamed=collections.OrderedDict()
        #type: Dict[Text, 'DataType']

        self._plainClassNamed = collections.OrderedDict()
        #type: Dict[Text, 'PlainClass']
        #: Only plain classes. Use method classes to get
        #: all the class (plain class + association class)

        self._plainAssociationNamed = collections.OrderedDict()
        #type: Dict[Text, 'PlainAssociation']
        #: Only plain associations. Use method associations to get
        #: all associations (association class + plain associations)

        self._associationClassNamed = collections.OrderedDict()
        #type: Dict[Text, 'AssociationClass']
        #: Map of association classes, indexed by name.

        self.operationWithFullSignature = collections.OrderedDict()
        #type: Dict[Text, 'Operation']
        #: Map of operations, indexed by operation full signatures.
        #: e.g. 'Person::raiseSalary(rate : Real) : Real

        self._packageNamed=collections.OrderedDict()
        #type: Dict[Text, Package]
        # ALL packages, not only the top level ones

        self._invariantNamed = collections.OrderedDict()
        #type: Dict[Text, 'Invariant']


        from modelscripts.metamodels.classes.core import \
            registerDataTypes
        registerDataTypes(self)
        # Register core datatypes

        from modelscripts.metamodels.classes.oclchecker import \
            ClassOCLChecker
        self.classOCLChecker=ClassOCLChecker(self)

    @property
    def metamodel(self):
        return METAMODEL

    #--------------------------------------------------------------
    #   packages
    #--------------------------------------------------------------

    @property
    def packages(self):
        return self._packageNamed.values()

    @property
    def packageNames(self):
        return self._packageNamed.keys()

    def package(self, name):
        if name in self._packageNamed:
            return self._packageNamed[name]
        else:
            return None

    # --------------------------------------------------------------
    #   simple types
    # --------------------------------------------------------------

    @property
    def simpleTypeNamed(self):
        _ = self._dataTypeNamed.copy()
        _.update(self._enumerationNamed)
        return _

    @property
    def simpleTypes(self):
        return self.simpleTypeNamed.values()

    @property
    def simpleTypeNames(self):
        return self.simpleTypeNamed.keys()

    @MComposition('DataType[*] inv model')
    def dataTypes(self):
        return self._dataTypeNamed.values()

    @property
    def dataTypeNames(self):
        return self._dataTypeNamed.keys()

    def dataType(self, name):
        if name in self._dataTypeNamed:
            return self._dataTypeNamed[name]
        else:
            return None

    @property
    def enumerations(self):
        return self._enumerationNamed.values()

    @property
    def enumerationNames(self):
        return self._enumerationNamed.keys()

    def enumeration(self, name):
        if name in self._enumerationNamed:
            return self._enumerationNamed[name]
        else:
            return None

    # --------------------------------------------------------------
    #   classes
    # --------------------------------------------------------------

    @property
    def plainClasses(self):
        return self._plainClassNamed.values()

    @property
    def plainClassNames(self):
        return self._plainClassNamed.keys()

    def plainClass(self, name):
        if name in self._plainClassNamed:
            return self._plainClassNamed[name]
        else:
            return None

    @property
    def classes(self):
        """
        All classes or association classes.
        """
        return self.plainClasses+self.associationClasses

    @property
    def classNames(self):
        return self.plainClassNames+self.associationClassNames

    def class_(self, name):
        c=self.plainClass(name)
        if c is not None:
            return c
        else:
            return self.associationClass(name)

    # --------------------------------------------------------------
    #   associations
    # --------------------------------------------------------------

    @property
    def plainAssociations(self):
        return self._plainAssociationNamed.values()

    @property
    def plainAssociationNames(self):
        return self._plainAssociationNamed.keys()

    def plainAssociation(self, name):
        if name in self._plainAssociationNamed:
            return self._plainAssociationNamed[name]
        else:
            return None

    @property
    def associations(self):
        """
        All classes or association classes.
        """
        return self.plainAssociations+self.associationClasses

    @property
    def associationNames(self):
        return self.plainAssociationNames+self.associationClassNames

    def association(self, name):
        a=self.plainAssociation(name)
        if a is not None:
            return a
        else:
            return self.associationClass(name)

    # --------------------------------------------------------------
    #   association classes
    # --------------------------------------------------------------

    @property
    def associationClasses(self):
        return self._associationClassNamed.values()

    @property
    def associationClassNames(self):
        return self._associationClassNamed.keys()

    def associationClass(self, name):
        if name in self._associationClassNamed:
            return self._associationClassNamed[name]
        else:
            return None

    # --------------------------------------------------------------
    #   invariants
    # --------------------------------------------------------------

    @property
    def invariants(self):
        return self._invariantNamed.values()

    @property
    def invariantNames(self):
        return self._invariantNamed.keys()

    def invariant(self, name):
        if name in self._invariantNamed:
            return self._invariantNamed[name]
        else:
            return None

    @property
    def hasOCLCode(self):
        for inv in self.invariants:
            if inv.hasOCLCode:
                return True
        else:
            return False


    def entity(self, name):
        # This is used for permission, to search for an entity by name
        e=self.class_(name)
        if e is not None:
            return e
        else:
            return self.association(name)

    @property
    def metrics(self):
        #type: () -> Metrics
        ms=super(ClassModel, self).metrics
        ms.addList((
            ('package', len(self.packages)),
            ('data type', len(self.dataTypes)),
            ('enumeration', len(self.enumerations)),
            ('enumeration literal', len(
                [el
                    for e in self.enumerations
                        for el in e.literals])),
            ('class', len(self.classes) ),
            ('plain class', len(self.plainClasses) ),
            ('association', len(self.associations)),
            ('plain association',
                 len(self.plainAssociations)),
            ('association class', len(self.associationClasses)),
            ('attribute', len(
                [a
                    for c in self.classes
                        for a in c.attributes])),
            ('owned attribute', len(
                [a
                 for c in self.classes
                 for a in c.ownedAttributes])),
            ('inherited attribute', len(
                [a
                 for c in self.classes
                 for a in c.inheritedAttributes])),
            ('role', len(
                [r
                    for a in self.associations
                        for r in a.roles])),
            ('invariant', len(self.invariants))))
        return ms

    def globalNames(self):
        return (
            self.enumerationNames
            + self.classNames
            + self.associationNames
            + self.dataTypeNames)

    def __str__(self):
        # TODO:4 move this to printer
        def category_line(label,elems):
            print(label)
            print(elems)
            n = len(list(elems))
            return '% 3d %s: %s' % (
                n,
                label.ljust(22),
                ','.join(elems)
            )
        categories = [
            ('packages', self.packageNames),
            ('data types', self.dataTypeNames),
            ('enumerations', self.enumerationNames),
            ('plain classes', self.plainClassNames),
            ('plain associations', self.associationNames),
            ('association classes', self.associationClassNames),
        ]
        total = 0
        lines = [ 'class model '+self.name ]
        for (label, items) in categories:
            lines.append(category_line(label, items))
            total += len(list(items))
        print(lines)
        lines.append('% 3d' % total)
        return  '\n'.join(lines)

    def finalize(self):
        super(ClassModel, self).finalize()

        def add_owned_attached_roles():
            for a in self.associations:
                source_class=a.sourceRole.type
                target_class=a.targetRole.type

                source_class._ownedOppositeRoleNamed \
                    [a.targetRole.name]=a.targetRole
                source_class._ownedPlayedRoles.append(a.sourceRole)

                target_class._ownedOppositeRoleNamed \
                    [a.sourceRole.name]=a.sourceRole
                target_class._ownedPlayedRoles.append(a.targetRole)

        def check_inheritance_cycles():
            cycles_nb=0
            last_class=None
            for class_ in self.classes:
                cycles=list(
                    genPaths(
                        lambda x: x.superclasses,
                        class_,
                        class_))
                if len(cycles)>=1:
                    ASTNodeSourceIssue(
                        code=icode('SUPER_CYCLES_MSG'),
                        astNode=class_.astNode,
                        level=Levels.Error,
                        message=(
                            'Class inheritance is cyclic for "%s"'
                             % class_.name))
                    # TODO:4 add detailed message with cycles var
                    cycles_nb += len(cycles)
                    # just for (more or less) localized error message
                    last_class = class_
                class_.inheritanceCycles=cycles
            if cycles_nb>=1:
                ASTNodeSourceIssue(
                    code=icode('SUPER_CYCLES_STOP'),
                    astNode=last_class.astNode,
                    level=Levels.Fatal,
                    message=(
                        'The inheritance graphs is cyclic.'))

        def add_inherited_attributes():
            # Dill the attribute class._inheritedAttributeNamed
            # Implement the inheritance algorithm with
            # multiple inheritance.

            def _ensure_inherited_attribute(class_):
                # Fill the attribute inheritedAttributeNamed
                # The "horizontal' name confilcts are reported. That is
                # the situation where an attribute let's say "x" is
                # inherited from one side, and another attribute with
                # the same name is inherited from the another side.
                if class_._inheritedAttributeNamed is not None:
                    return
                inh_att_named = collections.OrderedDict()
                for sc in class_.superclasses:
                    _ensure_inherited_attribute(sc)
                    # for all inherited attributes
                    for sc_att in sc.attributes:
                        # if the attribute was already inherited
                        # do not care.
                        # Otherwise prepare to add it
                        if sc_att not in inh_att_named.values():
                            name=sc_att.name
                            if name in inh_att_named.keys():
                                # two inherited attribute have the same
                                # name.
                                ASTNodeSourceIssue(
                                    code=icode('SUPER_ATT_INH_HORIZ'),
                                    astNode=class_.astNode,
                                    level=Levels.Error,
                                    message=(
                                        'Two inherited attributes are'
                                        ' named "%s"'
                                        ' Attribute ignored.' % name))
                            else:
                                inh_att_named[name]=sc_att
                class_._inheritedAttributeNamed=inh_att_named
                print('WW'*10, 'class %s inherits' % class_.name)
                for a in inh_att_named:
                    print('WW' * 10, '    %s' % a)

            def _check_no_vertical_conflicts(class_):
                for name in class_._inheritedAttributeNamed.keys():
                    if name in class_.ownedAttributeNames:
                        ASTNodeSourceIssue(
                            code=icode('SUPER_ATT_INH_VERT'),
                            astNode=class_.astNode,
                            level=Levels.Error,
                            message=(
                                    'Inherited attribute "%s" conflicts'
                                    ' with "%s.%s".'
                                    ' Inherited attribute ignored.'
                                    % (name, class_.name, name)))
                        del class_._inheritedAttributeNamed[name]

            for class_ in self.classes:
                _ensure_inherited_attribute(class_)
                _check_no_vertical_conflicts(class_)

        def add_inherited_attached_roles():
            # Fill two attributes for class_:
            #       _inheritedOppositeRoleNamed
            #       _inheritedRoleNamed
            # Implement the inheritance algorithm with
            # multiple inheritance.

            def _ensure_inherited_opposite_roles(class_):
                pass

                # Implement the inheritance of opposite roles.
                # Fill the following attribute for class_:
                #       _inheritedOppositeRoleNamed
                # Another function is used for played roles.
                #
                # The "horizontal' name conflicts are reported for
                # opposite roles (there is no need to check this
                # for played role since played roles can have the
                # same name). Horizontal conflicts reflect
                # the situation where an opposite role let's say "x" is
                # inherited from one side of the inheritance graph,
                # and another opposite role with the same name is
                # inherited from the another side.

                # The function is recursive. It walk among all class_,
                # following inheritance relationships.
                # The attribute to fill serve as a "visited" marker.
                #
                #####################################################
                #####################################################
                #####################################################
                #           TO BE CONTINUED
                #####################################################
                #####################################################
                #####################################################
                # if class_._inheritedOppositeRoleNamed is not None:
                #     return
                # inh_opp_role_named = collections.OrderedDict()
                # for sc in class_.superclasses:
                #     _ensure_inherited_opposite_roles(sc)
                #     # for all inherited opposite roles
                #     for sc_opp_role in sc.oppositeRoles:
                #         # if the opposite roles was already inherited
                #         # do not care.
                #         # Otherwise prepare to add it
                #         if sc_opp_role not in inh_opp_role_named.values():
                #             name=sc_opp_role.name
                #             if name in inh_opp_role_named.keys():
                #                 # two inherited opposite role have
                #                 # the same name.
                #                 ASTNodeSourceIssue(
                #                     code=icode('SUPER_OROLE_INH_VERT'),
                #                     astNode=class_.astNode,
                #                     level=Levels.Fatal, XXXXXXXX
                #                     message=(
                #                         'Name conflict between two'
                #                         ' inherited roles: "%s".'
                #                          % name))
                #             else:
                #                 WWW
                #                 inh_att_named[name]=sc_att
                # class_._inheritedAttributeNamed=inh_att_named
                # print('WW'*10, 'class %s inherits' % class_.name)
                # for a in inh_att_named:
                #     print('WW' * 10, '    %s' % a)

            def _ensure_inherited_played_roles(class_):
                pass #TODO:1 add inheritance

            def _check_no_vertical_conflicts(class_):
                pass #TODO:1 add inheritance

            for class_ in self.classes:
                _ensure_inherited_opposite_roles(class_)
                _ensure_inherited_played_roles(class_)
                _check_no_vertical_conflicts(class_)

        add_owned_attached_roles()
        check_inheritance_cycles()  # #### ORDER IS IMPORTANT ####
        add_inherited_attributes()  # After check
        add_inherited_attached_roles() # After check

        self.classOCLChecker.check()

        self._isClassModelFinalized=True




class PackagableElement(SourceModelElement):
    """
    Top level element.
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self,
                 name,
                 model,
                 astNode=None,
                 package=None,
                 lineNo=None, description=None):
        SourceModelElement.__init__(
            self,
            model=model,
            name=name,
            astNode=astNode,
            lineNo=lineNo, description=description)
        self.package=package
        if self.package is not None:
            self.package.addElement(self)

    @MAttribute('String')
    def label(self):
        if self.package is not None:
            return '%s.%s' % (
                self.package.label,
                self.name)
        else:
            return self.name


class Item(object):
    """
    Either an entity or a member.
    Useful for instance to define "scope" of invariants.
    Is is named either like X or X.Y
    X can be a
        enumeration/datatype
        class/association/associationclass
        package
        invariant
    Y can be a enumeration literal, attribute or role
    """

    __metaclass__ = abc.ABCMeta


class Entity(Resource, Item):

    __metaclass__ = abc.ABCMeta


class Member(Resource, Item):

    __metaclass__ = abc.ABCMeta


class Package(PackagableElement, Entity):
    """
    Packages.
    """
    def __init__(self,
                 name,
                 model,
                 astNode=None,
                 package=None,
                 lineNo=None, description=None):
        super(Package, self).__init__(
            name=name,
            model=model,
            astNode=astNode,
            package=package,
            lineNo=lineNo, description=description,)
        self._elememts=[]
        model._packageNamed[name]=self


    @property
    def elements(self):
        return self._elememts

    def addElement(self, element):
        assert element is not None
        if element not in self._elememts:
            self._elememts.append(element)
            element.package=self


# class Parameter


METAMODEL = Metamodel(
    id='cl',
    label='class',
    extension='.cls',
    modelClass=ClassModel,
    uniqueness=True
)

MetamodelDependency(
    sourceId='cl',
    targetId='gl',
    optional=True,
    multiple=True,
)

