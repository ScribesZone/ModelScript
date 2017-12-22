# coding=utf-8
from typing import Text, Dict, List, Any
import collections
from abc import ABCMeta


from modelscribes.base.issues import (
    Level
)
from modelscribes.megamodels.issues import (
    ModelElementIssue
)

DEBUG=1

class CheckList(object):

    checkersForClass=collections.OrderedDict()
    #type: Dict['MetaClass', List[Checker]]

    @classmethod
    def registerChecker(cls, checker):

        for c in checker.classes:
            cbc=CheckList.checkersForClass
            if c not in cbc:
                cbc[c]=[]
            if DEBUG >= 1:
                print('ckk: register %s' %
                      checker.name)
            cbc[c].append(checker)

    @classmethod
    def check(cls, element):
        c=type(element)
        print('CC'*10+str(type(c)))
        print(element)
        if c in CheckList.checkersForClass:
            for checker in CheckList.checkersForClass[c]:
                msg=checker.doCheck(element)
                if msg is not None:
                    ModelElementIssue(
                        model=element.model,
                        modelElement=element,
                        level=checker.level,
                        message=msg
                    )


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
        print('QQ'*10+self.name)


    def doCheck(self, e):
        raise NotImplementedError(
            'Checker %s on %s is not implemented ' % (
                self.name,
                type(e).__name__
            ))



