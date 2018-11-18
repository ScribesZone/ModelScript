# coding=utf-8

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

