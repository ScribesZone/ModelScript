# coding=utf-8
from typing import Text, Dict, List, Any, Optional
import collections
from abc import ABCMeta, abstractmethod


from modelscripts.base.issues import (
    Level,
    Levels
)
from modelscripts.megamodels.issues import (
    ModelElementIssue
)

DEBUG=3

class CheckList(object):

    checkersForClass=collections.OrderedDict()
    #type: Dict['MetaClass', List[Checker]]

    @classmethod
    def registerChecker(cls, checker):
        if DEBUG >= 1:
            print('ckk: register %s [%s]' % (
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
        if DEBUG>=3:
            print('ckk: Checking element')
            print('ckk:     metaclass is: %s' % c.__name__ )
            # print('ckk:     element is  : '+str(element))
        if c in CheckList.checkersForClass:
            checkers=CheckList.checkersForClass[c]
            if DEBUG>=3:
                print('ckk:     checkers: %s' % (
                    ','.join([c.name for c in checkers])))
            for checker in checkers:
                msg=checker.doCheck(element)
                if msg is not None:
                    ModelElementIssue(
                        modelElement=element,
                        level=checker.level,
                        message=msg
                    )
        else:
            if DEBUG>=3:
                print('ckk:     no checker found.')


class Checker(object):
    __metaclass__ = ABCMeta

    def __init__(self, **params):
        # type : (List['MetaClass'], Text, Level, Optional[Dict[Text, Any]]) -> None
        self.params=params
        self.name=type(self).__name__
        if 'metaclasses' not in params:
            raise ValueError(
                '%s do not define metaclasses' % self.name)
        self.metaclasses=params.get('metaclasses')
        self.level=params.get('level', Levels.Error)
        CheckList.registerChecker(self)


    def doCheck(self, e):
        raise NotImplementedError(
            'Checker %s on %s is not implemented ' % (
                self.name,
                type(e).__name__
            ))


class NamingChecker(Checker):
    __metaclass__ = ABCMeta

    def __init__(self, fun, namingName, **params):
        Checker.__init__(self, **params)
        self.fun=fun
        self.namingName=namingName

    def doCheck(self, e):
        if not self.fun(e.name):
            return (
                '"%s" should be in %s.' % (
                e.name,
                self.namingName))


class LimitsChecker(Checker):
    __metaclass__ = ABCMeta

    def __init__(self, label, **params):
        Checker.__init__(self, label=label, **params)
        self.label=label
        self.min=self.params['min']
        self.max=self.params['max']
        print('UUUUUUUUUUUUUUUUU')
        print self.min

    @abstractmethod
    def size(self, e):
        raise NotImplementedError()

    def doCheck(self, e):
        l=self.size(e)
        if l<self.min:
            return (
                'At least %s %s(s) must be defined. Got %s.' %(
                    self.min,
                    self.label,
                    l
                )
            )
        if l>self.max:
            return (
                'At most %s %s(s) must be defined. Got %s.' %(
                    self.max,
                    self.label,
                    l
                )
            )