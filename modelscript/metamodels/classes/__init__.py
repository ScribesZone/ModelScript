# coding=utf-8
"""Class metamodel.

The composition view is the backbone of the class model.
It shows containment relationships ::

    ClassModel
        <>--* Package
        <>--* DataType
        <>--* Enumeration
              <>--* EnumerationLiteral
        <>--* PlainClass
              <>--* Attribute
              <>--* Operation           opdel
                    <>--* OperationCondition
              <>--* Invariant           invdel
        <>--* PlainAssociation
              <>--2 Role
        <>--* AssociationClass
              <>--2 Role
              <>--* Attribute
              <>--* Operation           opdel
                    <>--* OperationCondition
    Association, Class
    <|--  AssociationClass

    Class
    </-- PlainClass

    Association
    </-- PlainAssociation


    SimpleType
    <|--  DataType
    <|--  Enumeration

"""

import abc
import collections
import logging
from typing import Text, Dict, List, Optional

from modelscript.base.graphs import (
    genPaths)
from modelscript.base.grammars import (
    # ModelSourceAST, \
    # ASTBasedModelSourceFile,
    ASTNodeSourceIssue)
from modelscript.base.issues import (
    Levels)
# TODO:3 metastuff to be continued
from modelscript.megamodels.py import (
    MComposition,
    MAttribute)
from modelscript.megamodels.elements import SourceModelElement
from modelscript.base.metrics import Metrics
from modelscript.megamodels.metamodels import Metamodel
from modelscript.megamodels.dependencies.metamodels import (
    MetamodelDependency)
from modelscript.megamodels.models import Model
# from modelscript.metamodels.classes.associations import Association
# from modelscript.metamodels.classes.classes import Class
# from modelscript.metamodels.classes.types import (
#     Enumeration )
from modelscript.metamodels.permissions.sar import Resource

__all__ = (
    'ClassModel',
    'PackagableElement',
    'Item',
    'Entity',
    'Member',
    'Package',
    'METAMODEL',
    'MetamodelDependency'
)


