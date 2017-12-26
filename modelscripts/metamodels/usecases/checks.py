# coding=utf-8

from modelscripts.megamodels.checkers import (
    Checker,
    NamingChecker,
    LimitsChecker
)
from modelscripts.base.symbols import Symbol
from modelscripts.base.issues import (
    Levels
)

from modelscripts.metamodels.usecases import (
    UsecaseModel
)


class SystemDefinedChecker(Checker):

    def __init__(self, **params):
        super(SystemDefinedChecker, self).__init__(
            metaclasses=[UsecaseModel],
            **params
        )

    def doCheck(self, ucm):
        if not ucm.isSystemDefined:
            return (
                'No system defined'
            )

SystemDefinedChecker(
    level=Levels.Error
)

class ActorLimitsChecker(LimitsChecker):
    def __init__(self, **params):
        LimitsChecker.__init__(self,
            metaclasses=[UsecaseModel],
            label='actor',
            **params)

    def size(self, e):
        return len(e.actors)


ActorLimitsChecker(
    level=Levels.Warning,
    min=1,
    max=10
)

#-------------------------------------------------------------

from modelscripts.metamodels.usecases import (
    System
)


class SystemNamingChecker(NamingChecker):
    def __init__(self, **params):
        NamingChecker.__init__(
            self,
            metaclasses=[System],
            fun=Symbol.is_CamlCase,
            namingName='CamlCase',
            **params
        )

SystemNamingChecker(
    level=Levels.Warning,
)


class UsecaseLimitsChecker(LimitsChecker):
    def __init__(self, **params):
        LimitsChecker.__init__(self,
            metaclasses=[System],
            label='usecase',
            **params)

    def size(self, e):
        return len(e.usecases)


UsecaseLimitsChecker(
    level=Levels.Warning,
    min=3,
    max=15
)
#-------------------------------------------------------------

from modelscripts.metamodels.usecases import (
    Actor
)

class ActorNamingChecker(NamingChecker):
    def __init__(self, **params):
        NamingChecker.__init__(
            self,
            metaclasses=[Actor],
            fun=Symbol.is_CamlCase,
            namingName='CamlCase',
            **params
        )

ActorNamingChecker(
    level=Levels.Warning,
)


class LazyActorChecker(Checker):
    def __init__(self, **params):
        Checker.__init__(
            self,
            metaclasses=[Actor],
            **params)

    def doCheck(self, e):
        if len(e.usecases)==0:
            return (
                'Actor "%s" does not perform any usecase' %
                e.name)

LazyActorChecker(
    level=Levels.Warning,
)

#-------------------------------------------------------------

from modelscripts.metamodels.usecases import (
    Usecase
)

class UsecaseNamingChecker(NamingChecker):
    def __init__(self, **params):
        NamingChecker.__init__(
            self,
            metaclasses=[Usecase],
            fun=Symbol.is_CamlCase,
            namingName='CamlCase',
            **params
        )

UsecaseNamingChecker(
    level=Levels.Warning,
)


class UnusedUsecaseChecker(Checker):
    def __init__(self, **params):
        Checker.__init__(self,
                         metaclasses=[Usecase],
                         **params)

    def doCheck(self, e):
        if len(e.actors)==0:
            return (
                'No actor performs "%s"' %
                e.name)

UnusedUsecaseChecker(
    level=Levels.Warning,
)