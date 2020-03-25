# coding=utf-8
import inspect
from typing import Any, Union

class PyMetamodelParser(object):

    def __init__(self):
        pass

    def parsePyModule(self, module):

        classes=_PyHelper.moduleClasses(module)
        print(('metamodel %s' % module.__name__))
        print('')
        for c in classes:
            self.parsePyClass(c)


    def parsePyClass(self, class_):
        superc=', '.join(
            [c.__name__ for c in _PyHelper.classSuperclasses(class_)])
        print(('    class %s %s' % (
            class_.__name__,
            '' if superc is '' else ' < %s' % superc)))
        props=_PyHelper.classProperties(class_)
        if len(props)>0:
            # print('    attributes')
            for p in props:
                self.parsePyProperty(p)
        ops=_PyHelper.classMethods(class_)
        if len(ops)>0:
            # print('    operations')
            for o in ops:
                self.parsePyMethod(o)
        print('    end')
        print('')

    def parsePyProperty(self, p):
        mi=_PyHelper.classPropertyMetaInfo(p)
        print(('        %s %s : %s' % (mi.kind, mi.name, mi.spec)))

    def parsePyMethod(self, m):
        print(('        operation %s()' % m.__name__))




class _PyHelper(object):

    @classmethod
    def moduleSubModules(cls, module):
        return seconds(inspect.getmembers(
            module,
            inspect.ismodule))

    @classmethod
    def moduleClasses(cls, module):
        classes = seconds(
            inspect.getmembers(module, inspect.isclass))
        if hasattr(module, '__all__'):
            classes = [c for c in classes if c.__name__ in module.__all__]
        # classes = filter(
        #         lambda c: hasattr(c, 'meta'),
        #         classes)
        classes = list(filter(isNotHidden, classes))
        return classes

    @classmethod
    def classSuperclasses(cls, class_):
        return class_.__bases__

    @classmethod
    def classInheritedMembers(cls, class_):
        parents = inspect.getmro(class_)[1:]
        parents_members = []
        for parent in parents:
            members = seconds(inspect.getmembers(parent))
            for m in members:
                if m not in parents_members:
                    parents_members.append(m)
        return list(parents_members)

    @classmethod
    def classDirectMembers(cls, class_):
        inherited = _PyHelper.classInheritedMembers(class_)
        direct = [m
                  for (_, m) in inspect.getmembers(class_)
                  if m not in inherited]
        return direct

    @classmethod
    def classMembers(cls, class_, mode='direct'):
        # type: ('Class', Union['direct','all','inherited']) -> 'Members'
        if mode == 'all':
            return seconds(inspect.getmembers(class_))
        elif mode == 'inherited':
            return _PyHelper.classInheritedMembers(class_)
        elif mode == 'direct':
            return _PyHelper.classDirectMembers(class_)
        else:
            NotImplementedError()

    @classmethod
    def classProperties(cls, class_, mode='direct'):
        properties = [m for m in _PyHelper.classMembers(class_, mode=mode) if isinstance(m, property)]
        properties = [m for m in properties if hasattr(m.fget, 'metainfo')]
        return list(filter(isNotHidden, properties))

    @classmethod
    def classMethods(cls, class_, mode='direct'):
        methods = list(filter(
            inspect.ismethod,
            _PyHelper.classMembers(class_, mode=mode)))
        return list(filter(isNotHidden, methods))

    @classmethod
    def classPropertyMetaInfo(cls, property):
        return property.fget.metainfo




def seconds(l):
    return list([e[1] for e in l])

def nameOf(e):
    # (Any) -> bool
    if hasattr(e, '__name__'):
        return e.__name__
    elif hasattr(e, 'fget'):
        return e.fget.__name__
    else:
        print(('NO NAME FOR ELEMENT %s' % type(e).__name__))
        return '_NO_NAME'
        # raise NotImplementedError()


def isNotHidden(e):
    return not nameOf(e).startswith('_')


    # def isNotHidden(e):
    #     return nameOf(e).startswith('_')p) in inspect.getmembers(c, lambda o: isinstance(o, property)):
    #                 print('    prop ' + str(p.fget.__name__) + '')
    #                 # print('         ',dir(p))
    #             for (nm, m) in inspect.getmembers(c, inspect.ismethod):
    #                 print('    meth ' + str(m.__name__) + '()')