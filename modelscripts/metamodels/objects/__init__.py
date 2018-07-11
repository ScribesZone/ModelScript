# coding=utf-8

"""
    Abstract view
        ObjectModel
        <>--* Object
            <>--* Slot
        <>--* Link
        <>--* LinkObject

        StateElement
        <|-- Object
        <|-- Link

        Link, Object
        <|-- LinkObject

"""

from __future__ import print_function
from collections import OrderedDict
from typing import List, Optional, Dict, Text, Union
from abc import ABCMeta, abstractmethod

# TODO: to be continued
from modelscripts.megamodels.py import (
    MAttribute
)
from modelscripts.megamodels.elements import SourceModelElement
from modelscripts.base.metrics import Metrics
from modelscripts.megamodels.metamodels import Metamodel
from modelscripts.megamodels.models import (
    Model,
    Placeholder)
from modelscripts.megamodels.dependencies.metamodels import (
    MetamodelDependency
)
# used for typing
from modelscripts.metamodels.classes import (
    ClassModel,
    Class,
    Attribute,
    Association,
    Role,
    RolePosition,
    opposite,
    DataValue,
    SimpleValue,
    UNSPECIFIED,
    METAMODEL as CLASS_METAMODEL
)
from modelscripts.metamodels.textblocks import (
    TextBlock
)

__all__=(
    'ObjectModel',
    'StateElement',
    'Object',
    'AOBTextBlock',
    'PlainObject',
    'Slot',
    'Link',
    'PlainLink',
    'LinkRole',
    'LinkObject',
)


class ObjectModel(Model):

    """
    Object model, either create "manually" or via a story evaluation.
    """

    def __init__(self):
        super(ObjectModel, self).__init__()

        # ALL packages, not only the top level ones
        self.packageNamed=OrderedDict() #type: Dict[Text, Package]

        self._objectNamed = OrderedDict()
        # type: Dict[Text, Object]
        """
        All objects (plain objects and link objects).
        Link object are also registered in _links.
        """

        self._links=[]
        # type: List[Link]
        """
        All plain links (no link object).
        Link objects are also regitered in _objectNamed.
        """

        self._classModel=None
        #type: Optional[ClassModel]
        # filled by property classModel

        self.storyEvaluation=None
        #type: Optional['StoryEvaluation']
        # Filled only if this model is the result of a
        # story evaluation.
        # Otherwise this is most probably a handmade model.
        # Filled by object parser.

        self.checkStepEvaluation=None
        #type: Optional['CheckStepEvaluation']
        # Filled only if this model is the result of a Check
        # evaluation in a story.

        self.analyzis=None
        #type: Optional['ObjectModelAnalyzis']
        # Filled by finalize()

    def copy(self):
        """
        Return a ShadowObjectModel with the same content and
        the same classModel
        """
        return ObjectModelCopier(self).copy()

    @property
    def classModel(self):
        #type: ()-> ClassModel
        if self._classModel is None:
            self._classModel=self.theModel(CLASS_METAMODEL)
        return self._classModel

    def object(self, name):
        if name in self._objectNamed:
            return self._objectNamed[name]
        else:
            return None

    @property
    def objects(self):
        #type: () -> List[Object]
        return self._objectNamed.values()

    @property
    def plainObjects(self):
        #type: () -> List[PlainObject]
        return [
            o for o in self.objects if isinstance(o, PlainObject) ]

    @property
    def linkObjects(self):
        #type: () -> List[LinkObject]
        return [
            o for o in self.objects if isinstance(o, LinkObject) ]

    def classExtension(self, class_): #TODO: inheritance
        #type: (Class)-> List[Object]
        return [
            o for o in self.objects if o.class_==class_]

    @property
    def links(self):
        #type: () -> List[Link]
        return self._links

    @property
    def plainLinks(self):
        #type: () -> List[PlainLink]
        return [
            l for l in self._links if isinstance(l, PlainLink) ]


    @property
    def metrics(self):
        #type: () -> Metrics
        ms=super(ObjectModel, self).metrics
        ms.addList((
            ('object', len(self.objects)),
            ('link', len(self.links)),
            ('plain object', len(self.plainObjects)),
            ('plain link', len(self.plainLinks)),
            ('link object', len(self.linkObjects)),
            ('slot',sum(
                len(o.slots)
                for o in self.objects))
        ))
        return ms

    @property
    def metamodel(self):
        #type: () -> Metamodel
        return METAMODEL

    def finalize(self):
        from modelscripts.metamodels.objects.analyzis import (
            ObjectModelAnalyzis
        )
        self.analyzis=ObjectModelAnalyzis(self)
        self.analyzis.analyze()
        super(ObjectModel, self).finalize()


