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
from typing import List, Optional, Dict, Text
from abc import ABCMeta

# TODO: to be continued
from modelscripts.megamodels.py import (
    MAttribute
)
from modelscripts.megamodels.elements import SourceModelElement
from modelscripts.base.metrics import Metrics
from modelscripts.megamodels.metamodels import Metamodel
from modelscripts.megamodels.models import (
    Model)
from modelscripts.megamodels.dependencies.metamodels import (
    MetamodelDependency
)
# used for typing
from modelscripts.metamodels.classes import (
    ClassModel,
    Class,
    METAMODEL as CLASS_METAMODEL
)

__all__=(
    'ObjectModel',
    'ShadowObjectModel',
    'ElementFromOptionalStep',
    'PackagableElement',
    'ResourceInstance',

    'Entity',
    'Member',

    'Package',
)


class ObjectModel(Model):

    """
    Object model, either create "manually" or via a story evaluation.
    See ShadowObjectModel for story evaluation.
    """

    def __init__(self):
        super(ObjectModel, self).__init__()

        # ALL packages, not only the top level ones
        self.packageNamed=OrderedDict() #type: Dict[Text, Package]

        self._plainObjectNamed = OrderedDict()
        # type: Dict[Text, 'PlainObject']
        """
        Plain objects. No link objects.
        """

        self._plainLinks=[]
        # type: List['PlainLink']
        """
        Plain links (no link object).
        """

        self._linkObjectNamed = OrderedDict()
        # type: Dict[Text, 'LinkObject']
        """
        Link objects.
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
        from modelscripts.metamodels.objects.copier import (
            ObjectModelCopier)
        return ObjectModelCopier(self).copy()

    @property
    def classModel(self):
        #type: ()-> ClassModel
        if self._classModel is None:
            self._classModel=self.theModel(CLASS_METAMODEL)
        return self._classModel

    @property
    def plainObjects(self):
        return self._plainObjectNamed.values()

    @property
    def plainObjectNames(self):
        return self._plainObjectNamed.keys()

    def plainObject(self, name):
        if name in self._plainObjectNamed:
            return self._plainObjectNamed[name]
        else:
            return None

    @property
    def plainLinks(self):
        return self._plainLinks

    @property
    def linkObjects(self):
        return self._linkObjectNamed.values()

    @property
    def linkObjectNames(self):
        return self._linkObjectNamed.keys()

    def linkObject(self, name):
        if name in self._linkObjectNamed:
            return self._linkObjectNamed[name]
        else:
            return None

    @property
    def objects(self):
        return self.plainObjects+self.linkObjects

    @property
    def objectNames(self):
        return self.plainObjectNames+self.linkObjectNames

    def object(self, name):
        po=self.plainObject(name)
        if po is not None:
            return po
        else:
            return self.linkObject(name)

    @property
    def links(self):
        return self.plainLinks+self.linkObjects

    def classExtension(self, class_): #TODO: inheritance
        #type: (Class)-> List['Object']
        return [
            o for o in self.objects if o.class_==class_]

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
        print('.'*30,'>>>> ObjectModel.FINALIZE()')
        print('.'*30,'    >>>> ANALYZING OBJECT MODEL')
        self.analyzis=ObjectModelAnalyzis(self)
        self.analyzis.analyze()
        print('.'*30,'    <<<< OBJECT MODEL ANALYZED')
        super(ObjectModel, self).finalize()
        print('.'*30,'<<<< ObjectModel.FINALIZE()')


class ShadowObjectModel(ObjectModel):
    """
    Object model created or copied without any impact on the
    megamodel. No dependencies are created. ShadowObjectModel
    serves to represent intermediate state of stories.
    Their import box is empty, so there is no dependency to
    other model. The class model is an exception :the class model
    must be given explicitely since it is used to build
    ObjectModelAnalsysis.
    """
    def __init__(self, classModel):
        super(ShadowObjectModel, self).__init__()
        self._classModel=classModel


class ElementFromOptionalStep(SourceModelElement):
    """
    Superclass of all source model elements that can (optionaly)
    originates from a story step (hence "FromOriginalStep').
    Element create "manually" in standard object model will have None
    as a step value. By contrasts elements created from a story will
    have a step value.
    In practice this clas basically serves to add a "step" attribute
    to all subclasses and to compute location attributes accordingly.
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
        :param name:
            The name of the source element.
        :param model:
            The object model
        :param step:
            The step, if any, from where this element originates/
        :param astNode:
            The ast node, or None. step.astNode takes precedence.
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
        super(ElementFromOptionalStep, self).__init__(
            model=model,
            name=name,
            astNode=ast_node,
            lineNo=line_no, description=description_)
        self.step=step


class PackagableElement(ElementFromOptionalStep):
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