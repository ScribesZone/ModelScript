# coding=utf-8

def getObjectValues(object, name, asList=True):
    if not hasattr(object, name):
        raise ValueError('Class %s has not attribute %s' % (
            object.__class__.__name__,
            name))
    x = getattr(object, name)
    if callable(x):
        x=x()
    if asList and not isinstance(x, (tuple, list)):
        x= [] if x is None else [x]
    return x