ISSUES = {
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
    """Class model.
    """
    # metaMembers = [
    #       MComposition('enumerations : Enumeration[*] inv model'),
    #       MComposition('plainClasses : Class [*] inv model'),
    #       MComposition(
    #           'associationsClasses : Association[*] inv model'),
    #       MComposition('dataTypes : DataType[*] inv model'),
    # ]


    #TODO:4 convert this to MComposition when ready
    META_COMPOSITIONS = [
        'enumerations',
        'dataTypes',
        'plainClasses',
        'plainAssociations',
        'associationClasses',
        'packages',
        'invariants',
    ]

    _isResolved: bool
    _isClassModelFinalized: bool

    _enumerationNamed: Dict[str, 'Enumeration']
    """Map of enumerations, indexed by name."""

    _dataTypeNamed: Dict[str, 'DataType']
    """Map of data types. Indexed by type names."""

    _plainClassNamed: Dict[str, 'PlainClass']
    """Only plain classes. 
    Use method classes to get all the class (plain class + 
    association class)
    """

    _plainAssociationNamed:  Dict[str, 'PlainAssociation']
    """Only plain associations. 
    Use method associations to get all associations (association 
    class + plain associations)
    """

    _associationClassNamed: Dict[str, 'AssociationClass']
    """Map of association classes, indexed by name."""

    # opdel
    operationWithFullSignature: Dict[str, 'Operation']
    """Map of operations, indexed by operation full signatures.
    e.g. 'Person::raiseSalary(rate : Real) : Real
    """

    _packageNamed: Dict[str, 'Package']
    """ALL packages, not only the top level ones."""

    _invariantNamed: Dict[str, 'Invariant']
    """Map of invariants indexed by name/   """

    classOCLChecker: 'ClassOCLChecker'

    def __init__(self) -> None:
        super(ClassModel, self).__init__()

        self._isResolved = False
        self._isClassModelFinalized = False
        self._enumerationNamed = collections.OrderedDict()

        #: populated during the resolution phase
        self._dataTypeNamed = collections.OrderedDict()

        self._plainClassNamed = collections.OrderedDict()
        self._plainAssociationNamed = collections.OrderedDict()
        self._associationClassNamed = collections.OrderedDict()
        self.operationWithFullSignature = collections.OrderedDict() #opdel
        self._packageNamed = collections.OrderedDict()
        self._invariantNamed = collections.OrderedDict()

        from modelscript.metamodels.classes.core import \
            registerDataTypes
        registerDataTypes(self)
        # Register core data types

        from modelscript.metamodels.classes.oclchecker import \
            ClassOCLChecker
        self.classOCLChecker = ClassOCLChecker(self)

    @property
    def metamodel(self):
        return METAMODEL

    # --------------------------------------------------------------
    #   enumerations
    # --------------------------------------------------------------

    @property
    def enumerations(self) -> List['Enumerations']:
        return list(self._enumerationNamed.values())

    @property
    def enumerationNames(self) -> List[str]:
        return list(self._enumerationNamed.keys())

    def enumeration(self, name: str) -> Optional['Enumerations']:
        if name in self._enumerationNamed:
            return self._enumerationNamed[name]
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
    def simpleTypes(self) -> List['SimpleType']:
        return list(self.simpleTypeNamed.values())

    @property
    def simpleTypeNames(self) -> List[str]:
        return list(self.simpleTypeNamed.keys())

    def simpleType(self, name: str) -> Optional['SimpleType']:
        if name in self.simpleTypeNamed:
            return self.simpleTypeNamed[name]
        else:
            return None

    # --------------------------------------------------------------
    #   data types
    # --------------------------------------------------------------

    @MComposition('DataType[*] inv model')
    def dataTypes(self):
        return list(self._dataTypeNamed.values())

    @property
    def dataTypeNames(self):
        return list(self._dataTypeNamed.keys())

    def dataType(self, name):
        if name in self._dataTypeNamed:
            return self._dataTypeNamed[name]
        else:
            return None

    # --------------------------------------------------------------
    #   packages
    # --------------------------------------------------------------

    @property
    def packages(self) -> List['Package']:
        return list(self._packageNamed.values())

    @property
    def packageNames(self) -> List[str]:
        return list(self._packageNamed.keys())

    def package(self, name: str) -> Optional['Package']:
        if name in self._packageNamed:
            return self._packageNamed[name]
        else:
            return None

    # --------------------------------------------------------------
    #   plain classes
    # --------------------------------------------------------------


    @property
    def plainClasses(self):
        return list(self._plainClassNamed.values())

    @property
    def plainClassNames(self):
        #TODO:4 2to3 add list
        return list(self._plainClassNamed.keys())

    def plainClass(self, name):
        if name in self._plainClassNamed:
            return self._plainClassNamed[name]
        else:
            return None

    # --------------------------------------------------------------
    #   classes
    # --------------------------------------------------------------

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
    #   plain associations
    # --------------------------------------------------------------

    @property
    def plainAssociations(self):
        return list(self._plainAssociationNamed.values())

    @property
    def plainAssociationNames(self):
        return list(self._plainAssociationNamed.keys())

    def plainAssociation(self, name):
        if name in self._plainAssociationNamed:
            return self._plainAssociationNamed[name]
        else:
            return None

    # --------------------------------------------------------------
    #   associations
    # --------------------------------------------------------------

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
        return list(self._associationClassNamed.values())

    @property
    def associationClassNames(self):
        return list(self._associationClassNamed.keys())

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
        return list(self._invariantNamed.values())

    @property
    def invariantNames(self):
        return list(self._invariantNamed.keys())

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
        def category_line(label, elems):
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
                source_class = a.sourceRole.type
                target_class = a.targetRole.type

                source_class._ownedOppositeRoleNamed \
                    [a.targetRole.name] = a.targetRole
                source_class._ownedPlayedRoles.append(a.sourceRole)

                target_class._ownedOppositeRoleNamed \
                    [a.sourceRole.name]=a.sourceRole
                target_class._ownedPlayedRoles.append(a.targetRole)

        def check_inheritance_cycles():
            cycles_nb = 0
            last_class = None
            for class_ in self.classes:
                cycles = list(
                    genPaths(
                        lambda x: x.superclasses,
                        class_,
                        class_))
                class_.inheritanceCycles = cycles
                if len(cycles) >= 1:
                    ASTNodeSourceIssue(
                        code=icode('SUPER_CYCLES_MSG'),
                        astNode=class_.astNode,
                        level=Levels.Error,
                        message=(
                            'Class inheritance is cyclic for "%s" : %s'
                             % (class_.name, class_.cycles)))
                    # TODO:4 add detailed message with cycles var
                    cycles_nb += len(cycles)
                    # just for (more or less) localized error message
                    last_class = class_
            if cycles_nb >= 1:
                ASTNodeSourceIssue(
                    code=icode('SUPER_CYCLES_STOP'),
                    astNode=last_class.astNode,
                    level=Levels.Fatal,
                    message=(
                        'The inheritance graphs is cyclic.'))

        def add_inherited_attributes():
            # Fill the attribute class._inheritedAttributeNamed
            # Implement the inheritance algorithm with
            # multiple inheritance.

            def _ensure_inherited_attribute(class_):
                # Fill the attribute inheritedAttributeNamed
                # The "horizontal' name conflicts are reported. That is
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
                        if sc_att not in list(inh_att_named.values()):
                            name = sc_att.name
                            if name in list(inh_att_named.keys()):
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
                                inh_att_named[name] = sc_att
                class_._inheritedAttributeNamed = inh_att_named
                for a in inh_att_named:
                    print('WW' * 10, '    %s' % a)

            def _check_no_vertical_conflicts(class_):
                for name in list(class_._inheritedAttributeNamed.keys()):
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
        add_inherited_attached_roles()  # After check
        self.classOCLChecker.check()
        self._isClassModelFinalized = True


class PackagableElement(SourceModelElement, metaclass=abc.ABCMeta):
    """Top level element.
    """

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
        self.package = package
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


class Item(object, metaclass=abc.ABCMeta):   # invdel ?
    """Either an entity or a member.
    Useful for instance to define "scope" of invariants.
    Is is named either like X or X.Y
    X can be a
        enumeration/datatype
        class/association/associationclass
        package
        invariant
    Y can be a enumeration literal, attribute or role
    """


class Entity(Resource, Item, metaclass=abc.ABCMeta):

    pass


class Member(Resource, Item, metaclass=abc.ABCMeta):

    pass


class Package(PackagableElement, Entity):
    """Packages. """
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
        self._elements = []
        model._packageNamed[name] = self


    @property
    def elements(self):
        return self._elements

    def addElement(self, element):
        assert element is not None
        if element not in self._elements:
            self._elements.append(element)
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

