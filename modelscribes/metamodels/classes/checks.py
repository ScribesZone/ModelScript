# coding=utf-8

from modelscribes.megamodels.checks import Checker
from modelscribes.base.issues import (
    Levels
)
from modelscribes.base .symbols import Symbol

from modelscribes.metamodels.classes import (
    EnumerationLiteral
)

class EnumLiteralNomclatureChecker(Checker):

    def __init__(self, level, params=None):
        super(EnumLiteralNomclatureChecker, self).__init__(
            classes=[EnumerationLiteral],
            name='EnumLiteralNomclatureChecker',
            level=level,
            params=params
        )


    def doCheck(self, e):
        #:type ('EnumerationLiteral') -> None
        if not Symbol.is_camlCase(e.name):
            return (
                '"%s" should be in camlCase.' %
                e.name
            )

        else:
            return None

EnumLiteralNomclatureChecker(
    level=Levels.Warning
)

print('ZZ'*100)