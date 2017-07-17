# coding=utf-8

"""
Parser of subset of the soil language and of the sex format.
The same parser can parse both:
* .soil files, that is USE OCL soil files
* .sex files, that are an internal format merging .soil files with trace results
See the 'merge' module for more information.


SOIL Syntax
http://useocl.sourceforge.net/wiki/index.php/SOIL

            s ::=                                     (statement)
(P)            v := new c [(nameExpr)] |              (object creation)
(I)            create v : c
(I)            v := new c [(nameExpr)] between (participant1,participant2,...) |
                                                      (link object creation)
(I)            destroy e  |                           (object destruction)
(I)            insert (e1; ... ; en) into a j |       (link insertion)
(I)            delete (e1; ... ; en) from a j |       (link deletion)
(I)            e1.a := e2 |                           (attribute assignment)
(I)            v := e |                               (variable assignment)
               e1.op(e2; ... ; en) |                  (operation call)
               v := e1.op(e2; ... ; en) |             (operation call with result)
               [begin] s1; ... ; sn [end] [declare v1 : t1; ... ; vn : tn] |
                                                      (block of statements)
               if e then s1 [else s2] end |           (conditional execution)
               for v in e do s end                    (iteration)

"""
# TODO: add directive to this list
# TODO: add proper mamangement for Warning and Errors
# TODO: check if a first USE OCL use run would be better

from __future__ import unicode_literals, print_function, absolute_import, division
from typing import Text, Optional, Union, List, Dict
import os
import re

DEBUG=3

