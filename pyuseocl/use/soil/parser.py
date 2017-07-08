# coding=utf-8

"""
Parser of os subset of the soil language.


SOIL Syntax
http://useocl.sourceforge.net/wiki/index.php/SOIL

            s ::=                                     (statement)
(P)            v := new c [(nameExpr)] |              (object creation)
(I)            create v : c
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
from __future__ import unicode_literals, print_function, absolute_import, division

import os
import re

DEBUG=3

from pyuseocl.metamodel.scenarios import (
    Scenario,
    ObjectCreation,
    ObjectDestruction,
    LinkCreation,
    LinkDestruction,
    LinkObjectCreation,
    AttributeAssignment,
)



def isEmptySoilFile(file):
    with open(file) as f:
        content = f.read()
    match = re.search(r'(^ *!)|(^ *open)', content, re.MULTILINE)
    return match is None




class SoilSource(object):
    def __init__(self, classModel, soilFileName):
        if not os.path.isfile(soilFileName):
            raise Exception('File "%s" not found' % soilFileName)
        self.fileName = soilFileName
        self.sourceLines = (
            line.rstrip()
            for line in open(self.fileName, 'rU'))
        self.directory = os.path.dirname(soilFileName)
        self.isValid = None
        self.errors = []
        self.lines = None
        self.ignoredLines = []
        self.classModel = classModel
        self.scenario = Scenario(
            classModel=classModel,
            name=None,
            system=None,
            file=soilFileName)
        self._parse()
        self.isValid=True # Todo, check errors, etc.

    def _parse(self, prefix=r'^'):
        begin = prefix + r' *! *'
        end = ' *$'

        if DEBUG>=1:
            print('\nParsing %s\n' % self.fileName)

        for (line_index, line) in enumerate(self.sourceLines):
            original_line = line
            # replace tabs by spaces
            line = line.replace('\t',' ')
            line_no = line_index+1

            if DEBUG>=2:
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

            #--- object creation (create x : C) ---------------------
            r = begin+r'create +(?P<name>\w+) *: *(?P<className>\w+)'+end
            m = re.match(r, line)
            if m:
                variable=m.group('name')
                classname=m.group('className')
                id=None
                if DEBUG:
                    print('%s := new %s' % (variable,classname))

                ObjectCreation(
                    scenario=self.scenario,
                    variableName=variable,
                    class_=self.classModel.classNamed[classname],
                    id=id,
                    lineNo=line_no
                )
                continue

            #--- object creation(x := new C('lila') --------------------
            r = (begin
                 + r'(?P<name>\w+) *:= *new +(?P<className>\w+)'
                 + ' *( *\( *(\'(?P<id>\w+)\')? *\))?'
                 + end)
            m = re.match(r, line)
            if m:
                variable=m.group('name')
                classname=m.group('className')
                id=m.group('id')
                if DEBUG:
                    print('%s := new %s : %s' % (variable,id,classname))

                ObjectCreation(
                    scenario=self.scenario,
                    variableName=variable,
                    class_=self.classModel.classNamed[classname],
                    id=id,
                    lineNo=line_no
                )
                continue

            #--- attribute assignement ----------------------------------------
            r = (begin
                    + r'(set )? *(?P<name>\w+) *'
                    + r'\. *(?P<attribute>\w+) *'
                    + r':= *(?P<expr>.*) *'
                    + end )
            # r2 = (begin
            #         + r'create +(?P<name>\w+) *'
            #         + r'\. *(?P<attribute>\w+) *'
            #         + r':= *(?P<value>.*)'
            #         + end )
            m = re.match(r, line)
            if m:
                variable=m.group('name')
                attribute=m.group('attribute')
                expression=m.group('expr')
                if DEBUG:
                    print ('%s.%s := %s' % (
                        variable, attribute, expression))
                AttributeAssignment(
                    scenario=self.scenario,
                    variableName=variable,
                    attributeName=attribute,
                    expression=expression,
                    lineNo=line_no,
                )
                continue

            #--- link creation-------------------------------------------------
            r = (begin
                 + r'insert *\((?P<names>[\w, ]+)\) *'
                 + r'into +'
                 + r'(?P<associationName>\w+)'
                 + end )
            m = re.match(r, line)
            if m:
                names = [
                    n.strip()
                    for n in m.group('names').split(',')]
                assoc=self.classModel.associationNamed[m.group('associationName')]
                if DEBUG:
                    print('new (%s) : %s' % (
                        ','.join('names'),
                        assoc.name ))
                LinkCreation(
                    scenario=self.scenario,
                    names=names,
                    association=assoc,
                    id=None,
                    lineNo=None
                )
                continue

            #--- link object creation (form1 ) --------------------------------
            # ex: create r1 : Rent between (a1,b2)
            r = (begin
                 + r'create +(?P<name>\w+) *: *(?P<assocClassName>\w+) +'
                 + r'between +\((?P<names>[\w, ]+)\) *'
                 + end )
            m = re.match(r, line)
            if m:
                assoc_class_name = m.group('assocClassName')
                name = m.group('name')
                names = m.group('objectList').replace(' ','').split(',')
                ac = self.classModel.associationClassNamed[assoc_class_name]
                if DEBUG:
                    print(('new %s between (%s)' % (
                        assoc_class_name,
                        ','.join(names))
                    ))
                LinkObjectCreation(
                    scenario=self.scenario,
                    variableName=name,
                    names=names,
                    id=None,
                    associationClass=ac,
                    lineNo=None
                )
                continue

            #--- link object creation (form1 ) --------------------------------
            # v1 := new Rent('lila') between (r1,a2,v3)
            r = (begin
                 + r'(?P<name>\w+) *:='
                 + r' *new +(?P<assocClassName>\w+)'
                 + r' *( *\( *(\'(?P<id>\w+)\')? *\))?'
                 + r' *between +\((?P<objectList>[\w, ]+)\) *'
                 + end )
            m = re.match(r, line)
            if m:
                assoc_class_name = m.group('assocClassName')
                name = m.group('name')
                id = m.group('id')
                names = m.group('objectList').replace(' ','').split(',')
                ac = self.classModel.associationClassNamed[assoc_class_name]
                if DEBUG:
                    print(('new %s between (%s)' % (
                        assoc_class_name,
                        ','.join(names)
                    )))
                LinkObjectCreation(
                    scenario=self.scenario,
                    variableName=name,
                    names=names,
                    id=id,
                    associationClass=ac,
                    lineNo=None
                )
                continue




            #--- object (or link object) destruction --------------------------
            r = (begin+ r'destroy +(?P<name>\w+)'+ end )
            m = re.match(r, line)
            if m:
                name = m.group('name')
                if DEBUG:
                    print( 'delete object %s' % name )
                ObjectDestruction(
                    scenario=self.scenario,
                    variableName=name,
                )
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
                print( 'delete link from %s between %s' % (
                    association_name,
                    object_names
                ))




            #---- unknown or unimplemented commands ---------------------------
            print( 'Error: pyuseocl cannot parse line #%s: %s' %(
                line_no,
                original_line
            ))

            raise NotImplementedError(line)
