# coding=utf-8

"""
Condition, Invariants, Precondition and Postcondition.

The structure of this package is the following::

    Condition
    <--  OperationCondition
         <--  PreCondition
         <--  PostCondition
    <--  Invariant
"""

from __future__ import print_function
from typing import Text, Optional, Union, List, Dict
import collections
import abc
import logging

# logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('test.' + __name__)

from modelscripts.metamodels.classes import (
    ClassTopLevelElement
)
from modelscripts.base.sources import SourceElement
from modelscripts.metamodels.classes import (
    ClassModel,
    Class,
    Operation
)

class Condition(ClassTopLevelElement):
    """
    Invariant, precondition or postcondition
    """
    __metaclass__ = abc.ABCMeta
    def __init__(
            self, name, model, class_, expression, code=None,
            lineNo=None, docComment=None, eolComment=None):
        #type: (Optional[Text], ClassModel, Class, Text, Optional[Text], Optional[int], Optional[Text], Optional[Text]) -> None
        super(Condition, self).__init__(
            name, model, code=code,
            lineNo=lineNo, docComment=docComment, eolComment=eolComment)
        self.class_ = class_  # Text resolved in Class  # could be null as some invariants are toplevel
        self.expression = expression
        # add it so that it can be resolved later
        self.model._conditions.append(self)


class OperationCondition(Condition):
    """
    Operation conditions (precondition or postcondition).
    """
    __metaclass__ = abc.ABCMeta
    def __init__(
            self, name, model, class_, operation, expression,
            code=None,   # FIXME: operation could be unknowed
            lineNo=None, docComment=None, eolComment=None ):
        #type: (Optional[Text], ClassModel, Class,  Operation, Text, Optional[Text], Optional[int], Optional[Text], Optional[Text]) -> None
        super(OperationCondition, self).__init__(
            name, model, class_=class_, expression=expression, code=code,
            lineNo=lineNo, docComment=docComment, eolComment=eolComment)
        self.operation=operation # the signature of the operation, then resolved as Operation
        # # store the condition in the operation
        # operation.conditionNamed[name] = self



class PreCondition(OperationCondition):
    """
    Preconditions.
    """
    def __init__(self,
                 name, model, class_, operation, expression, code=None,
                 lineNo=None, docComment=None, eolComment=None):
        super(PreCondition, self).__init__(
            name, model, class_=class_, operation=operation, expression=expression,
            code=code,
            lineNo=lineNo, docComment=docComment, eolComment=eolComment
        )



class PostCondition(OperationCondition):
    """
    Postconditions.
    """
    def __init__(self,
                 name, model, class_, operation, expression, code=None,
                 lineNo=None, docComment=None, eolComment=None):
        super(PostCondition, self).__init__(
            name, model, class_=class_, operation=operation, expression=expression,
            code=code,
            lineNo=lineNo, docComment=docComment, eolComment=eolComment)


class Invariant(Condition):
    """
    Invariants.
    """
    def __init__(self, name, model, expression, class_=None, code=None,
                 variable='self',
                 additionalVariables = (),
                 toplevelDefined=True,
                 isExistential=False,
                 lineNo=None, docComment=None, eolComment=None):
        super(Invariant, self).__init__(
            name, model, class_=class_, expression=expression, code=code,
            lineNo=lineNo, docComment=docComment, eolComment=eolComment)
        self.variable = variable
        self.additionalVariables = additionalVariables
        self.toplevelDefined=toplevelDefined,
        self.isExistential = isExistential

    @property
    def isModelInvariant(self):
        """
        Is the invariant defined on model, that is without any context
        """
        return self.class_ is None

    @property
    def invariantLabel(self):
        return '%s::%s' % (self.class_.name, self.name)

    def __str__(self):
        return self.invariantLabel

    def __repr__(self):
        return 'INV(%s::%s)' % (self.class_.name, self.name)
