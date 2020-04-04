# coding=utf-8
"""Decorators of meta elements.

This way of annotating the implementation of the metamodel is not very
used. It seems that it is competing with the metametamodel package.
To be checked.
"""

import functools

__all__ = (
    'MemberDecorator',
    'MAttribute',
    'MReference',
    'MComposition',
    'MContainer'
)

class MemberDecorator(object):
    def __init__(self, kind, spec):
        self.spec = spec
        self.kind = kind
        self.method = None  # filled when applied
        self.name = None  # filled when applied
        self.p = None

    def __call__(self, method):
        method.metainfo = self

        # @functools.wraps(method)
        # def decorated(*args, **kwargs):
        #     print "before call, %s" % self.arg
        #     method(*args, **kwargs)
        #     print "after call, %s" % self.arg
        self.method = method
        self.name = self.method.__name__
        self.p = property(method)
        return self.p


class MAttribute(MemberDecorator):
    def __init__(self, spec):
        super(MAttribute, self).__init__(
            kind='attribute',
            spec=spec
        )


class MReference(MemberDecorator):
    def __init__(self, spec):
        super(MReference, self).__init__(
            kind='reference',
            spec=spec
        )


class MComposition(MemberDecorator):
    def __init__(self, spec):
        super(MComposition, self).__init__(
            kind='composition',
            spec=spec
        )

class MContainer(MemberDecorator):
    def __init__(self, spec):
        super(MContainer, self).__init__(
            kind='composition',
            spec=spec
        )

