# coding=utf-8
"""Exceptions
"""

__all__=(
    'NotFound',
    'InternalError',
    'UnexpectedCase',
    'UnexpectedState',
    'UnexpectedValue',
    'NoSuchFeature',
    'MethodToBeDefined',
    'FileSystemError',
    'TODO'
)

class NotFound(Exception):
    pass


class InternalError(Exception):
    pass


class UnexpectedCase(InternalError):
    pass


class UnexpectedState(InternalError):
    pass


class UnexpectedValue(InternalError):
    pass


class NoSuchFeature(InternalError):
    pass


class MethodToBeDefined(InternalError):
    pass


class FileSystemError(InternalError):
    pass


class TODO(InternalError):
    pass