class ShadowObjectModel(ObjectModel):
    """
    Object model created or copied without any impact on the
    megamodel. No dependencies are created. ShadowObjectModel
    serves to represent intermediate state of stories.
    Their import box is empty.
    The class model must however be given explicitely since it
    is used to build ObjectModelAnalsysis.
    """
    def __init__(self, classModel):
        super(ShadowObjectModel, self).__init__()
        self._classModel=classModel


class ElementFromStep(SourceModelElement):
    """
    Superclass of all source model elements that can come
    from a story step. Basically add a "step" attribute to all
    subclasses.
    """
    __metaclass__ = ABCMeta

    def __init__(self,
                 name,
                 model,
                 step=None,
                 astNode=None,
                 lineNo=None, description=None):
        #type: (Optional['Step']) -> None
        """
        :param name: The name of the source element.
        :param model: The object model
        :param step: The step, if any, from where this element
            originates/
        :param astNode: The ast node, or None.
            step.astNode takes precedence.
        :param lineNo: lineNo for this element.
            step.lineNo take precendence.
        :param description: Description of the element.
            step take precendence
        """
        if astNode is None and step is not None:
            ast_node=step.astNode
        else:
            ast_node=astNode
        if lineNo is None and step is not None:
            line_no=step.lineNo
        else:
            line_no=lineNo
        if description is None and step is not None:
            description_=step.description
        else:
            description_=description
        super(ElementFromStep, self).__init__(
            model=model,
            name=name,
            astNode=ast_node,
            lineNo=line_no, description=description_)
        self.step=step


