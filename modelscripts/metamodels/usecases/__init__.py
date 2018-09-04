# coding=utf-8
from __future__ import print_function

import collections

from typing import Dict, Text

from modelscripts.base.issues import Issue, Levels
from modelscripts.base.symbols import Symbol
from modelscripts.megamodels.issues import ModelElementIssue
from modelscripts.megamodels.elements import SourceModelElement
from modelscripts.base.metrics import Metrics
from modelscripts.megamodels.metamodels import Metamodel
from modelscripts.megamodels.dependencies.metamodels import (
    MetamodelDependency)
from modelscripts.megamodels.models import Model
from modelscripts.metamodels.permissions.sar import Subject

META_CLASSES=(
    'UsecaseModel',
    'Usecase',
    'System',
    'Actor'
)

__all__= META_CLASSES


class UsecaseModel(Model):

    META_COMPOSITIONS=[
        'actors',
        'system',
    ]

    def __init__(self):
        super(UsecaseModel, self).__init__()

        self.system=System(self)
        """
        The system of the usecase model.
        It is created automatically during initialization.
        This avoid to have None and then None exception 
        in case of unfinished parsing.
        The value of the system is set later.
        Use 'isSystemDefined' to check if the system has been
        defined in the model.
        """

        self.actorNamed = collections.OrderedDict()
        # type: Dict[Text, Actor]

    @property
    def isSystemDefined(self):
        return self.system.name!='*unknown*'

    @property
    def metamodel(self):
        #type: () -> Metamodel
        return METAMODEL

    @property
    def actors(self):
        return self.actorNamed.values()

    @property
    def nbOfInteractions(self):
        n=0
        for a in self.actors:
            n += len(a.usecases)
            return n

    @property
    def metrics(self):
        #type: () -> Metrics
        ms=super(UsecaseModel, self).metrics
        ms.addList((
            ('actor', len(self.actors)),
            ('system', 1 if self.isSystemDefined else 0 ),
            ('usecase', len(self.system.usecases))
        ))
        return ms




class System(SourceModelElement):

    META_COMPOSITIONS = [
        'usecases',
    ]

    def __init__(self, usecaseModel):
        SourceModelElement.__init__(self,
            model=usecaseModel,
            name='*unknown*',
            astNode=None)

        self.usecaseModel = usecaseModel
        self.usecaseModel.system=self

        self.usecaseNamed = collections.OrderedDict()
        # type: Dict[str,Usecase]

        self.impliciteDeclaration = True

    def setInfo(self, name,
                implicitDeclaration=True,
                astNode=None
                ):
        super(System, self).__init__(
            model=self.usecaseModel,
            name=name,
            astNode=astNode)

        self.implicitDeclaration=implicitDeclaration

    @property
    def usecases(self):
        return self.usecaseNamed.values()

    # def check(self):
    #     # if not Symbol.is_CamlCase(self.name):
    #     #     ModelElementIssue(
    #     #         modelElement=self,
    #     #         level=Levels.Warning,
    #     #         message=(
    #     #             '"%s" should be in CamlCase.'
    #     #             % self.name))
    #     if len(self.usecases)==0:
    #         Issue(
    #             origin=self.usecaseModel,
    #             level=Levels.Warning,
    #             message=('No usecases defined in system "%s".' %
    #                      self.name)
    #         )
    #     else:
    #         for u in self.usecases:
    #             u.check()


class Actor(SourceModelElement, Subject):
    def __init__(self,
                 usecaseModel,
                 name,
                 kind='human',
                 implicitDeclaration=False,
                 astNode=None):
        SourceModelElement.__init__(self,
                                    model=usecaseModel,
                                    name=name,
                                    astNode=astNode)

        self.usecaseModel = usecaseModel
        self.usecaseModel.actorNamed[name]=self
        self.kind=kind # system|human  human is default
        self.implicitDeclaration=implicitDeclaration
        self.superActors=[]  # strings during parsing
        self.subActors=[]
        self.usecases=[]

    def addUsecase(self, usecase):
        if usecase in self.usecases:
            return
        else:
            usecase.actors.append(self)
            self.usecases.append(usecase)

    def addSuperActor(self, actor):
        if actor in self.superActors:
            return
        else:
            actor.subActors.append(self)
            self.superActors.append(actor)

    # def check(self):
        # if not Symbol.is_CamlCase(self.name):
        #     ModelElementIssue(
        #         modelElement=self,
        #         level=Levels.Warning,
        #         message=(
        #             '"%s" should be in CamlCase.'
        #             % self.name))
        # if len(self.usecases)==0:
        #     ModelElementIssue(
        #         modelElement=self,
        #         level=Levels.Warning,
        #         message='"%s" does not perform any usecase.' %
        #             self.name
        #     )


class Usecase(SourceModelElement, Subject):
    def __init__(self,
                 system,
                 name,
                 implicitDeclaration=False,
                 astNode=None):

        SourceModelElement.__init__(self,
                                    model=system.model,
                                    name=name,
                                    astNode=astNode)
        self.system = system
        self.system.usecaseNamed[name]=self
        self.implicitDeclaration=implicitDeclaration
        self.actors=[]

    @property
    def superSubjects(self):
        return self.actors

    def addActor(self, actor):
        if actor in self.actors:
            return
        else:
            actor.usecases.append(self)
            self.actors.append(actor)

    # def check(self):
    #     if not Symbol.is_CamlCase(self.name):
    #         ModelElementIssue(
    #             modelElement=self,
    #             level=Levels.Warning,
    #             message=(
    #                 '"%s" should be in CamlCase.'
    #                 % self.name))
    #     if len(self.actors)==0:
    #         ModelElementIssue(
    #             modelElement=self,
    #             level=Levels.Warning,
    #             message='No actor performs "%s".' %
    #                     self.name
    #         )



METAMODEL = Metamodel(
    id='us',
    label='usecase',
    extension='.uss',
    modelClass=UsecaseModel,
    modelKinds=('preliminary', '', 'detailed')
)
MetamodelDependency(
    sourceId='us',
    targetId='gl',
    optional=True,
    multiple=True,
)
MetamodelDependency(
    sourceId='us',
    targetId='pa',
    optional=True,
    multiple=True,
)
