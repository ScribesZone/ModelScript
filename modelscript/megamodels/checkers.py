# coding=utf-8
"""Library to define model checkers of various kind."""

from typing import Dict, List, ClassVar
import collections
from abc import ABCMeta, abstractmethod


from modelscript.base.issues import (
    Levels)
from modelscript.megamodels.issues import (
    ModelElementIssue)
from modelscript.base.exceptions import (
    MethodToBeDefined,
    UnexpectedCase)

__all__ = (
    'CheckOutput',
    'CheckList',
    'Checker',
    'PassChecker',
    'NamingChecker',
    'LimitsChecker'
)

DEBUG = 0


class Checker(object, metaclass=ABCMeta):
    def __init__(self, **params):
        # type : (List['MetaClass'], Text, Level, Optional[Dict[Text, Any]]) -> None
        self.params = params
        self.name = type(self).__name__
        if 'metaclasses' not in params:
            raise ValueError(  # raise;TODO:3
                '%s do not define metaclasses' % self.name)
        self.metaclasses = params.get('metaclasses')
        self.level = params.get('level', Levels.Error)
        CheckList.registerChecker(self)


    def doCheck(self, e):
        raise MethodToBeDefined(  # raise:TODO:3
            'CKK: Checker %s on %s is not implemented ' % (
                self.name,
                type(e).__name__
            ))


class CheckOutput(object):
    def __init__(self, message, locationElement=None):
        self.message=message
        self.locationElement = locationElement


class CheckList(object):

    checkersForClass: ClassVar[Dict['MetaClass', List[Checker]]] \
        = collections.OrderedDict()

    @classmethod
    def registerChecker(cls, checker):
        if DEBUG >= 1:
            print('CKK: register %s [%s]' % (
                  checker.name,
                  ', '.join(
                      [mc.__name__ for mc in checker.metaclasses])
                  ))
        for c in checker.metaclasses:
            cbc=CheckList.checkersForClass
            if c not in cbc:
                cbc[c]=[]

            cbc[c].append(checker)

    @classmethod
    def check(cls, element):
        c=type(element)
        if DEBUG >= 3:
            print('CKK: CHECKING %25s' % c.__name__, end='')
        if c in CheckList.checkersForClass:
            checkers = CheckList.checkersForClass[c]
            if DEBUG >= 3:
                print('-> [%s]' % (
                    ','.join([c.name for c in checkers])))
            for checker in checkers:
                check_output=checker.doCheck(element)
                metaclasses_part='_'.join(
                    [mc.__name__ for mc in checker.metaclasses])
                code = 'cck.%s.%s' % (
                    metaclasses_part,
                    checker.__class__.__name__)
                if check_output is not None:
                    ModelElementIssue(
                        modelElement=element,
                        code=code,
                        level=checker.level,
                        message=check_output.message,
                        locationElement=
                            check_output.locationElement
                    )
        else:
            if DEBUG >= 3:
                print('-> []')


class PassChecker(Checker):
    def __init__(self, **params):
        Checker.__init__(self, **params)

    def doCheck(self, e):
        pass


class NamingChecker(Checker, metaclass=ABCMeta):
    def __init__(self, fun, namingName, **params):
        Checker.__init__(self, **params)
        self.fun = fun
        self.namingName = namingName

    def doCheck(self, e):
        if not self.fun(e.name):
            return CheckOutput(
                message='"%s" should be in %s.' % (
                    e.name,
                    self.namingName),
                locationElement=self.locationElement(e))

    def locationElement(self, e):
        """
        This method can be overloaded if a location
        element is known
        """
        return e


class LimitsChecker(Checker, metaclass=ABCMeta):
    def __init__(self, label, **params):
        Checker.__init__(self, label=label, **params)
        self.label=label
        self.min = self.params['min']
        self.max = self.params['max']

    @abstractmethod
    def size(self, e):
        raise MethodToBeDefined( #raise: TODO:3
            'size() not implemented.')

    def doCheck(self, e):
        l=self.size(e)
        if l<self.min:
            msg = ('At least %s %s(s) must be defined. Got %s.' % (
                    self.min,
                    self.label,
                    l))
            return CheckOutput(
                message=msg,
                locationElement=self.locationElement(e)
            )
        if l>self.max:
            msg = ('At most %s %s(s) must be defined. Got %s.' %(
                    self.max,
                    self.label,
                    l))
            return CheckOutput(
                message=msg,
                locationElement=self.locationElement(e)
            )

    def locationElement(self, e):
        """
        This method can be overloaded if a location
        element is known
        """
        return e