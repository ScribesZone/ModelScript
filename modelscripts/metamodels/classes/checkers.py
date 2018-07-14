# coding=utf-8

from modelscripts.megamodels.checkers import NamingChecker
from modelscripts.base.issues import (
    Levels
)
from modelscripts.base .symbols import Symbol

from modelscripts.metamodels.classes.classes import (
    Class)
from modelscripts.metamodels.classes.types import EnumerationLiteral


class ClassNomenclatureChecker(NamingChecker):
    def __init__(self, **params):
        super(ClassNomenclatureChecker, self).__init__(
            metaclasses=[Class],
            fun=Symbol.is_CamlCase,
            namingName='CamlCase',
            **params)

ClassNomenclatureChecker(
    level=Levels.Warning
)

class EnumLiteralNomenclatureChecker(NamingChecker):
    def __init__(self, **params):
        super(EnumLiteralNomenclatureChecker, self).__init__(
            metaclasses=[EnumerationLiteral],
            fun=Symbol.is_camlCase,
            namingName='camlCase',
            **params
        )

EnumLiteralNomenclatureChecker(
    level=Levels.Warning
)