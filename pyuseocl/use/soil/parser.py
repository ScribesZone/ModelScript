# coding=utf-8

"""
Interpreter of soil specifications. Not fully implemented.


SOIL Syntax
http://useocl.sourceforge.net/wiki/index.php/SOIL

            s ::=                                     (statement)
                v := new c [(nameExpr)] |              (object creation)
                create v : c
               v := new c [(nameExpr)] between (participant1,participant2,...) |
                                                      (link object creation)
(I)            destroy e  |                           (object destruction)
(I)            insert (e1; ... ; en) into a j |       (link insertion)
(I)            delete (e1; ... ; en) from a j |       (link deletion)
(I)            e1.a := e2 |                           (attribute assignment)
               v := e |                               (variable assignment)
               e1.op(e2; ... ; en) |                  (operation call)
               v := e1.op(e2; ... ; en) |             (operation call with result)
               [begin] s1; ... ; sn [end] [declare v1 : t1; ... ; vn : tn] |
                                                      (block of statements)
               if e then s1 [else s2] end |           (conditional execution)
               for v in e do s end                    (iteration)

"""

import os
import re


from pyuseocl.metamodel.scenarios import (
    Scenario,
    ObjectCreation,
    ObjectDestruction,
    LinkCreation,
    LinkDestruction,
    AttributeAssignement,
)



def isEmptySoilFile(file):
    with open(file) as f:
        content = f.read()
    match = re.search(r'(^ *!)|(^ *open)', content, re.MULTILINE)
    return match is None


class SoilSpecificationFile(object):
    def __init__(self, useSoilFile):
        if not os.path.isfile(useSoilFile):
            raise Exception('File "%s" not found' % useSoilFile)
        self.fileName = useSoilFile
        self.sourceLines = tuple(
            open(useSoilFile, 'r').read().splitlines())
        self.directory = os.path.dirname(useSoilFile)
        self.isValid = None
        self.errors = []
        self.lines = None
        self.ignoredLines = []
        self.state = None # filled by _parse pyuseocl.metamodel.state.State
        self._parse()


    def _parse(self, prefix=r'^'):
        begin = prefix + r' *! *'
        end = ' *$'
        scenario=pyuseocl.metamodel.state.State()
        print '\nParsing %s\n' % self.fileName

        for (line_index, line) in enumerate(self.sourceLines):
            original_line = line
            # replace tabs by spaces
            line = line.replace('\t',' ')
            line_no = line_index+1

            print ('#%i : %s' % (line_no, original_line))

            #---- blank lines ---------------------------------------------
            r = prefix+' *'+end
            m = re.match(r, line)
            if m:
                continue

            #---- comments -------------------------------------------------
            r = prefix+' *--.*'+end
            m = re.match(r, line)
            if m:
                continue

            #--- object creation ----------------------------------------------
            r = begin+r'create +(?P<name>\w+) *: *(?P<className>\w+)'+end
            m = re.match(r, line)
            if m:
                print 'object %s : %s' % (m.group('name'),m.group('className'))

                # pyuseocl.metamodel.state.Object(
                #     self.state, m.group('className'), m.group('name'))
                continue

            #--- attribute assignement ----------------------------------------
            r = (begin
                    + r'(set )? *(?P<name>\w+) *'
                    + r'\. *(?P<attribute>\w+) *'
                    + r':= *(?P<value>.*)'
                    + end )
            # r2 = (begin
            #         + r'create +(?P<name>\w+) *'
            #         + r'\. *(?P<attribute>\w+) *'
            #         + r':= *(?P<value>.*)'
            #         + end )
            m = re.match(r, line)
            if m:
                print 'attribute %s.%s = %s' % (
                   m.group('name'), m.group('attribute'), m.group('value'))
                # object = self.state.objects[m.group('name')]
                # object.set(m.group('attribute'),m.group('value'))
                continue

            #--- link creation-------------------------------------------------
            r = (begin
                 + r'insert *\((?P<objectList>[\w, ]+)\) *'
                 + r'into +'
                 + r'(?P<associationName>\w+)'
                 + end )
            m = re.match(r, line)
            if m:
                print 'link %s : %s' % (
                    m.group('objectList'),
                    m.group('associationName'), )
                # object_names = m.group('objectList').replace(' ','').split(',')
                # objects = [ self.state.objects[object_name]
                #             for object_name in object_names ]
                # pyuseocl.metamodel.state.Link(
                #     self.state, m.group('associationName'), objects)
                continue

            #--- link object creation -----------------------------------------
            r = (begin
                 + r'create +(?P<name>\w+) *: *(?P<className>\w+) +'
                 + r'between +\((?P<objectList>[\w, ]+)\) *'
                 + end )
            m = re.match(r, line)
            if m:
                class_name = m.group('className')
                name = m.group('name')
                object_names = m.group('objectList').replace(' ','').split(',')
                print 'linkobject %s : %s between ' % (
                    name,
                    class_name,
                    object_names
                )
                # objects = [self.state.objects[object_name]
                #            for object_name in object_names]
                # pyuseocl.metamodel.state.LinkObject(
                #     self.state, class_name, name, objects)
                continue

            #--- object (or link object) destruction --------------------------
            r = (begin+ r'destroy +(?P<name>\w+)'+ end )
            m = re.match(r, line)
            if m:
                name = m.group('name')
                print 'delete object %s' % name
                # check if this is an regular object or a link object
                # if name in self.state.objects:
                #     del self.state.objects[name]
                # else:
                #     del self.state.linkObject[name]
                # continue

            #--- link destruction ---------------------------------------------
            r = (begin
                 + r'delete *\((?P<objectList>[\w, ]+)\)'
                 + r' +from +(?P<associationName>\w+)'
                 + end )
            m = re.match(r, line)
            if m:
                object_names = \
                    m.group('objectList').replace(' ', '').split(',')
                association_name = m.group('associationName')
                # link_name = '_'.join(object_names)
                # del self.state.links[link_name]
                print 'delete link from %s between %s' % (
                    association_name,
                    object_names
                )




            #---- unknown or unimplemented commands ---------------------------
            print 'Error: pyuseocl cannot parse line #%s: %s' %(
                line_no,
                original_line
            )

            raise NotImplementedError(line)
