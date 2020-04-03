# coding=utf-8
"""Python helpers"""

__all__ = (
    'getObjectValues'
)


def getObjectValues(obj, name, asList=True):
    if not hasattr(obj, name):
        raise ValueError('Class %s has not attribute %s' % (  # raise:TODO:4
            obj.__class__.__name__,
            name))
    x = getattr(obj, name)
    if callable(x):
        x = x()
    if asList and not isinstance(x, (tuple, list)):
        x = [] if x is None else [x]
    return x
