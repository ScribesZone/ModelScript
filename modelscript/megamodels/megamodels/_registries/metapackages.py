# coding=utf-8
from collections import OrderedDict

from typing import Dict,  List, Optional

__all__=(
    '_MetaPackageRegistry'
)

class _MetaPackageRegistry(object):
    """
    Part of the megamodel dealing with metapackages
    """

    _metaPackageNamed=OrderedDict()

    @classmethod
    def registerMetaPackage(cls, metaPackage):
        cls._metaPackageNamed[metaPackage.qname]=metaPackage

    @classmethod
    def metaPackages(cls):
        return cls._metaPackageNamed.values()