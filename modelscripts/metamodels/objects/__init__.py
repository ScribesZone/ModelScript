# coding=utf-8

"""
Simple metamodel for object states. The metamodel
represents two views:
* an abstract view in which object/slots and links are
  represented without and order,
* a story view that represents the same entities but
  as they are defined, as in a story, in a sequential order
  and with Annotated OBject (AOB) text blocks, that is text
  blocks nested definitions.


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

    Story view
        Definition
        <|-- CoreDefinition
             <|-- Object
             <|-- Slot
             <|-- Link
        <|-- AnnotatedTextBlock
            <>--* CoreDefinition
"""


from collections import OrderedDict
from typing import List, Optional, Dict, Text, Union
import abc

# TODO: to be continued
from modelscripts.megamodels.py import (
    MComposition,
    MReference,
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
    Class,
    Attribute,
    Association
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
    'BasicValue',
    'Slot',
    'Link',
    'PlainLink',
    'LinkObject',
)


class ObjectModel(Model):

    def __init__(self):
        super(ObjectModel, self).__init__()

        # ALL packages, not only the top level ones
        self.packageNamed=OrderedDict() #type: Dict[Text, Package]

        self._objectNamed = OrderedDict()
        # type: Dict[Text, Object]
        """
        All objects (plain objects and link objects).
        Link object are also registered in _links.
        This serve the abstract view of the model:
        there is no indication about the definition order
        with other definitions.
        """

        self._links=[]
        # type: List[Link]
        """
        All plain links (no link object).
        Link object are also regitered in _objectNamed.
        This serve the abstract view of the model:
        there is no indication about the definition order
        with other definitions.
        """

        self.definitions=[]
        #type: List[Definition]
        """
        The list of all "top level" definitions  
        in the order of the "story".
        """


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
    def annotatedTextBlocks(self):
        # type: () -> List[AnnotatedTextBlock]
        return [
            l for l in self.definitions
            if isinstance(l, AnnotatedTextBlock) ]

    @property
    def metrics(self):
        #type: () -> Metrics
        ms=super(ObjectModel, self).metrics
        ms.addList((
            ('object', len(self.objects)),
            ('link', len(self.links)),
            ('plain object', len(self.plainObjects)),
            ('plain link', len(self.plainLinks)),
            ('linkObject', len(self.linkObjects)),
            ('slot',sum(
                len(o.slots)
                for o in self.objects)),
            ('annotated text block', len(self.annotatedTextBlocks))
        ))
        return ms

    @property
    def metamodel(self):
        #type: () -> Metamodel
        return METAMODEL


