# coding=utf-8

from typing import Dict, Text, Optional, Union, List

from abc import ABCMeta, abstractmethod
from collections import OrderedDict

from modelscripts.megamodels.models import Placeholder
# from modelscripts.metamodels.classes.classes import Class
from modelscripts.metamodels.classes.types import UNSPECIFIED
from modelscripts.metamodels.textblocks import TextBlock
from modelscripts.metamodels.objects import (
    ObjectModel,
    ElementFromOptionalStep,
    Member,
    PackagableElement,
    Entity)
from modelscripts.base.exceptions import (
    MethodNotDefined,
    NoSuchFeature)


class _ClassPrint(object):
    """
    The list of ids value for a given object. It could also be
    the list of all values for a given object, not only id.
    This is used to compare the class print of two object.
    For a given object this is basically a
        Dict[attname,Optional[Text]] for each
    that is, a optional value for each attributes in the class.
    The value of slots are converted to Text to simplify
    implementation.
    This may cause problem with multiple textual representation
    (e.g. 10.00 vs 10.0, "a'" vs 'a\''. This is good enough
    however at the time being.
    If an attribute has no slot return None.
    If "onlyIds" are specified only these attributes are selected.

    This class is useful to compare objects and their ids.
    Use equals() for that.
    """
    def __init__(self, object, onlyIds=False, inherited=False):
        # TODO:3 check impact of inheritance
        #   care should be taken with inheritance (additional param?)
        self.object=object
        self.attVal=OrderedDict()
        #type: Dict[Text, Optional[Text]]
        # add all attribute/values pairs to attVal
        for att in self.object.class_.attributes:
            if not onlyIds or att.isId:
                s=self.object.slot(att.name)
                if s is None:
                    self.attVal[att.name]=UNSPECIFIED
                else:
                    self.attVal[att.name]=str(s.simpleValue)

    def equals(self, classPrint2):
        """
        If two valued attributes differ return False.
        If there is at least one None, then return None.
        Otherwise return false.
        """
        has_unspecified=False
        for att in self.attVal.keys():
            v1=self.attVal[att]
            v2=classPrint2.attVal[att]
            if (v1 is not UNSPECIFIED
                and v2 is not UNSPECIFIED
                and v1!=v2):
                return False
            if v1 is UNSPECIFIED or v2 is UNSPECIFIED:
                has_unspecified=True
        else:
            if has_unspecified:
                return UNSPECIFIED
            else:
                return True

    def __str__(self):
        if len(self.attVal)==0:
            return ()
        elif len(self.attVal)==1:
            return str(self.attVal[self.attVal.keys()[0]])
        else:
            return '(%s)' % (','.join([
                '%s=%s' % (att, str(val))
                for (att, val) in self.attVal.items()
            ]))


class Object(PackagableElement, Entity):
    """
    An object. Either a plain object or a link object.
    Link object
    """
    __metaclass__ = ABCMeta

    def __init__(self, model, name, class_,
                 package=None,
                 step=None,
                 lineNo=None, description=None, astNode=None):
        #type: (ObjectModel, Text, Union['Class', Placeholder], Optional[package], Optional['Step'], Optional[int], Optional[TextBlock], Optional['ASTNode'] )-> None
        PackagableElement.__init__(
            self,
            model=model,
            name=name,
            package=package,
            step=step,
            astNode=astNode,
            lineNo=lineNo,
            description=description
        )
        Entity.__init__(self)

        self.class_ = class_
        #type: Union[Placeholder, 'Class']

        self._slotNamed = OrderedDict()
        #type: Dict[Text, Slot]
        # Slots of the object indexed by attribute name (not attribute)

        self._link_roles_per_role=OrderedDict()
        #type: Dict['Role', 'LinkRole']
        """
        The links roles "opposite" to the objects, that is, at the
        opposite side of the link. The collection is indexed by 
        the "owned" roles. Note that the direction of the
        association is not taken into account. Only owned
        roles count to group links. Only valid linked roles are 
        in this list. This variable is set by the object
        analyzer by the method _analyze_link_role_types.
        """

    def cardinality(self, role):
        if role in self._link_roles_per_role:
            return len(self._link_roles_per_role[role])
        else:
            raise NoSuchFeature( #raise:OK
                'Unexpected role "%s" for an object of class "%s"' % (
                    role.name,
                    self.class_.name))

    @property
    def slots(self):
        return list(self._slotNamed.values())

    @property
    def slotNames(self):
        return list(self._slotNamed.keys())

    def slot(self, name):
        if name in self._slotNamed:
            return self._slotNamed[name]
        else:
            return None

    def links(role):
        #type: ('Role') -> List['Link']
        """
        The list of links that are connected to the object and
        that are owned by the role.
        """

    @abstractmethod
    def isPlainObject(self):
        # This method is not really useful as isinstance can be used.
        # It is just used to prevent creating object of this class
        # (using ABCMeta is not enough to prevent this).
        raise MethodNotDefined( #raise:OK
            'isPlainObject() is not defined')

    # def _class_print(self, onlyIds=False):
    #     #type: (bool) -> Dict[Text, Optional[SimpleValue]]
    #     """
    #     Return a Dict[attname,Optional[SimpleValue]] for each
    #     attributes in the class. If a value has no slot return None.
    #     If "onlyIds" are specified only these attributes are selected.
    #     :param onlyIds:
    #     :return:
    #     """
    #     id_print=IdPrint()
    #     for att in self.class_.attributes:
    #         if not onlyIds or att.isId:
    #             s=self.slot(att.name)
    #             if s is None:
    #                 cprint[att.name]=None
    #             else:
    #                 cprint[att.name]=s.value
    #     return cprint

    @property
    def idPrint(self):
        return _ClassPrint(
            object=self,
            onlyIds=True
        )

    def __str__(self):
        return self.name


class PlainObject(Object):

    def __init__(self, model, name, class_,
                 package=None,
                 step=None,
                 lineNo=None, description=None, astNode=None):
        #type: (ObjectModel, Text, Union['Class', Placeholder], Optional[package], Optional['Step'], Optional[int], Optional['ASTNode'] )-> None
        super(PlainObject, self).__init__(
            model=model,
            name=name,
            class_=class_,
            package=package,
            step=step,
            astNode=astNode,
            lineNo=lineNo,
            description=description
        )
        model._plainObjectNamed[name]=self


    def isPlainObject(self):
        return True


class Slot(ElementFromOptionalStep, Member):

    def __init__(self, object, attribute, simpleValue,
                 step=None,
                 description=None, lineNo=None, astNode=None):
        #type: (Object, Union['Attribute', Placeholder], 'DataValue',  Optional['Step'], Optional[TextBlock], Optional[int], 'ASTNode') -> None
        attribute_name=(
            attribute.placeholderValue
                if isinstance(attribute, Placeholder)
            else attribute.name
        )
        ElementFromOptionalStep.__init__(
            self,
            model=object.model,
            name='%s.%s' % (object.name, attribute_name),
            step=step,
            astNode=astNode,
            lineNo=lineNo,
            description=description)
        Member.__init__(self)
        self.object=object

        self.attribute=attribute
        self.simpleValue=simpleValue
        object._slotNamed[attribute_name]=self

    def __str__(self):
        return '%s.%s=%s' % (
            self.object.name,
            self.attribute.name,
            str(self.simpleValue)
        )