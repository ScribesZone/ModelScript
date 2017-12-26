# coding=utf-8
from typing import Text, Dict, List, Any
import collections
from abc import ABCMeta


from modelscripts.base.issues import (
    Level
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
            print('ckk: register %s' %
                  checker.name)
        for c in checker.classes:
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
                        model=element.model,
                        modelElement=element,
                        level=checker.level,
                        message=msg
                    )
        else:
            if DEBUG>=3:
                print('ckk:     no checker found.')


class Checker(object):
    __metaclass__ = ABCMeta

    def __init__(self, classes, name, level, params=None):
        #type: (List['MetaClass'], Text, Level, Dict[Text, Any]) -> None
        self.classes=classes
        self.name=name
        self.level=level
        if params is None:
            params=dict()
        self.parameters=params
        CheckList.registerChecker(self)


    def doCheck(self, e):
        raise NotImplementedError(
            'Checker %s on %s is not implemented ' % (
                self.name,
                type(e).__name__
            ))



