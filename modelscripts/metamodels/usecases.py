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
from modelscripts.megamodels.elements import ModelElement
from modelscripts.megamodels.dependencies.metamodels import (
    MetamodelDependency
)
from modelscripts.megamodels.models import Model
from modelscripts.metamodels.permissions.sar import Subject

__all__=(
    'UsecaseModel',
    'Usecase',
    'System',
    'Actor'
)

class UsecaseModel(Model):
    def __init__(self):
        super(UsecaseModel, self).__init__()

        self.system=System(self)
        """
        The system of the usecase model.
        It is created automatically now. This avoid to have None
        and then None exception in case of unfinished parsing.
        The value of the system are set later.
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
    def metrics(self):
        #type: () -> Metrics
        ms=super(UsecaseModel, self).metrics
        ms.addList((
            ('actor', len(self.actors)),
            ('system', 1 if self.isSystemDefined else 0 ),
            ('usecase', len(self.system.usecases))
        ))
        return ms

    def check(self):
        if not self.isSystemDefined:
            Issue(
                origin=self,
                level=Levels.Error,
                message=('No system defined')
            )
        else:
            if len(self.actors)==0:
                Issue(
                    origin=self,
                    level=Levels.Warning,
                    message=('No actor defined.')
                )
            else:
                for a in self.actors:
                    a.check()
                self.system.check()


class System(SourceModelElement):
    def __init__(self, usecaseModel):
        SourceModelElement.__init__(self,
            model=usecaseModel,
            name='*unknown*',
            code=None,
            lineNo=None,
            docComment=None, eolComment=None)

        self.usecaseModel = usecaseModel
        self.usecaseModel.system=self

        self.usecaseNamed = collections.OrderedDict()
        # type: Dict[str,Usecase]

    def setInfo(self, name, code=None, lineNo=None,
                docComment=None, eolComment=None
                ):
        super(System, self).__init__(
            model=self.usecaseModel,
            name=name,
            code=code,
            lineNo=lineNo,
            docComment=docComment, eolComment=eolComment)

    @property
    def usecases(self):
        return self.usecaseNamed.values()

    def check(self):
        if not Symbol.is_CamlCase(self.name):
            ModelElementIssue(
                model=self.usecaseModel,
                modelElement=self,
                level=Levels.Warning,
                message=(
                    '"%s" should be in CamlCase.'
                    % self.name))
        if len(self.usecases)==0:
            Issue(
                origin=self.usecaseModel,
                level=Levels.Warning,
                message=('No usecases defined in system "%s".' %
                         self.name)
            )
        else:
            for u in self.usecases:
                u.check()


class Actor(SourceModelElement, Subject):
    def __init__(self,
                 usecaseModel,
                 name,
                 kind='human',
                 code=None,
                 lineNo=None,
                 docComment=None,
                 eolComment=None):
        SourceModelElement.__init__(self,
            model=usecaseModel,
            name=name,
            code=code,
            lineNo=lineNo,
            docComment=docComment,
            eolComment=eolComment)

        self.usecaseModel = usecaseModel
        self.usecaseModel.actorNamed[name]=self
        self.kind=kind # system|human
        self.superActors=[]
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

    def check(self):
        if not Symbol.is_CamlCase(self.name):
            ModelElementIssue(
                model=self.usecaseModel,
                modelElement=self,
                level=Levels.Warning,
                message=(
                    '"%s" should be in CamlCase.'
                    % self.name))
        if len(self.usecases)==0:
            ModelElementIssue(
                model=self.usecaseModel,
                modelElement=self,
                level=Levels.Warning,
                message='"%s" does not perform any usecase.' %
                    self.name
            )


class Usecase(SourceModelElement, Subject):
    def __init__(self,
                 system,
                 name,
                 code=None, lineNo=None, docComment=None, eolComment=None):

        SourceModelElement.__init__(self,
            model=system.model,
            name=name,
            code=code,
            lineNo=lineNo,
            docComment=docComment,
            eolComment=eolComment)
        self.system = system
        self.system.usecaseNamed[name]=self
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

    def check(self):
        if not Symbol.is_CamlCase(self.name):
            ModelElementIssue(
                model=self.system.usecaseModel,
                modelElement=self,
                level=Levels.Warning,
                message=(
                    '"%s" should be in CamlCase.'
                    % self.name))
        if len(self.actors)==0:
            ModelElementIssue(
                model=self.system.usecaseModel,
                modelElement=self,
                level=Levels.Warning,
                message='No actor performs "%s".' %
                        self.name
            )



METAMODEL = Metamodel(
    id='us',
    label='usecase',
    extension='.uss',
    modelClass=UsecaseModel,
    modelKinds=('', 'preliminary', 'detailled')
)
MetamodelDependency(
    sourceId='us',
    targetId='gl',
    optional=True,
    multiple=True,
)

