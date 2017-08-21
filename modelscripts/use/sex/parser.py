# coding=utf-8

"""
Parser of subset of the soil language and of the sex format.
The same parser can parse both:
* .soil files, that is USE .soil files
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

# Scn: Assertion
# TODO: add @assert inv X::Y is True|False   -> check -d -v
# TODO: add @assert inv * is True|False      -> check -d -v
# TODO: add @assert query expr is result     -> ??


# TODO: add proper mamangement for Warning and Errors
# TODO: check if a USE OCL run before parsin is necessary/better

from __future__ import unicode_literals, print_function, absolute_import, division
from typing import Text, Optional, Union, List, Dict
import os
import re

DEBUG=3

from modelscripts.use.engine import USEEngine

from modelscripts.source.sources import SourceFile

from modelscripts.use.sex.printer import (
    SoilPrinter,
    SexPrinter
)


from modelscripts.metamodels.classes import (
    ClassModel,
)

from modelscripts.metamodels.usecases import (
    UsecaseModel,
    Actor,
    Usecase,
    System,
)
from modelscripts.metamodels.scenarios import (
    ScenarioModel,
    ActorInstance,
    ContextBlock,
)
from modelscripts.metamodels.scenarios.blocks import (
    UsecaseInstanceBlock,
    TopLevelBlock,
)
from modelscripts.metamodels.scenarios.operations import (
    ObjectCreation,
    ObjectDestruction,
    LinkCreation,
    LinkDestruction,   #TODO: implement link destruction
    LinkObjectCreation,
    AttributeAssignment,
    Check,
    Query,
)

from modelscripts.metamodels.scenarios.evaluations import (
    ScenarioEvaluation,
    CheckEvaluation,
    InvariantValidation,
    InvariantViolation,
    CardinalityViolation,
    CardinalityViolationObject,
    QueryEvaluation,
)

__all__ = (
    'SoilSource',
    'SexSource',
)


def isEmptySoilFile(file):
    with open(file) as f:
        content = f.read()
    match = re.search(r'(^ *!)|(^ *open)', content, re.MULTILINE)
    return match is None


#TODO: add support for use interpreter errors !!!


class _PolymorphicSource(SourceFile):
    def __init__(self,
                 classModel, soilFileName, parseExecution=True, usecaseModel=None):
        #type: (ClassModel, Text, bool, Optional[UsecaseModel]) -> None
        """
        Create a soil/sex source from the given file.
        In order to do this a class model is necessary to resolve
        class names and operation names in operation.
        A use case model is also necessary, but only if
        there are directives for actor instance and usecase instance.
        """
        super(_PolymorphicSource, self).__init__()

        self.fileKind='sex' if parseExecution else 'soil'
        self.parseExecution=parseExecution
        self.hasExecutionResult=parseExecution
        self.soilFileName=soilFileName
        self.classModel = classModel #type:ClassModel
        self.usecaseModel = usecaseModel #type:Optional[System]
        self.useFileName=self.classModel.source.fileName
        if not os.path.isfile(soilFileName):
            raise Exception('File "%s" not found' % soilFileName)

        self.scenario = ScenarioModel(    #type:ScenarioModel
            source=self,
            classModel=classModel,
            name=None,
            usecaseModel=usecaseModel,
            file=self.soilFileName)

        self.fileToParse=self.getFileToParse()
        self.sourceLines = (
            line.rstrip()
            for line in open(self.fileToParse, 'rU'))
        self.isValid = None #type:Optional[bool]
        self.errors = []
        self.lines = None #type:List[Text]
        self.ignoredLines = []

        if self.hasExecutionResult:
            self.scenarioEvaluation=ScenarioEvaluation(self.scenario)
        else:
            self.scenarioEvaluation=None

        if self.fileKind=='soil':
            prefix='^'
        else:
            prefix='^(\d{5}|\|{5}):'
        self._parse(prefix)
        self.isValid=True # Todo, check errors, etc.

    def getFileToParse(self):
        if self.parseExecution:
            filename=USEEngine.executeSoilFileAsSex(
                useFile=self.useFileName,
                soilFile=self.soilFileName)
        else:
            filename=self.soilFileName
            # Get directly the .soil file
        print('XXXXXXXXXXX %s' % filename)
        return filename


    def printStatus(self):
        """
        Print the status of the file:

        * the list of errors if the file is invalid,
        * a short summary of entities (classes, attributes, etc.) otherwise
        """
        print('****************************************')

        if self.isValid:
            p=None
            if self.hasExecutionResult:
                p=SoilPrinter(
                    scenario=self.scenarioEvaluation,
                    displayLineNos=True)
            else:
                p=SexPrinter(
                    scenario=self.scenario,
                    displayLineNos=True)

            print(p.do())
            print('****************qqqq*******************')
        else:
            print('***************sdf*********************')

            print('%s error(s) in the model' % len(self.errors))
            for e in self.errors:
                print(e)

    def _parse(self, prefix):

        class _S(object):
            """
            Current state of the parser.
            Required for _getBlock
            """
            original_line=""

            # Always the line number in the soil file, the only file seen be the user
            line_no=0
            # The line number in the sex file or None if parsing a soil file
            sex_line_no=None

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


        begin = prefix + r' *'
        end = ' *$'



        if DEBUG>=1:
            print('\nParsing %s with %s usecase model\n' % (
                self.soilFileName,
                'no' if self.usecaseModel is None else 'a'
            ))

        last_check_evaluation=None
        current_cardinality_info=None
        current_invariant_violation=None
        current_query_evaluation=None

        for (line_index, line) in enumerate(self.sourceLines):

            _S.original_line = line
            line = line.replace('\t',' ')


            # Compute the line number
            if self.parseExecution:  #'sex':
                _S.sex_line_no = line_index + 1
                _m=re.match(r'^(?P<lineno>\d{5}):', line)
                if _m:
                    # in case of sex file update the line no from the line begining
                    _S.line_no=int(_m.group('lineno'))
                else:
                    # This is a result line. |||||: Do nothing.
                    # The same line number to the soil will be reused.
                    pass
            else:
                _S.line_no = line_index + 1

            if DEBUG>=2:
                if self.parseExecution: #'sex':
                    print ('#%05i <- %05i : %s' % (
                        _S.line_no,
                        _S.sex_line_no,
                        _S.original_line,
                    ))
                else:
                    print('#%05i : %s' % (
                        _S.line_no,
                        _S.original_line,
                    ))

            #---- blank lines ---------------------------------------------
            r = prefix+''+end
            m = re.match(r, line)
            if m:
                continue



            #---- query
            r = begin+'(?P<kind>\?\??) *(?P<expr>.*)'+end
            m = re.match(r, line)
            if m:
                query=Query(
                    block=_getBlock(),
                    expression=m.group('expr'),
                    verbose=m.group('kind')=='??',
                    lineNo=_S.line_no,
                )
                if self.hasExecutionResult:
                    current_query_evaluation = QueryEvaluation(
                        scenarioEvaluation=self.scenarioEvaluation,
                        query=query)
                continue


            #-------------------------------------------------
            # directives
            #-------------------------------------------------

            if re.match(begin+r'--', line):
                #---- -- @scenario XXX
                r = begin+'-- *@scenario( +model?) +(?P<name>\w+)'+end
                m = re.match(r, line)
                if m:
                    if self.scenario.name is not None:
                        raise ValueError(
                            'Error at line #%i: '
                            'scenario named again' % _S.line_no)
                    self.scenario.name=m.group('name')
                    self.scenario.lineNo=_S.line_no,

                    # TODO: raise an effor if some block has already there
                    continue

                #---- -- @actorinstance XXX : YYY
                r = prefix+'-- *@actori +(?P<name>\w+) *: *(?P<actor>\w+)'+end
                m = re.match(r, line)
                if m:
                    if self.usecaseModel is None:
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
                    if aname not in self.scenario.usecaseModel.actorNamed:
                        raise ValueError('Error at line %i: actor "%s" does not exist' % (
                            _S.line_no,
                            aname,
                        ))
                    a=self.scenario.usecaseModel.actorNamed[aname]
                    ai = ActorInstance(
                        scenario=self.scenario,
                        name=iname,
                        actor=a,
                        lineNo=_S.line_no
                    )
                    self.scenario.actorInstanceNamed[iname]=ai
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
                    if self.usecaseModel is None:
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
                    if ucname not in self.scenario.usecaseModel.system.usecaseNamed:
                        raise ValueError(
                            'Error at line %i: usecase "%s" is not defined' % (
                                _S.line_no,
                                ucname,
                            ))
                    uc=self.scenario.usecaseModel.system.usecaseNamed[ucname] #type: Usecase
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
                    if self.usecaseModel is None:
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



            # -------------------------------------------------
            # ! operations
            # -------------------------------------------------

            if re.match(begin + r'!', line):

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
                        lineNo=_S.line_no
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
                        lineNo=_S.line_no
                    )
                    continue

                #--- link object creation (form2 ) --------------------------------
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
                        print(("new %s('%s') between (%s)" % (
                            assoc_class_name,
                            id,
                            ','.join(names)
                        )))
                    LinkObjectCreation(
                        block=_getBlock(),
                        variableName=name,
                        names=names,
                        id=id,
                        associationClass=ac,
                        lineNo=_S.line_no
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
                    raise NotImplementedError('FIXME: implement link destruction')
                    # continue




            #==========================================================
            #  results of evaluation
            #==========================================================

            if self.parseExecution and line.startswith('|||||:'): # sex



                #------------------------------------------------------
                #  Cardinality evaluation
                #------------------------------------------------------

                r=(begin
                   +'checking structure...'
                   +end)
                # for some reason this appear as a blank line when
                # redirecting in a file. It was blank so the algorithm
                # below does not take it into account.
                m = re.match(r, line)
                if m:
                    continue

                r=(begin
                   +'checked structure in .*\.'
                   +end)
                # like "check structure...
                m = re.match(r, line)
                if m:
                    continue

                r=(begin
                    +r'Multiplicity constraint violation in association '
                    +r'`(?P<association>\w+)\':'
                    +end)
                m = re.match(r, line)
                if m:
                    current_cardinality_info={
                        'associationName':m.group('association')
                    }
                    continue

                if current_cardinality_info:
                    r=(begin
                        +r'  Object `(?P<object>\w+)\' of class '
                        +r'`(?P<sourceClass>\w+)\' is connected to '
                        +r'(?P<numberOfObjects>\d+) objects of class '
                        +r'`(?P<targetClass>\w+)\''
                        +end)
                    m = re.match(r, line)
                    if m:
                        current_cardinality_info['objectName']=m.group('object')
                        current_cardinality_info['sourceClassName']=(
                            m.group('sourceClass'))
                        current_cardinality_info['targetClassName'] = (
                            m.group('targetClass'))
                        current_cardinality_info['numberOfObjects'] = (
                            int(m.group('numberOfObjects')))
                        continue

                    r = (begin
                        +r'  at association end `(?P<role>\w+)\' but the '
                        +r'multiplicity is specified as'
                        +r' `(?P<cardinality>[^\']+)\'.'
                        +end)
                    m = re.match(r, line)
                    if m:
                        role=self.classModel.findRole(
                            current_cardinality_info['associationName'],
                            m.group('role'))
                        if role in last_check_evaluation.cardinalityEvaluations:
                            card_eval = (
                                last_check_evaluation.cardinalityEvaluations[role])
                        else:
                            card_eval = (
                                CardinalityViolation(
                                    checkEvaluation=last_check_evaluation,
                                    role=role,
                                ))
                        CardinalityViolationObject(
                            cardinalityViolation=card_eval,
                            violatingObject=(
                                current_cardinality_info['objectName']
                            ),
                            actualCardinality=(
                                current_cardinality_info['numberOfObjects']
                            )
                        )

                        continue



                #------------------------------------------------------
                #  Invariant evaluation
                #------------------------------------------------------

                r=(begin
                    +r'checked \d+ invariants in .*'
                    +end)
                m = re.match(r, line)
                if m:
                    current_invariant_violation=None
                    continue

                r=(begin
                   +'checking invariants...'
                   +end)
                # like "check structure...
                m = re.match(r, line)
                if m:
                    continue

                r=(begin
                    +r'checking invariant \(\d+\) `'
                    +r'(?P<context>\w+)'
                    +r'::(?P<invname>\w+)'
                    +r'\': '
                    +r'(?P<result>OK|FAILED)\.'
                    +end)
                m = re.match(r, line)
                if m:
                    invariant=self.classModel.findInvariant(
                        classOrAssociationClassName=m.group('context'),
                        invariantName=m.group('invname')
                    )
                    if m.group('result')=='OK':
                        InvariantValidation(
                            checkEvaluation=last_check_evaluation,
                            invariant=invariant,
                        )
                    else:
                        current_invariant_violation=InvariantViolation(
                            checkEvaluation=last_check_evaluation,
                            invariant=invariant,
                        )
                    continue

                if current_invariant_violation:

                    r=(begin
                        +r'Results of subexpressions:'
                        +end)
                    m = re.match(r, line)
                    if m:
                        continue



                    r=(begin
                        +r'Instances? of \w+ violating the invariant:'
                        +end)
                    m = re.match(r, line)
                    if m:
                        continue

                    r=(begin
                        +r'  -> Set\{(?P<expr>[\w ,]+)\}'
                        +r' : Set\((?P<type>\w+)\)'
                        +end)
                    m = re.match(r, line)
                    if m:
                        names=[ x.strip()
                                for x in m.group('expr').split(',')
                                if x!='' ]
                        current_invariant_violation.violatingObjects=names
                        current_invariant_violation.violatingObjectsType=m.group('type')
                        current_invariant_violation.violatingObjectType=m.group('type')
                        current_invariant_violation=None
                        continue

                    # WARNING: this rule MUST be after the one
                    # like -> Set\{ ...
                    # Otherwise this one catch the other one
                    r=(begin
                        +r'  -> (?P<expr>.*) : (?P<type>.*)'
                        +end)
                    m = re.match(r, line)
                    if m:
                        current_invariant_violation.resultValue=m.group('expr')
                        current_invariant_violation.resultType=m.group('type')
                        continue

                    # WARNING: this rule MUST be at the end
                    # Otherwise this one catch the other ones
                    r=(begin
                        +r'  (?P<expr>.*)'
                        +end)
                    m = re.match(r, line)
                    if m:
                        current_invariant_violation.subexpressions.append(
                            m.group('expr'))
                        continue

                #------------------------------------------------------
                #  query evaluation
                #------------------------------------------------------

                if current_query_evaluation:
                    r = (begin
                         + r'Detailed results of subexpressions:'
                         + end)
                    m = re.match(r, line)
                    if m:
                        continue

                    r=(begin
                        +r'  (?P<expr>.*)'
                        +end)
                    m = re.match(r, line)
                    if m:
                        current_query_evaluation.subexpressions.append(m.group('expr'))
                        continue

                    r=(begin
                        +r'-> (?P<expr>.*) : (?P<type>.*)'
                        +end)
                    m = re.match(r, line)
                    if m:
                        current_query_evaluation.resultValue=m.group('expr')
                        current_query_evaluation.resultType=m.group('type')
                        current_query_evaluation=None
                        continue


            # ---- check
            # WARNING: this rule MUST go after the rules thats starts
            # with 'check' something as this one will take precedence!
            r = begin + 'check *(?P<params>( -[avd])*)' + end
            m = re.match(r, line)
            if m:
                check = Check(
                    block=_getBlock(),
                    verbose='v' in m.group('params'),
                    showFaultyObjects='d' in m.group('params'),
                    all='a' in m.group('params'),
                    lineNo=_S.line_no,
                )
                if self.hasExecutionResult:
                    last_check_evaluation = CheckEvaluation(
                        scenarioEvaluation=self.scenarioEvaluation,
                        check=check)
                continue


            #---- unknown or unimplemented commands ---------------------------

            raise NotImplementedError(
                'Error at line #%i: cannot parse this line\n'
                   '"%s"' % (_S.line_no,_S.original_line)
            )


class SoilSource(_PolymorphicSource):
    """
    Source corresponding directly to the raw .soil source given
    as the parameter. USE is *NOT* executed so some errors may
    be left undiscovered. Moreover, there is no cardinality check,
    no invariant checking, etc.
    From this one can get an object model.
    """

    def __init__(self, classModel, soilFileName, usecaseModel=None):
        #type: (ClassModel, Text, Optional[UsecaseModel]) -> None
        super(SoilSource, self).__init__(
            parseExecution=False,
            classModel=classModel,
            soilFileName=soilFileName,
            usecaseModel=usecaseModel,
        )


class SexSource(_PolymorphicSource):
    """
    Source corresponding to a scenario execution.
    The the .soil file merged with the trace of
    the execution of USE .soil file.
    """
    def __init__(self, classModel, soilFileName, usecaseModel=None):
        #type: (ClassModel, Text, Optional[UsecaseModel]) -> None
        super(SexSource, self).__init__(
            parseExecution=True,
            classModel=classModel,
            soilFileName=soilFileName,
            usecaseModel=usecaseModel,
        )