class PackagableElement(ElementFromStep):
    """
    Top level element.
    """
    __metaclass__ = ABCMeta

    def __init__(self,
                 name,
                 model,
                 package=None,
                 step=None,
                 lineNo=None, astNode=None, description=None):
        super(PackagableElement, self).__init__(
            model=model,
            name=name,
            step=step,
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


class ResourceInstance(object):
    __metaclass__ = ABCMeta
    """ 
    Currently not used, but can be useful to describes
    access instances. 
    This corresponds to the instance level of Resource.
    See modelscripts.metamodels.permissions.sar.Resource
    """


class Entity(ResourceInstance):
    __metaclass__ = ABCMeta


class Member(ResourceInstance):
    __metaclass__ = ABCMeta


# TODO: generalize and improve packages
#       This class comes from metamodels.class
#       It would make sense to move this to a upper level

class Package(PackagableElement):
    """
    Packages.
    """
    def __init__(self,
                 name,
                 model,
                 package=None,
                 step=None,
                 lineNo=None, astNode=None, description=None):
        PackagableElement.__init__(
            self,
            name=name,
            model=model,
            package=package,
            step=None,
            lineNo=lineNo, astNode=astNode, description=description)
        self._elememts=[]
        self.model.packageNamed[name]=self


    @property
    def elements(self):
        return self._elememts

    def addElement(self, element):
        assert element is not None
        if element not in self._elememts:
            self._elememts.append(element)
            element.package=self


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
        #type: (ObjectModel, Text, Union[Class, Placeholder], Optional[package], Optional['Step'], Optional[int], Optional[TextBlock], Optional['ASTNode'] )-> None
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
        #type: Union[Placeholder, Class]

        self._slotNamed = OrderedDict()
        #type: Dict[Text, Slot]
        # Slots of the object indexed by attribute name (not attribute)

        #TODO: check for duplicates to avoid loosing objects
        #      Register the object in the model
        model._objectNamed[name]=self

        self._link_roles_per_role=OrderedDict()
        #type: Dict[Role, LinkRole]
        """
        The links roles "opposite" to the objects sorted by 
        the "owned" roles. Note that the direction of the
        association is not taken into account. Only owned
        roles count to group links. Only valid linked role are 
        in this list. This variable is set by the object
        analyzer.
        """

    def cardinality(self, role):
        if role in self._link_roles_per_role:
            return len(self._link_roles_per_role[role])
        else:
            raise ValueError(
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
        #type: (Role) -> List[Link]
        """
        The list of links that are connected to the object and
        that are owned by the role.
        """

    @abstractmethod
    def isPlainObject(self):
        # This method is not really useful as isinstance can be used.
        # It is just used to prevent creating object of this class
        # (using ABCMeta is not enough to prevent this).
        raise NotImplementedError()

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


class _ClassPrint(object):
    """
    For a given object this is basically a
        Dict[attname,Optional[Text]] for each
    that is, a optional value for each attributes in the class.
    The value of slots are converted to Text to simplify implementation.
    This may cause problem with multiple textual representation but this
    is good enough at the time beeing.
    If an attribute has no slot return None.
    If "onlyIds" are specified only these attributes are selected.
    This class is usefull to compare objects and there ids.
    """
    def __init__(self, object, onlyIds=False, inherited=False):
        # TODO: care should be taken with inheritance (additional param?)
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


class PlainObject(Object):

    def __init__(self, model, name, class_,
                 package=None,
                 step=None,
                 lineNo=None, description=None, astNode=None):
        #type: (ObjectModel, Text, Union[Class, Placeholder], Optional[package], Optional['Step'], Optional[int], Optional['ASTNode'] )-> None
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

    def isPlainObject(self):
        return True


class Slot(ElementFromStep, Member):

    def __init__(self, object, attribute, simpleValue,
                 step=None,
                 description=None, lineNo=None, astNode=None):
        #type: (Object, Union[Attribute, Placeholder], DataValue,  Optional['Step'], Optional[TextBlock], Optional[int], 'ASTNode') -> None
        attribute_name=(
            attribute.placeholderValue
                if isinstance(attribute, Placeholder)
            else attribute.name
        )
        ElementFromStep.__init__(
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


class Link(PackagableElement, Entity):
    __metaclass__ = ABCMeta

    def __init__(self,
                 model, association,
                 sourceObject, targetObject,
                 name=None,
                 package=None,
                 step=None,
                 astNode=None, lineNo=None,
                 description=None):
        #type: (ObjectModel, Union[Association, Placeholder], Object, Object, Optional[Text], Optional[Package], Optional['Step'],Optional['ASTNode'], Optional[int], Optional[TextBlock]) -> None
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


        self.association=association
        #type: association

        self.sourceObject = sourceObject
        # type: Object

        self.targetObject = targetObject
        # type: Object

        model._links.append(self)

        # Singleton-like link roles to allow direct comparison
        # of link role instances. (see linkRole method)
        self._linkRole=OrderedDict()
        self._linkRole['source']=LinkRole(self, 'source')
        self._linkRole['target']=LinkRole(self, 'target')

    @abstractmethod
    def isPlainLink(self):
        # just used to prevent creating object of this class
        # (ABCMeta is not enough)
        raise NotImplementedError()

    def object(self, position):
        #type: () -> RolePosition
        if position=='source':
            return self.sourceObject
        elif position=='target':
            return self.targetObject
        else:
            raise NotImplementedError(
                'role position "%s" is not implemented' % position)

    def linkRole(self, position):
        return self._linkRole[position]

    def __str__(self):
        return '(%s,%s,%s)' % (
            self.sourceObject.name,
            self.association.name,
            self.targetObject.name
        )


class LinkRole(object):

    def __init__(self, link, position):
        self.link=link
        self.position=position

    @property
    def object(self):
        return self.link.object(self.position)

    @property
    def association(self):
        return self.link.association

    @property
    def role(self):
        return self.link.association.role(self.position)

    @property
    def roleType(self):
        return self.role.type

    @property
    def objectType(self):
        return self.object.class_

    @property
    def opposite(self):
        return self.link.linkRole(opposite(self.position))

    def __str__(self):
        if self.position=='source':
            return '([[%s]],%s,%s)' % (
                self.link.sourceObject.name,
                self.association.name,
                self.link.targetObject.name
            )
        elif self.position=='target':
            return '(%s,%s,[[%s]])' % (
                self.link.sourceObject.name,
                self.association.name,
                self.link.targetObject.name
            )
        else:
            raise NotImplementedError(
                'Unexpected position: %s' % self.position)


class PlainLink(Link):

    def __init__(self,
                 model, association,
                 sourceObject, targetObject,
                 name=None,
                 package=None,
                 step=None,
                 astNode=None, lineNo=None,
                 description=None):
        #type: (ObjectModel, Union[Association, Placeholder], Object, Object, Optional[Text], Optional[Package], Optional['Step'], Optional['ASTNode'], Optional[int], Optional[TextBlock]) -> None
        super(PlainLink, self).__init__(
            model=model,
            association=association,
            sourceObject=sourceObject,
            targetObject=targetObject,
            name=name,
            package=package,
            step=step,
            astNode=astNode,
            lineNo=lineNo,
            description=description
        )

    def isPlainLink(self):
        return True

    # def delete(self):
    #     self.state.links=[l for l in self.state.links if l != self]


class LinkObject(Object, Link):

    def __init__(self, model, associationClass,
                 sourceObject, targetObject,
                 name,
                 package=None,
                 step=None,
                 astNode=None, lineNo=None,
                 description=None):
        Object.__init__(
            self,
            model=model,
            name=name,
            class_=associationClass,
            package=package,
            step=step,
            astNode=astNode,
            lineNo=lineNo,
            description=description
        )
        # the linkObject has been added to _objectNamed

        Link.__init__(
            self,
            model=model,
            association=associationClass,
            sourceObject=sourceObject,
            targetObject=targetObject,
            name=name,
            package=package,
            step=step,
            astNode=astNode,
            lineNo=lineNo,
            description=description
        )
        # the linkObject has been added to _links

        # just make sure that the name of this link object is set.
        # This avoid relying on the implementation of Link constructor.
        # This could be an issue otherwize since link have no name.
        self.name=name


    # def delete(self):
    #     #TODO:  implement delete operation on link objects
    #     raise NotImplementedError('Delete operation on link object is not implemented')

    def isPlainLink(self):
        return False

    def isPlainObject(self):
        return False


class ObjectModelCopier(object):

    def __init__(self, source):
        self.o=source
        #type: ObjectModel

        self.t=ShadowObjectModel(classModel=source._classModel)
        #type: ObjectModel

        self._object_map=dict()

        #TODO: implement LinkObject

    def copy(self):
        self.t._classModel=self.o._classModel
        self.t.storyEvaluation=self.o.storyEvaluation
        for po in self.o.plainObjects:
            self._copy_plain_object(po)
        for l in self.o.plainLinks:
            self._copy_plain_link(l)
            # TODO: implement LinkObject
        return self.t

    def _copy_plain_object(self, plain_object):

        if plain_object.package is not None:
            raise NotImplementedError(
                'The usage of package is not supported yet')
        new_object = \
            PlainObject(
                model=self.t,
                name=plain_object.name,
                class_=plain_object.class_,
                package=plain_object.package,   # See exception above
                step=plain_object.step,   # this is ok since an object
                                    # is created only once
                lineNo=plain_object.lineNo,
                description=plain_object.description,
                astNode=plain_object.astNode)
        self._object_map[plain_object]=new_object
        for slot in plain_object.slots:
            self._copy_slot(slot, new_object)

    def _copy_slot(self, old_slot, new_object):
        new_slot=\
            Slot(
                object=new_object,
                attribute=old_slot.attribute,
                simpleValue=old_slot.simpleValue,
                step=old_slot.step,
                description=old_slot.description,
                lineNo=old_slot.lineNo,
                astNode=old_slot.astNode)

    def _copy_plain_link(self, plain_link):
        if plain_link.package is not None:
            raise NotImplementedError(
                'The usage of package is not supported yet')
        new_link= \
            PlainLink(
                model=self.t,
                name=plain_link.name,
                association=plain_link.association,
                sourceObject=self._object_map[plain_link.sourceObject],
                targetObject=self._object_map[plain_link.targetObject],
                package=plain_link.package,
                step=plain_link.step,
                astNode=plain_link.astNode,
                lineNo=plain_link.lineNo,
                description=plain_link.description)


METAMODEL = Metamodel(
    id='ob',
    label='object',
    extension='.obs',
    modelClass=ObjectModel
)
MetamodelDependency(
    sourceId='ob',
    targetId='gl',
    optional=True,
    multiple=True,
)
MetamodelDependency(
    sourceId='ob',
    targetId='ob',
    optional=True,
    multiple=True,
)
MetamodelDependency(
    sourceId='ob',
    targetId='cl',
    optional=False,
    multiple=True,
)