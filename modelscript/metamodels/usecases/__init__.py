# coding=utf-8


import collections

from typing import Dict, Text

from modelscript.base.issues import Issue, Levels
from modelscript.base.symbols import Symbol
from modelscript.megamodels.issues import ModelElementIssue
from modelscript.megamodels.elements import SourceModelElement
from modelscript.base.metrics import Metrics
from modelscript.megamodels.metamodels import Metamodel
from modelscript.megamodels.dependencies.metamodels import (
    MetamodelDependency)
from modelscript.megamodels.models import Model
from modelscript.metamodels.permissions.sar import Subject

META_CLASSES=(
    'UsecaseModel',
    'Usecase',
    'System',
    'Actor',
    'METAMODEL'
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
        return list(self.actorNamed.values())

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
        return list(self.usecaseNamed.values())


#TODO:3 it could make sense to have superSubject for superActor
# A super actor should logically be a super subject
# This imply adding superSubjects
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
