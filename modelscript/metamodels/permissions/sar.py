# coding=utf-8

import abc
from abc import ABCMeta
from typing import List, Dict, Text


def _getNaming(o):
    for att in ['label', 'name', 'id', '__str__', '__repr__']:
        if hasattr(o, att):
            return getattr(o, att)
    return id(o)


class Subject(object):
    __metaclass__ = ABCMeta

    @property
    def superSubjects(self):
        """ Direct parents """
        # type: () -> List[Subject]
        return []

    @property
    def allSuperSubjects(self):
        # type: () -> List[Subject]
        """ All supersubject recursively + this one"""
        parents = self.superSubjects
        _=[self]
        for p in parents:
            _.extend(p.allSuperSubjects)
        return _

    @property
    def subjectLabel(self):
        return _getNaming(self)

    def __str__(self):
        return self.subjectLabel


class Action(object):
    _actionNamed = {}  # type: Dict[Text, Action]

    @classmethod
    def named(cls, name):
        return Action._actionNamed[name]

    def __init__(self, name, value):
        self.value = value
        self.name = name
        Action._actionNamed[self.name] = self

    @property
    def actionLabel(self):
        return self.name

    @property
    def superActions(self):
        """ Direct parents """
        # type: () -> List[Action]
        return []

    @property
    def allSuperActions(self):
        """ All superactions recursively + this one"""
        # type: () -> List[Action]
        acs = self.superActions
        return [self]+acs+ [a.superActions for a in acs]

    def __str__(self):
        return self.actionLabel


class Resource(object):
    __metaclass__ = abc.ABCMeta

    @property
    def resourceLabel(self):
        return _getNaming(self)

    @property
    def superResources(self):
        """ Direct parents """
        # type: () -> List[Resource]
        return []

    @property
    def allSuperResources(self):
        # type: () -> List[Resource]
        """ All superresources recursively + this one"""
        rs = self.superResources
        return [self] + rs + [r.allSuperResources for r in rs]

    def __str__(self):
        return self.resourceLabel


class SAR(object):
    """
    Subject-Action-Resource triplet.
    """

    __metaclass__ = ABCMeta

    def __init__(self, subject, action, resource):
        #type: (Subject, Action, Resource) -> None
        self.subject=subject #type: Subject
        self.action=action #type: Action
        self.resource=resource #type: Resource

    def __str__(self):
        return '%s %s %s' % (
            self.subject.subjectLabel,
            self.action.actionLabel,
            self.resource.resourceLabel
        )




