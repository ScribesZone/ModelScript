# coding=utf-8
"""Demo metamodel.

The composition view is the backbone of the class model.
It shows containment relationships ::

    DemoModel
        <>--* Class
            <>--* Reference

"""

import collections
from typing import Union, List, Optional

from modelscript.base.grammars import TextXNode
from modelscript.megamodels.elements import SourceModelElement
from modelscript.base.metrics import Metrics
from modelscript.megamodels.metamodels import Metamodel
from modelscript.megamodels.dependencies.metamodels import (
    MetamodelDependency)
from modelscript.megamodels.models import Model
from modelscript.megamodels.models import Placeholder

__all__ = (
    'DemoModel',
    'Class',
    'Reference',
    'METAMODEL',
    'MetamodelDependency'
)



ISSUES = {
    'SUPER_CYCLES_MSG': 'cl.fin.Cycle.One',
}


def icode(ilabel):
    return ISSUES[ilabel]


class DemoModel(Model):
    """Demo model.
    """

    META_COMPOSITIONS = [
        'classes',
    ]

    def __init__(self) -> None:
        super(DemoModel, self).__init__()

        self._classNamed = collections.OrderedDict()

    @property
    def metamodel(self):
        return METAMODEL

    # --------------------------------------------------------------
    #   Classes
    # --------------------------------------------------------------

    @property
    def classes(self) -> List['Class']:
        return list(self._classNamed.values())

    @property
    def classNames(self) -> List[str]:
        return list(self._classNamed.keys())

    def class_(self, name: str) -> Optional['Class']:
        if name in self._classNamed:
            return self._classNamed[name]
        else:
            return None

    # --------------------------------------------------------------
    #   Metrics
    # --------------------------------------------------------------

    @property
    def metrics(self) -> Metrics:
        ms = super(DemoModel, self).metrics
        ms.addList([
            ('class', len(self.classes)),
            ('references', len(
                [r
                 for c in self.classes
                 for r in c.references]
            ))
        ])
        return ms

    def finalize(self):
        super(DemoModel, self).finalize()
        pass  # demo: TODO


class Class(SourceModelElement):
    """Classes.
    """

    isAbstract: bool
    references: List['Reference']

    META_COMPOSITIONS = [
        'references'
    ]

    def __init__(self,
                 name: str,
                 model: DemoModel,
                 isAbstract: bool = False,
                 astNode: 'TextXNode' = None,
                 lineNo=None,
                 description=None):
        super(Class, self).__init__(
            model=model,
            name=name,
            astNode=astNode,
            lineNo=lineNo, description=description)

        self.isAbstract = isAbstract
        self._referenceNamed = collections.OrderedDict()

        self.model._classNamed[name] = self

    # -----------------------------------------------------------------
    #   references
    # -----------------------------------------------------------------

    @property
    def references(self):
        return list(self._referenceNamed.values())

    def reference(self, name):
        if name in self._referenceNamed:
            return self._referenceNamed[name]
        else:
            return None

    @property
    def referenceNames(self):
        return list(self._referenceNamed.keys())


class Reference(SourceModelElement):
    """References.
    """

    isMultiple: bool
    target: Union[str, Class]

    def __init__(self,
                 name: str,
                 class_: Class,
                 isMultiple: bool,
                 target: Union[Placeholder, Class],
                 astNode: 'TextXNode' = None,
                 lineNo=None,
                 description=None):
        super(Reference, self).__init__(
            model=class_.model,
            name=name,
            astNode=astNode,
            lineNo=lineNo, description=description)

        self.isMultiple = isMultiple

        # The target can be just a name that will be resolved later.
        self.target = target

        # register the reference into the class
        class_._referenceNamed[name] = self


METAMODEL = Metamodel(
    id='de',
    label='demo',
    extension='.des',
    modelClass=DemoModel,
    uniqueness=True
)

# MetamodelDependency(
#     sourceId='cl',
#     targetId='gl',
#     optional=True,
#     multiple=True,
# )