from pyuseocl.metamodel.classes import (
    ClassModel
)
from pyuseocl.metamodel.usecases import (
    System,
    Actor,
    Usecase,
)
from pyuseocl.metamodel.scenarios import (
    Scenario,
    ActorInstance,
    ContextBlock,
)
from pyuseocl.metamodel.scenarios.blocks import (
    UsecaseInstanceBlock,
    TopLevelBlock,
)
from pyuseocl.metamodel.scenarios.operations import (
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
    def __init__(self, classModel, soilFileName, system=None):
        """
        Create a soil source and parse it as a scenario.
        In order to do this a class model is necessary to resolve
        class names and operation names in operation.
        A use case model (system) is also necessary, but only there are
        directives for actor instance and usecase instance.
        """
        #type: (ClassModel,Text,Optional[System]) -> None
        if not os.path.isfile(soilFileName):
            raise Exception('File "%s" not found' % soilFileName)
        self.fileName = soilFileName  #type: Text
        self.sourceLines = (
            line.rstrip()
            for line in open(self.fileName, 'rU'))
        self.directory = os.path.dirname(soilFileName) #type:Text
        self.isValid = None #type:Optional[bool]
        self.errors = []
        self.lines = None #type:List[Text]
        self.ignoredLines = []
        self.classModel = classModel #type:ClassModel
        self.system = system #type:Optional[System]
        self.scenario = Scenario(    #type:Scenario
            classModel=classModel,
            name=None,
            system=system,
            file=soilFileName)
        self._parse()
        self.isValid=True # Todo, check errors, etc.

    def _parse(self, prefix=r'^'):

        class _S(object):
            """
            Current state of the parser.
            Required for _getBlock
            """
            original_line=""
            line_no=0

            main_block = None
            # type: Optional[Union[UsecaseInstanceBlock, TopLevelBlock]]
            # current main block
            # null if no toplevel block have been created yet

            context_block = None
            # type: Optional[ContextBlock]
            #: can be nested in other blocks

        def _getBlock():
            """
            Create a toplevel block if necessary (None)
            otherwise reuse the existing one.
            """
            if _S.context_block is not None:
                # inside a context block
                return _S.context_block
            else:
                if _S.main_block is None:
                    # no block, create one
                    _S.main_block = TopLevelBlock(
                        scenario=self.scenario,
                        lineNo=_S.line_no
                    )
                return _S.main_block


        begin = prefix + r'^ *'
        end = ' *$'



        if DEBUG>=1:
            print('\nParsing %s with %s usecases\n' % (
                self.fileName,
                'no' if self.system is None else ''
            ))

        for (line_index, line) in enumerate(self.sourceLines):

            _S.original_line = line
            _S.line_no = line_index+1
            # replace tabs by spaces
            line = line.replace('\t',' ')

            if DEBUG>=2:
                print ('#%i : %s' % (_S.line_no, _S.original_line))


            #---- check
            r = prefix+'check *.*'+end
            m = re.match(r, line)
            if m:
                print('Warning at line %i: "check" is not implemented yet. Ignored.' % (
                    _S.line_no,
                ))
                continue

            #---- check
            r = prefix+'\?\??.*'+end
            m = re.match(r, line)
            if m:
                print('Warning at line %i: Queries (?) are not implemented yet. Ignored.' % (
                    _S.line_no,
                ))
                continue

            #-------------------------------------------------
            # directives
            #-------------------------------------------------

            #---- -- @scenario XXX
            r = prefix+'-- *@scenario +(?P<name>\w+)'+end
            m = re.match(r, line)
            if m:
                self.scenario.name=m.group('name')
                # TODO: raise an error if the name is already defined
                # TODO: raise an effor if some block has already there
                continue

            #---- -- @actorinstance XXX : YYY
            r = prefix+'-- *@actori +(?P<name>\w+) *: *(?P<actor>\w+)'+end
            m = re.match(r, line)
            if m:
                if self.system is None:
                    print('Warning at line %i: no use case model provided. Directive ignored' % (
                        _S.line_no,
                    ) )
                    continue
                #--- instance
                iname=m.group('name')
                if iname in self.scenario.actorInstanceNamed:
                    raise ValueError(
                        'Error at line %i: actor instance "%s" already exist' % (
                        _S.line_no,
                        iname,
                    ))
                #--- actor
                aname=m.group('actor')
                if aname not in self.scenario.system.actorNamed:
                    raise ValueError('Error at line %i: actor "%s" does not exist' % (
                        _S.line_no,
                        aname,
                    ))
                a=self.scenario.system.actorNamed[aname]
                ai = ActorInstance(
                    scenario=self.scenario,
                    name=iname,
                    actor=a,
                    lineNo=_S.line_no
                )
                self.scenario.actorInstanceNamed[aname]=ai
                continue

            #---- -- @context
            r = prefix+'-- *@context'+end
            m = re.match(r, line)
            if m:
                if _S.context_block is None:
                    _S.context_block=ContextBlock(
                        self.scenario,
                        lineNo=_S.line_no,
                    )
                    print('Opening context')
                continue

            #---- -- @endcontext
            r = prefix+'-- *@endcontext'+end
            m = re.match(r, line)
            if m:
                if _S.context_block is None:
                    raise ValueError(
                        'Error at line %i: context is not open' % (
                            _S.line_no,
                        ))
                _S.context_block=None
                print('Closing context')
                continue

            #---- -- @uci
            r = (prefix
                 +r'-- *@uci'
                 +r' +(?P<name>\w+)'
                 # +r' *(: *(?P<actor>\w+))?'  # TODO: add online definition
                 +r' *(?P<usecase>\w+)'
                 +end)
            m = re.match(r, line)
            if m:
                if self.system is None:
                    print('Warning at line %i: no use case model provided. Directive ignored' % (
                        _S.line_no,
                    ) )
                    continue
                if _S.context_block is not None:
                    raise ValueError(
                        'Error at line %i: context is open' % (
                            _S.line_no,
                        ))
                ainame=m.group('name')
                if ainame not in self.scenario.actorInstanceNamed:
                    raise ValueError(
                        'Error at line %i: actori "%s" is not defined' % (
                            _S.line_no,
                            ainame,
                        ))
                ai=self.scenario.actorInstanceNamed[ainame] #type: ActorInstance
                a=ai.actor #type: Actor
                ucname=m.group('usecase')
                if ucname not in self.scenario.system.usecaseNamed:
                    raise ValueError(
                        'Error at line %i: usecase "%s" is not defined' % (
                            _S.line_no,
                            ucname,
                        ))
                uc=self.scenario.system.usecaseNamed[ucname] #type: Usecase
                if uc not in a.usecases:
                    raise ValueError(
                        'Error at line %i: actor %s cannot perform usecase %s' % (
                            _S.line_no,
                            a.name,
                            uc.name,
                        ))
                _S.main_block=UsecaseInstanceBlock(
                    scenario=self.scenario,
                    actorInstance=ai,
                    useCase=uc,
                    lineNo=_S.line_no,
                )
                continue

            #---- -- @enduci
            r = (prefix
                 +r'-- *@enduci'
                 +end)
            m = re.match(r, line)
            if m:
                if self.system is None:
                    print('Warning at line %i: no use case model provided. Directive ignored' % (
                        _S.line_no,
                    ) )
                    continue
                if not isinstance(_S.main_block, UsecaseInstanceBlock):
                    raise ValueError(
                        'Error at line %i: no opened usecase instance' % (
                            _S.line_no,
                        ))
                _S.main_block=None
                continue

            #---- blank lines ---------------------------------------------
            r = prefix+''+end
            m = re.match(r, line)
            if m:
                continue

            #--- unrecognized directive ----------------------------------------
            r = (begin+'-- *@.*'+end)
            m = re.match(r, line)
            if m:
                print('Warning at line %i: directive not recognized: %s' % (
                    _S.line_no,
                    _S.original_line
                ))
                continue

            #---- comments -------------------------------------------------
            r = prefix+'--.*'+end
            m = re.match(r, line)
            if m:
                continue

            #--- object creation (create x : C) ---------------------
            r = begin+r'! *create +(?P<name>\w+) *: *(?P<className>\w+)'+end
            m = re.match(r, line)
            if m:
                variable=m.group('name')
                classname=m.group('className')
                id=None
                if DEBUG:
                    print('%s := new %s' % (variable,classname))

                ObjectCreation(
                    block=_getBlock(),
                    variableName=variable,
                    class_=self.classModel.classNamed[classname],
                    id=id,
                    lineNo=_S.line_no
                )
                continue

            #--- object creation(x := new C('lila') --------------------
            r = (begin
                 + r'! *(?P<name>\w+) *:= *new +(?P<className>\w+)'
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
                    block=_getBlock(),
                    variableName=variable,
                    class_=self.classModel.classNamed[classname],
                    id=id,
                    lineNo=_S.line_no
                )
                continue

            #--- attribute assignement ----------------------------------------
            r = (begin
                    + r'! *(set )? *(?P<name>\w+) *'
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
                    block=_getBlock(),
                    variableName=variable,
                    attributeName=attribute,
                    expression=expression,
                    lineNo=_S.line_no,
                )
                continue

            #--- link creation-------------------------------------------------
            r = (begin
                 + r'! *insert *\((?P<names>[\w, ]+)\) *'
                 + r'into +'
                 + r'(?P<associationName>\w+)'
                 + end )
            m = re.match(r, line)
            if m:
                names = [
                    n.strip()
                    for n in m.group('names').split(',')]
                # print('D'*5,m.group('names'))
                # print('     ',names)
                assoc=self.classModel.associationNamed[m.group('associationName')]
                if DEBUG:
                    print('new (%s) : %s' % (
                        ','.join(names),
                        assoc.name ))
                LinkCreation(
                    block=_getBlock(),
                    names=names,
                    association=assoc,
                    id=None,
                    lineNo=None
                )
                continue

            #--- link object creation (form1 ) --------------------------------
            # ex: create r1 : Rent between (a1,b2)
            r = (begin
                 + r'! *create +(?P<name>\w+) *: *(?P<assocClassName>\w+) +'
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
                    block=_getBlock(),
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
                 + r'! *(?P<name>\w+) *:='
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
                    block=_getBlock(),
                    variableName=name,
                    names=names,
                    id=id,
                    associationClass=ac,
                    lineNo=None
                )
                continue




            #--- object (or link object) destruction --------------------------
            r = (begin
                 + r'! *destroy +(?P<name>\w+)'+ end )
            m = re.match(r, line)
            if m:
                name = m.group('name')
                if DEBUG:
                    print( 'delete object %s' % name )
                ObjectDestruction(
                    block=_getBlock(),
                    variableName=name,
                )
                continue
                # check if this is an regular object or a link object
                # if name in self.state.objects:
                #     del self.state.objects[name]
                # else:
                #     del self.state.linkObject[name]
                # continue

            #--- link destruction ---------------------------------------------
            r = (begin
                 + r'! *delete *\((?P<objectList>[\w, ]+)\)'
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
                continue



            #---- unknown or unimplemented commands ---------------------------
            print( 'Error: pyuseocl cannot parse line #%s: %s' %(
                _S.line_no,
                _S.original_line
            ))

            raise NotImplementedError(line)


