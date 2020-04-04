# coding=utf-8
"""Element of source or models"""

from abc import ABCMeta
from collections import OrderedDict
from typing import Optional, Any, Dict, Text

__all__=(
    'SourceElement',
    'Descriptor',
    'ModelElement',
    'SourceModelElement'
)

from modelscript.base import py
from modelscript.megamodels.checkers import (
    CheckList
)
from modelscript.base.grammars import (
    TextXNode
)


class SourceElement(object, metaclass=ABCMeta):
    """ Element of a source file.
    """
    def __init__(self,
                 name: Optional[str] = None,
                 astNode: TextXNode = None,
                 lineNo: Optional[int] = None,
                 code: Optional[str] = None,
                 description: Optional[str] = None,
                 eolComment: Optional[str] = None):
        self.name = name
        self.astNode = astNode
        self.lineNo = lineNo
        self.code = code
        self.description = description
        self.eolComment = eolComment


class Descriptor(object):

    def __init__(self, name: str, value: Any = None) -> None:
        self.name: str = name
        self.value: Any = value

    def __repr__(self):
        return '<descriptor:%s:%s>' % (
            self.name,
            self.value
        )


class ModelElement(object, metaclass=ABCMeta):
    def __init__(self, model):
        assert model is not None
        self._model = model
        self.stereotypes = []
        self.tags = []
        from modelscript.metamodels.textblocks import (
            TextBlock
        )
        self.description: Optional[TextBlock] = None
        self.descriptorNamed: Dict[Text, Descriptor] = OrderedDict()

    @property
    def model(self) -> 'Model':
        return self._model

    @property
    def descriptors(self):
        #TODO:4 2to3 was return self.descriptorNamed.values()
        return list(self.descriptorNamed.values())

    @model.setter
    def model(self, model):
        self._model = model

    @property
    def children(self):
        r = []
        if hasattr(self, 'META_COMPOSITIONS'):
            for child_name in getattr(self, 'META_COMPOSITIONS'):
                l = py.getObjectValues(
                    self, child_name, asList=True)
                for e in l:
                    if e not in r:
                        r.append(e)
        return r

    def check(self):
        CheckList.check(self)
        for child in self.children:
            child.check()


class SourceModelElement(ModelElement, SourceElement, metaclass=ABCMeta):
    def __init__(self,
                 model,
                 name=None,
                 astNode=None,
                 code=None,
                 lineNo=None,
                 description=None,
                 eolComment=None):
        from modelscript.megamodels.models import Model
        SourceElement.__init__(self,
                               name = name,
                               astNode=astNode,
                               code = code,
                               lineNo = lineNo,
                               description = description,
                               eolComment = eolComment)
        if model is not None:
            assert isinstance(model, Model)
            ModelElement.__init__(self, model)
        if self.source is not None:
            self.source._addSourceModelElement(self)

    @property
    def source(self):
        return self.model.source


