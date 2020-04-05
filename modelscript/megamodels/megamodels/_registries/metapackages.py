# coding=utf-8
"""issue box registry.
This module provides a unique mixin _MetaPackageRegistry to be
included in the Megamodel class.
"""

from collections import OrderedDict

__all__ = (
    '_MetaPackageRegistry'
)


class _MetaPackageRegistry(object):
    """Part of the megamodel dealing with metapackages
    """

    _metaPackageNamed = OrderedDict()

    @classmethod
    def registerMetaPackage(cls, metaPackage):
        cls._metaPackageNamed[metaPackage.qname] = metaPackage

    @classmethod
    def metaPackages(cls):
        return list(cls._metaPackageNamed.values())