class PackagableElement(SourceModelElement):
    """
    Top level element.
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self,
                 name,
                 model,
                 package=None,
                 lineNo=None, astNode=None, description=None):
        super(PackagableElement, self).__init__(
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


class Definition(object):
    pass

class CoreDefinition(Definition):
    """
    Elements that can be in Annotated Text Blocks:
    * objects
    * slots
    * links
    * link objects
    Their container can be either the model (container attribute
    set to None) or an annotated source.
    """

    def __init__(self, container):
        self.container=container
        #type: Optional[AnnotatedTextBlock]
        """
        None if the definition is at the top level.
        The containing annotated text block otherwize
        """
        if self.container is not None:
            self.container.definitions.append(self)


class ResourceInstance:
    __metaclass__ = abc.ABCMeta
    """ 
    Currently not used, but can be useful to describes
    access instances. 
    This corresponds to the instance level of Resource.
    See modelscripts.metamodels.permissions.sar.Resource
    """


class Entity(ResourceInstance, CoreDefinition):
    __metaclass__ = abc.ABCMeta

    def __init__(self, container):
        #type: (Optional[AnnotatedTextBlock]) -> None
        CoreDefinition.__init__(self,
            container=container)

class Member(ResourceInstance, CoreDefinition):
    __metaclass__ = abc.ABCMeta

    def __init__(self, container):
        # type: (Optional[AnnotatedTextBlock]) -> None
        CoreDefinition.__init__(self,
            container=container)


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
                 lineNo=None, astNode=None, description=None):
        PackagableElement.__init__(
            self,
            name=name,
            model=model,
            package=package,
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
    __metaclass__ = abc.ABCMeta

    def __init__(self, model, name, class_,
                 container=None,
                 package=None,
                 lineNo=None, description=None, astNode=None):
        #type: (ObjectModel, Text, Union[Class, Placeholder], Optional[AnnotatedTextBlock], Optional[package], Optional[int], Optional[TextBlock], Optional['ASTNode'] )-> None
        PackagableElement.__init__(
            self,
            model=model,
            name=name,
            package=package,
            astNode=astNode,
            lineNo=lineNo,
            description=description
        )
        Entity.__init__(self, container)

        self.class_ = class_
        #type: Union[Placeholder, Class]

        self.slotNamed = OrderedDict()
        #type: Dict[Text, Slot]
        # Slots of the object indexed by attribute name (not attribute)

        #TODO: check for duplicates to avoid loosing objects
        # Register the object in the model for the abstract view
        model._objectNamed[name]=self

        if container is None:
            # Register the object definition to the top level
            model.definitions.append(self)

    @property
    def slots(self):
        return list(self.slotNamed.values())

    # def delete(self):
    #     #TODO:  implement delete operation on objects
    #
    #     raise NotImplementedError('Delete operation on objects is not implemented')



class PlainObject(Object):

    def __init__(self, model, name, class_, container=None,
                 package=None,
                 lineNo=None, description=None, astNode=None):
        #type: (ObjectModel, Text, Union[Class, Placeholder], Optional[package], Optional[int], Optional[AnnotatedTextBlock], Optional['ASTNode'] )-> None
        super(PlainObject, self).__init__(
            model=model,
            container=container,
            name=name,
            class_=class_,
            package=package,
            astNode=astNode,
            lineNo=lineNo,
            description=description
        )



BasicValue=Union[Text, 'Bool', int, float]



class Slot(SourceModelElement, Member):

    def __init__(self, object, attribute, value, container=None,
                 description=None, lineNo=None, astNode=None):
        #type: (Object, Union[Attribute, Placeholder], BasicValue, Optional[AnnotatedTextBlock], Optional[TextBlock], Optional[int], 'ASTNode') -> None
        attribute_name=(
            attribute.placeholderValue
                if isinstance(attribute, Placeholder)
            else attribute.name
        )
        SourceModelElement.__init__(
            self,
            model=object.model,
            name='%s.%s' % (object.name, attribute_name),
            astNode=astNode,
            lineNo=lineNo,
            description=description)
        Member.__init__(self, container)
        self.object=object

        self.attribute=attribute
        self.value=value
        object.slotNamed[attribute_name]=self

        if container is None:
            # Register the object definition to the top level
            object.model.definitions.append(self)


class Link(PackagableElement, Entity):
    __metaclass__ = abc.ABCMeta

    def __init__(self,
                 model, association,
                 sourceObject, targetObject,
                 name=None,
                 container=None,
                 package=None,
                 astNode=None, lineNo=None,
                 description=None):
        #type: (ObjectModel, Union[Association, Placeholder], Object, Object, Optional[Text], Optional[AnnotatedTextBlock], Optional[Package], Optional['ASTNode'], Optional[int], Optional[TextBlock]) -> None
        PackagableElement.__init__(
            self,
            model=model,
            name=name,
            package=package,
            astNode=astNode,
            lineNo=lineNo,
            description=description
        )
        Entity.__init__(self, container=container)

        self.association=association
        #type: association

        self.sourceObject = sourceObject
        # type: Object

        self.targetObject = targetObject
        # type: Object

        model._links.append(self)

        if container is None:
            # Register the link definition to the top level
            model.definitions.append(self)


class PlainLink(Link):

    def __init__(self,
                 model, association,
                 sourceObject, targetObject,
                 name=None,
                 container=None,
                 package=None,
                 astNode=None, lineNo=None,
                 description=None):
        #type: (ObjectModel, Union[Association, Placeholder], Object, Object, Optional[Text], Optional[AnnotatedTextBlock], Optional[Package], Optional['ASTNode'], Optional[int], Optional[TextBlock]) -> None
        super(PlainLink, self).__init__(
            model=model,
            association=association,
            sourceObject=sourceObject,
            targetObject=targetObject,
            name=name,
            container=container,
            package=package,
            astNode=astNode,
            lineNo=lineNo,
            description=description
        )

    # def delete(self):
    #     self.state.links=[l for l in self.state.links if l != self]



class LinkObject(Object, Link):

    def __init__(self, model, associationClass,
                 sourceObject, targetObject,
                 name,
                 package=None,
                 astNode=None, lineNo=None,
                 description=None):
        Object.__init__(
            self,
            model=model,
            name=name,
            class_=associationClass,
            package=package,
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



class AnnotatedTextBlock(SourceModelElement, Definition):
    """
    Annotated text block container core definitions.
    """
    def __init__(self,
                 model,
                 textBlock=None,
                 astNode=None, lineNo=None):
        #type: (ObjectModel, TextBlock, Optional[Package], Optional['ASTNode'], Optional[int]) -> None
        super(AnnotatedTextBlock, self).__init__(
            model=model,
            astNode=astNode,
            lineNo=lineNo
        )
        self.textBlock=textBlock
        #type: Optional[TextBlock]
        # will be set later.

        self.definitions=[]
        #type: List[TextBlock]

        model.definitions.append(self)



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