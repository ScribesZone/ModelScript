# coding=utf-8

from modelscript.megamodels.checkers import NamingChecker
from modelscript.base.issues import (
    Levels
)
from modelscript.base .symbols import Symbol

from modelscript.metamodels.classes.classes import (
    Class)
from modelscript.metamodels.classes.types import EnumerationLiteral


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