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


from collections import OrderedDict
from typing import List, Optional, Dict, Text
from abc import ABCMeta

# TODO:4 to be continued
from modelscript.megamodels.py import (
    MAttribute
)
from modelscript.megamodels.elements import SourceModelElement
from modelscript.base.metrics import Metrics
from modelscript.megamodels.metamodels import Metamodel
from modelscript.megamodels.models import (
    Model)
from modelscript.megamodels.dependencies.metamodels import (
    MetamodelDependency
)
# used for typing
from modelscript.metamodels.classes import (
    ClassModel,
    METAMODEL as CLASS_METAMODEL
)

__all__=(
    'ObjectModel',
    'ShadowObjectModel',
    'ElementFromOptionalStep',

    'Package',
    'PackagableElement',

    'ResourceInstance',

    'Entity',
    'Member',
)


class ObjectModel(Model):
    """Object model, either created "manually" or via a story evaluation.
    See ShadowObjectModel for story evaluation.
    """

    packageNamed: Dict[str, 'Package']
    """ALL packages, not only the top level ones"""

    _plainObjectNamed: Dict[str, 'PlainObject']
    """Dictionary of plain objects. 
    No link objects.
    """

    _plainLinks: List['PlainLink']
    """Plain links. 
    No link objects. By contrast to other properties 
    such as plainObjectNamed, this is not a dictionary since
    links are not named.
    """

    _linkObjectNamed: Dict[str, 'LinkObject']
    """Link objects. """

    _classModel: Optional[ClassModel]
    """Class model on which the object model is based on."""

    storyEvaluation: Optional['StoryEvaluation']
    """Story evaluation if this model is the result of a
    story evaluation. Otherwise this is most probably a handmade model
    illed by object parser.
    """

    checkStepEvaluation: Optional['CheckStepEvaluation']
    """Filled only if this model is the result of a Check
    evaluation in a story.
    """

    stateCheck:  Optional['StateCheck']
    """Filled by finalize')"""

    def __init__(self):
        super(ObjectModel, self).__init__()

        self.packageNamed = OrderedDict()
        self._plainObjectNamed = OrderedDict()
        self._plainLinks = []
        self._linkObjectNamed = OrderedDict()

        # Class model. filled by property classModel
        self._classModel = None

        self.storyEvaluation = None
        self.checkStepEvaluation = None
        self.stateCheck = None


    def copy(self):
        """
        Return a ShadowObjectModel with the same content and
        the same classModel
        """
        from modelscript.metamodels.objects.copier import (
            ObjectModelCopier)
        return ObjectModelCopier(self).copy()

    @property
    def classModel(self) -> ClassModel:
        if self._classModel is None:
            self._classModel = self.theModel(CLASS_METAMODEL)
        return self._classModel

    @property
    def hasClassModel(self) -> bool :
        try:
            self.classModel
            return True
        except ValueError:
            return False

    # -------------------------------------------------------------------
    #    plainObjects
    # -------------------------------------------------------------------

    @property
    def plainObjects(self):
        return list(self._plainObjectNamed.values())

    @property
    def plainObjectNames(self):
        return list(self._plainObjectNamed.keys())

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
        return list(self._linkObjectNamed.values())

    @property
    def linkObjectNames(self):
        return list(self._linkObjectNamed.keys())

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
        po = self.plainObject(name)
        if po is not None:
            return po
        else:
            return self.linkObject(name)

    @property
    def links(self):
        return self.plainLinks+self.linkObjects

    def classExtension(self, class_: 'Class') -> List['Object']:
        # TODO:2 add inheritance in classExtension
        return [
            o for o in self.objects if o.class_==class_]

    @property
    def story(self) -> Optional['Story']:
        """ Return None if the ObjectModel does not result from
        a story evaluation. Otherwise return the corresponding
        story.
        """
        if self.storyEvaluation is None:
            return None
        else:
            return self.storyEvaluation.step

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
    def metamodel(self) -> Metamodel:
        return METAMODEL

    def finalize(self):
        from modelscript.metamodels.objects.statechecker import (
            StateCheck
        )
        print('.'*30, '>>>> ObjectModel.FINALIZE()')
        print('.'*30, '    >>>> ANALYZING OBJECT MODEL')
        self.stateCheck=StateCheck(self)
        self.stateCheck.check()
        print('.'*30, '    <<<< OBJECT MODEL ANALYZED')
        super(ObjectModel, self).finalize()
        print('.'*30, '<<<< ObjectModel.FINALIZE()')


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


class ElementFromOptionalStep(SourceModelElement, metaclass=ABCMeta):
    """
    Superclass of all source model elements that can (optionaly)
    originates from a story step (hence "FromOriginalStep').
    Element create "manually" in standard object model will have None
    as a step value. By contrasts elements created from a story will
    have a step value.
    In practice this clas basically serves to add a "step" attribute
    to all subclasses and to compute location attributes accordingly.
    """

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


class PackagableElement(ElementFromOptionalStep, metaclass=ABCMeta):
    """
    Top level element.
    """

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


class ResourceInstance(object, metaclass=ABCMeta):
    """ 
    Currently not used, but can be useful to describes
    access instances. 
    This corresponds to the instance level of Resource.
    See modelscript.metamodels.permissions.sar.Resource
    """


class Entity(ResourceInstance, metaclass=ABCMeta):
    pass


class Member(ResourceInstance, metaclass=ABCMeta):
    pass


# TODO:3 generalize and improve "package" management over languages
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