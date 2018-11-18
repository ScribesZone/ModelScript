# coding=utf-8
from collections import OrderedDict

from typing import Dict,  List, Optional

__all__=(
    '_MetaCheckerPackageRegistry'
)

class _MetaCheckerPackageRegistry(object):
    """
    Part of the megamodel dealing with metapackages
    """

    _metaCheckerPackageNamed=OrderedDict()

    @classmethod
    def registerMetaCheckerPackage(cls, metaPackage):
        cls._metaCheckerPackageNamed[metaPackage.qname]=metaPackage

    @classmethod
    def metaCheckerPackages(cls):
        return cls._metaCheckerPackageNamed.values()