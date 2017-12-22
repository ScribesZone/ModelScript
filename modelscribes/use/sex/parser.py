# coding=utf-8

"""
Parser of subset of the soil language and of the sex format.
Parser of subset of the soil language and of the sex format.
The same parser can parse both:
* .soil files, that is USE .soil files (NOT MAINTAINED anymore)
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

# FIXME: check what to do with optional class model

from __future__ import unicode_literals, print_function, absolute_import, division

import os
import re

from typing import Text, Optional, Union, List



from abc import ABCMeta

from modelscribes.use.engine import USEEngine

from modelscribes.base.parsers import DocCommentLines
from modelscribes.base.preprocessors import Preprocessor
from modelscribes.megamodels.sources import ModelSourceFile

from modelscribes.base.issues import (
    Issue,
    LocalizedSourceIssue,
    Levels,
    FatalError,
)
from modelscribes.base.files import (
    replaceExtension
)

from modelscribes.interfaces.environment import (
    Environment
)
from modelscribes.metamodels.glossaries import (
    GlossaryModel,
)

from modelscribes.scripts.classes.parser import (
    ClassModelSource
)
from modelscribes.metamodels.classes import (
    ClassModel,
)

from modelscribes.metamodels.usecases import (
    UsecaseModel,
    Actor,
    Usecase,
)
from modelscribes.metamodels.scenarios import (
    ScenarioModel,
    ActorInstance,
    ContextBlock,
    METAMODEL
)
from modelscribes.metamodels.scenarios.blocks import (
    UsecaseInstanceBlock,
    TopLevelBlock,
)
from modelscribes.metamodels.scenarios.operations import (
    ObjectCreation,
    ObjectDestruction,
    LinkCreation,
    #TODO: implement link destruction
    LinkObjectCreation,
    AttributeAssignment,
    Check,
    Query,
    AssertQuery
)

from modelscribes.metamodels.scenarios.evaluations.operations import (
    _USEImplementedQueryEvaluation,
    _USEImplementedCheckEvaluation,
    InvariantValidation,
    InvariantViolation,
    CardinalityViolation,
    CardinalityViolationObject,
)

from modelscribes.metamodels.permissions import (
    PermissionModel
)

from modelscribes.scripts.megamodels.parser import (
    isMegamodelStatement
)

DEBUG=0
#DEBUG=0


__all__ = (
    # 'SoilSource',
    'SexSource',
)


def isEmptySoilFile(file):
    with open(file) as f:
        content = f.read()
    match = re.search(r'(^ *!)|(^ *open)', content, re.MULTILINE)
    return match is None


class _SexOrSoilSource(ModelSourceFile):
    __metaclass__ = ABCMeta

    def __init__(self,
                 evaluateScenario,
                 originalFileName,
                 allowedFeatures=(
                         'permission',   # not used yet
                         'access', # not used yet
                         'update',
                         'check',
                         'assertQuery',
                         'assocClass',
                         'delete',
                         'query',
                         'usecase',
                         'context',
                         'createSyntax',
                         'topLevelBlock'),
                 parsePrefix='^',
                 preIssueMessages=()):
        #type: (bool,Text, List[Text], Text, Text, List[Text]) -> None

        # TODO:3 check obsolete comment
        """

        Initialize the soil/sex sources attributes
        but DO NOT parse the file for now.
        The parseToFillModel() method is called explictely in
        the concrete subclasses.
        See subclasses

        Args:
            evaluateScenario:
                If true, the scenario has been executed
                WITH USE
            and it will have an scenarioEvaluation associated.
            allowedFeatures:
                'delete'
                'query'
                'usecase'
                'context'
                'createSyntax'
            parsePrefix:
                See subclasses. Prefix is necessary for parsing sex file.
                Only used if evaluateScenario.
            preIssueMessages:
                If not [] these errors with be added to the list of
                error and nothing else will happen.

        """

        # TODO:3 check obsolete comment
        """

            originalFileName:
                The name of the soil file.
                If evaluateScenario the sex file generated
                (generated previously) will be parsed instead of
                originalFileName.
            classModel:
                The class model used to resolve Classes, Associations, etc.
                If not provided the source may contains some errors.
                This is checked dynamically and a Fatal error will be
                raised. If not provided to the constructor
                an import can set the class model source.
            usecaseModel:
                A use case model is necessary only if there are
                directives for actor instance and usecase instance.
                If not provided warning will be generated.
                Usecase Model can be used without evaluateScenario.
            permissionModel:
                In case of evaluateScenario used to check accesses.
                No permission will be checked at all if not provided.
        """
        self.evaluateScenario=evaluateScenario  #type: bool
        self.soilFileName=originalFileName  #type: Text
        self._parsePrefix=parsePrefix

        # Call the super class.
        # - creates an empty model of type metamodel
        # - read the logical (.soil) file
        # - parse import statements (ImportBox)
        # - parsing will be done later
        if DEBUG>=2:
            print(
                'sxp: reading/parsing the file %s for imports' %
                originalFileName)
        super(_SexOrSoilSource, self).__init__(
            fileName=originalFileName,
            realFileName=None,  # will be set later
            preErrorMessages=preIssueMessages,
            readFileLater=False,
            fillImportBoxLater=False,
            parseFileLater=True,
            noSymbolChecking=False,
            allowedFeatures=allowedFeatures,
            prequelFileName=originalFileName,
            recognizeUSEOCLNativeModelDefinition=False)
        if DEBUG>=2:
            print(
                'sxp: reading/parsing file for imports done')

        self.scenarioModel.usecaseModel=self.usecaseModel
        self.scenarioModel.classModel=self.classModel
        self.scenarioModel.permissionModel=self.permissionModel
        self.scenarioModel.glossaryModel=self.glossaryModel

    @property
    def classSource(self):
        #type: () -> Optional[ClassModelSource]
        return self.importBox.sourceFile('cl')

    @property
    def classModel(self):
        #type: () -> Optional[ClassModel]
        # TODO: the optional stuff should come from metamdel
        return self.importBox.model('cl', optional='True')

    @property
    def usecaseModel(self):
        #type: () -> Optional[UsecaseModel]
        # TODO: the optional stuff should come from metamdel
        return self.importBox.model('us', optional='True')

    @property
    def glossaryModel(self):
        # TODO: the optional stuff should come from metamdel
        #type: () -> Optional[GlossaryModel]
        return self.importBox.model('gl', optional='True')

    @property
    def permissionModel(self):
        #type: () -> Optional[PermissionModel]
        # TODO: the optional stuff should come from metamdel
        return self.importBox.model('pe', optional='True')

    @property
    def scenarioModel(self):
        #type: () -> ScenarioModel
        m=self.model #type: ScenarioModel
        return m

    # @property
    # def scenarioModel(self):
    #     m=self.model #type: ScenarioModel
    #     return m

    @property
    def metamodel(self):
        return METAMODEL





    def parseToFillModel(self):
        """
        This method is called after the constructor because
        the reading of the file must be deferred in the case
        of sex file
        """
        try:
            self._parse(self._parsePrefix)
            if self.isValid:
                if not self.scenarioModel.isEvaluated:  # .model. but typing
                    self.model.evaluate()

        # else:
        #     self.scenario=None
        except FatalError:
            # The fatal error has already been already registered
            # so nothing else to do here.
            pass
        pass



    def _parse(self, prefix):
        #type: (Text) -> None

        def _entityError(e, suffix=''):
            return '%s are not allowed%s' % (e, suffix)

        class _S(object):
            """
            Current state of the parser.
            Required for _getBlock
            """
            original_line=''

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
            #: can be nested in other blocks (in practice in should not as one cannot find the order of execution based on blocks)



        def _get_block():
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
                        model=self.scenarioModel,
                        lineNo=_S.line_no
                    )
                return _S.main_block

        def _has_error_next():
            if not self.evaluateScenario:
                return False
            if _S.sex_line_no >= len(self.realSourceLines):
                return False
            else:
                nextline=self.realSourceLines[_S.sex_line_no]
                return _is_error_line(nextline)

        def _reqClassModel():
            """ Check that the model is available"""
            if self.classModel is None:
                LocalizedSourceIssue(
                    sourceFile=self,
                    level=Levels.Fatal,
                    message='No class model imported.',
                    line=_S.line_no)
            else:
                return self.classModel

        def _is_error_line(line):
            # print(line)
            m1=re.match('^\|\|\|\|\| *<[^>]>.*', line)
            m2=re.match('^\|\|\|\|\| *:?(Error|ERROR|Warning|WARNING)',line)
            return m1 is not None or m2 is not None

        begin = prefix + r' *'
        end = ' *$'

        if DEBUG>=1:
            print('\nsxp: Parsing %s with %s usecase model\n' % (
                self.soilFileName,
                'no' if self.usecaseModel is None else 'a'
            ))

        last_check_evaluation=None
        current_cardinality_info=None
        current_invariant_violation=None
        current_query_evaluation=None
        last_doc_comment = DocCommentLines()
        last_text_block_lines = []
        in_block_comment = False
        current_eol_comment=None
        current_element=self.model

        for (line_index, line) in enumerate(self.realSourceLines):

            _S.original_line = line
            line = line.replace('\t',' ')


            # Compute the line number
            if self.evaluateScenario:  #'sex':
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

            # skip the line if there is a (USE) error on the next
            # line. This avoid reporting error twice. One time for
            # this parser (first) and then another while discovering
            # the USE error on the next line.
            if _has_error_next():
                continue

            if DEBUG>=2:
                if self.evaluateScenario: #'sex':
                    print ('sxp: #%05i <- %05i : %s' % (
                        _S.line_no,
                        _S.sex_line_no,
                        _S.original_line,
                    ))
                else:
                    print('sxp: #%05i : %s' % (
                        _S.line_no,
                        _S.original_line,
                    ))

            # ----------------------------------
            # Single and multi line /* */
            # ----------------------------------

            # replace inline /* */ by spaces
            line = re.sub(r'(/\*.*?\*/)', ' ', line)

            # deal with /* comments
            r = begin+' */\*.*'+end
            m = re.match(r, line)
            if m:
                in_block_comment = True
                last_doc_comment.clean()
                continue

            if in_block_comment:
                r = begin+'^.*\*/(?P<rest>.*)'+end
                m = re.match(r, line)
                if m:
                    in_block_comment = False
                    last_doc_comment.clean()
                    line = m.group('rest')
                    # do not start the loop, the rest could be important

            if in_block_comment:
                last_doc_comment.clean()
                continue

            #--------------------------------------------------
            # Blank lines
            #--------------------------------------------------
            # This must go after /* */ comments as such a
            # comment can create a blank line
            r = prefix+''+end
            m = re.match(r, line)
            if m:
                last_doc_comment.clean()
                continue

            # ------------------------------------------
            # Description
            # ------------------------------------------


            r = prefix+'--\|(?P<line>.*)'+end
            m = re.match(r, line)
            if m:
                _line = m.group('line')
                # if current_element is not None:
                #     current_element.description.addNewLine(
                #         stringLine=_line,
                #         lineNo=_S.line_no,
                #     )
                last_text_block_lines+=_line
                continue

    # TODO: to restore
            # #---------------------------------
            # # Line comment --
            # #---------------------------------
            #
            # # TODO: check comment processing appiled in use parser
            # Full line comment
            r = prefix+' *--(?P<comment>[^@]?.*)'+end
            m = re.match(r, line)
            if m:
                c=m.group('comment')
                last_doc_comment.add(c)
                continue

            # Everything that follow is not part of a full line comment
            last_doc_comment.clean()

            #--------------------------------------------------
            # EOL comment --
            #--------------------------------------------------
            # TODO: check comment processing appiled in use parser
            # End of line (EOL comment)
            r = r'^(?P<content>.*?)--(?P<comment>[^@]?.*)$'
            m = re.match(r, line)
            if m:
                # There is a eol comment on this line
                # all following cases can use this variable
                current_eol_comment = m.group('comment')
                # we go though the next cases without the eol
                line=m.group('content')
            else:
                current_eol_comment = None
            # Don't stop the loop, the rest of the line has to
            # be processed.


            #--------------------------------------------------
            # assert query
            #--------------------------------------------------
            r = begin+'(?P<kind>\?\??) *(?P<expr>.*) *(?P<assert>--@assert) *'+end
            m = re.match(r, line)
            if m:
                if not self.checkAllowed(
                        feature='assertQuery',
                        lineNo=_S.line_no,
                        message=_entityError(
                            'Assertions', '.  Skipped.'),
                        level=Levels.Error):
                    continue
                assert_query=AssertQuery(
                    block=_get_block(),
                    expression=m.group('expr'),
                    verbose=m.group('kind') == '??',
                    lineNo=_S.line_no,
                )
                if self.evaluateScenario:
                    current_query_evaluation = (
                        _USEImplementedQueryEvaluation(
                            blockEvaluation=None,
                            op=assert_query))
                continue

            # --- megamodel statements -------------
            # currently useless as megastmt are replace by ''
            is_mms = isMegamodelStatement(
                lineNo=_S.line_no,
                modelSourceFile=self)
            if is_mms:
                # megamodel statements have already been
                # parse so silently ignore them
                continue
            pass

            #--------------------------------------------------
            # query
            #--------------------------------------------------
            r = begin+'(?P<kind>\?\??) *(?P<expr>.*) *'+end
            m = re.match(r, line)
            if m:
                if not self.checkAllowed(
                        feature='query',
                        lineNo=_S.line_no,
                        message=_entityError(
                            'Queries', '.  Skipped.'),
                        level=Levels.Error):
                    continue
                query=Query(
                    block=_get_block(),
                    expression=m.group('expr'),
                    verbose=m.group('kind')=='??',
                    lineNo=_S.line_no,
                )
                if self.evaluateScenario:
                    current_query_evaluation = (
                        _USEImplementedQueryEvaluation(
                            blockEvaluation=None,
                            op=query))
                continue

            # --- megamodel statements -------------
            # currently useless as megastmt are replace by ''
            is_mms = isMegamodelStatement(
                lineNo=_S.line_no,
                modelSourceFile=self)
            if is_mms:
                # megamodel statements have already been
                # parse so silently ignore them
                continue
            pass

            #-------------------------------------------------
            # directives
            #-------------------------------------------------

            if re.match(begin+r'--@', line):

                # -------------------------------
                # @actorinstance <actor> : <instance>
                # -----------------------------------

                r = (prefix
                     +'-- *@actori +(?P<name>\w+) *'
                     +': *(?P<actor>\w+)'
                     +end)
                m = re.match(r, line)
                if m:
                    if not self.checkAllowed(
                            feature='usecase',
                            lineNo=_S.line_no,
                            message=_entityError(
                                'Actor instances', '. Skipped.'),
                            level=Levels.Error):
                        continue

                    if self.usecaseModel is None:
                        LocalizedSourceIssue(
                            sourceFile=self,
                            level=Levels.Warning,
                            message='No usecase model provided. Directive ignored',
                            line=_S.line_no
                        )
                        continue

                    #--- instance --------
                    iname=m.group('name')
                    if iname in self.scenarioModel.actorInstanceNamed:
                        LocalizedSourceIssue(
                            sourceFile=self,
                            level=Levels.Warning,
                            message='Actor instance "%s" already exist. Directive ignored' % iname,
                            line=_S.line_no
                        )
                        continue

                    #--- actor ----------
                    aname=m.group('actor')
                    if aname not in self.scenarioModel.usecaseModel.actorNamed:
                        LocalizedSourceIssue(
                            sourceFile=self,
                            level=Levels.Error,
                            message='Actor "%s" does not exist. Directive ignored.' % aname,
                            line=_S.line_no
                        )
                        continue

                    a=self.scenarioModel.usecaseModel.actorNamed[aname]
                    ai = ActorInstance(
                        model=self.scenarioModel,
                        name=iname,
                        actor=a,
                        lineNo=_S.line_no
                    )
                    self.scenarioModel.actorInstanceNamed[iname]=ai
                    continue

                # -------------------------------
                # @systemI <system> : <system>
                # -----------------------------------

                r = (prefix
                     +'--@system +(?P<name>\w+) *'
                     +': *(?P<actor>\w+)'
                     +end)
                m = re.match(r, line)
                if m:
                    LocalizedSourceIssue(
                        sourceFile=self,
                        level=Levels.Warning,
                        message='Definition of system instance not implemented yet. Ignored',
                        line=_S.line_no
                    )
                    continue


                # -------------------------------------------------
                # @context
                # -------------------------------------------------

                r = prefix+'-- *@context'+end
                m = re.match(r, line)
                if m:

                    if not self.checkAllowed(
                            feature='context',
                            message=_entityError(
                                'Context blocks', '. Skipped.'),
                            level=Levels.Error):
                        continue


                    if _S.main_block is not None:

                        # TODO: this limitation could be removed. But this
                        # requires some analysis.The problem seems to be
                        # that the order of block could is not enough to
                        # know the order of statement.
                        LocalizedSourceIssue(
                            sourceFile=self,
                            level=Levels.Fatal,
                            message='Context cannot be nested',
                            line=_S.line_no
                        )
                        continue
                    if _S.context_block is None:
                        _S.context_block=ContextBlock(
                            self.scenarioModel,
                            lineNo=_S.line_no,
                        )
                    continue

                # -------------------------------------------------
                # @endcontext
                # -------------------------------------------------

                r = prefix+'-- *@endcontext'+end
                m = re.match(r, line)
                if m:
                    if not self.checkAllowed(
                            feature='context',
                            message=_entityError(
                                'Context blocks', '. Skipped.'),
                            level=Levels.Error):
                        continue
                    if _S.context_block is None:
                        LocalizedSourceIssue(
                            sourceFile=self,
                            level=Levels.Error,
                            message='No context opened. Directive ignored.',
                            line=_S.line_no
                        )
                        continue
                    _S.context_block=None
                    continue

                #--------------------------------------------------
                # @uci <actori> <usecase>
                #--------------------------------------------------
                r = (prefix
                     # +r'-- *@ *(uci|usecase( +instance)?)'
                     +r'-- *@ *uci'
                     +r' +(?P<name>\w+)'
                     # TODO: add online definition of actor instance
                     # +r' *(: *(?P<actor>\w+))?'
                     +r' *(?P<usecase>\w+)'
                     +end)
                m = re.match(r, line)
                if m:
                    if not self.checkAllowed(
                            feature='usecase',
                            message=_entityError(
                                'Actor instance definitions', '. Skipped.'),
                            level=Levels.Error):
                        continue
                    if self.usecaseModel is None:
                        LocalizedSourceIssue(
                            sourceFile=self,
                            level=Levels.Warning,
                            message=
                                'No use case model provided. Directive ignored.',
                            line=_S.line_no
                        )
                        continue
                    if _S.context_block is not None:
                        LocalizedSourceIssue(
                            sourceFile=self,
                            level=Levels.Error,
                            message='Context block is not closed. Assume it is',
                            line=_S.line_no
                        )
                        _S.context_block = None
                    ainame=m.group('name')
                    if ainame not in self.scenarioModel.actorInstanceNamed:
                        LocalizedSourceIssue(
                            sourceFile=self,
                            level=Levels.Fatal,
                            message=( 'Actor instance "%s" is not defined.'
                                      % ainame ),
                            line=_S.line_no
                        )
                    ai=self.scenarioModel.actorInstanceNamed[ainame] #type: ActorInstance
                    a=ai.actor #type: Actor
                    ucname=m.group('usecase')
                    if ucname not in self.scenarioModel.usecaseModel.system.usecaseNamed:
                        LocalizedSourceIssue(
                            sourceFile=self,
                            level=Levels.Fatal,
                            message=( 'Usecase "%s" is not defined.'
                                      % ucname ),
                            line=_S.line_no
                        )
                    uc=self.scenarioModel.usecaseModel.system.usecaseNamed[ucname] #type: Usecase
                    if uc not in a.usecases:
                        LocalizedSourceIssue(
                            sourceFile=self,
                            level=Levels.Error,
                            message=(
                                'Actor %s cannot "%s"' % (
                                    a.name,
                                    uc.name,
                                )),
                            line=_S.line_no
                        )
                    _S.main_block=UsecaseInstanceBlock(
                        model=self.scenarioModel,
                        actorInstance=ai,
                        useCase=uc,
                        lineNo=_S.line_no,
                    )
                    continue

                #--------------------------------------------------
                #-- @enduci
                #--------------------------------------------------

                r = (prefix
                     +r'-- *@enduci'
                     +end)
                m = re.match(r, line)
                if m:
                    if not self.checkAllowed(
                            feature='usecase',
                            message=_entityError(
                                'Usecase instances', '. Skipped.'),
                            level=Levels.Error):
                        continue
                    if self.usecaseModel is None:
                        LocalizedSourceIssue(
                            sourceFile=self,
                            level=Levels.Warning,
                            message=
                                'No use case model provided. Directive ignored.',
                            line=_S.line_no
                        )
                        continue
                    if not isinstance(_S.main_block, UsecaseInstanceBlock):
                        LocalizedSourceIssue(
                            sourceFile=self,
                            level=Levels.Error,
                            message='No opened usecase instance. Directive ignored.',
                            line=_S.line_no
                        )
                    _S.main_block=None
                    continue


                #--------------------------------------------------
                #-- @something ...
                #--------------------------------------------------

                r = (begin+'-- *@(?P<name>[\w]*).*'+end)
                m = re.match(r, line)
                if m:
                    directive=(
                        '' if m.group('name') is None
                        else m.group('name'))
                    LocalizedSourceIssue(
                        sourceFile=self,
                        level=Levels.Warning,
                        message=(
                            'Directive "%s" not recognized. Ignored.'
                            % directive),
                        line=_S.line_no
                    )
                    continue

                # #--------------------------------------------------
                # #---- comments ------------------------------------
                # #--------------------------------------------------
                #
                # r = prefix+'--.*'+end
                # m = re.match(r, line)
                # if m:
                #     continue



            #==================================================
            # ! operations
            #==================================================

            if re.match(begin + r'!', line):

                if not self.checkAllowed(
                        feature='update',
                        lineNo=_S.line_no,
                        message=_entityError(
                            'Update operations', '. Skipped.'),
                        level=Levels.Error):
                    continue

                #--------------------------------------------------
                #--- object creation (old syntax)
                #--- create x : C)
                #--------------------------------------------------

                r = (
                    begin+r'! *'
                    +r'create +(?P<name>\w+)'
                    +r' *: *(?P<className>\w+)'
                    +end)
                m = re.match(r, line)
                if m:
                    variable=m.group('name')
                    classname=m.group('className')
                    self.checkAllowed(
                            feature='createSyntax',
                            lineNo=_S.line_no,

                        message=_entityError('Deprecated syntax'),
                            level=Levels.Warning)
                    id=None
                    if DEBUG:
                        print('sxp: %s := new %s' % (variable,classname))

                    ObjectCreation(
                        block=_get_block(),
                        variableName=variable,
                        class_=_reqClassModel().classNamed[classname],
                        id=id,
                        lineNo=_S.line_no
                    )
                    continue

                #--------------------------------------------------
                #--- object creation (new syntax)
                #  x := new C('lila')
                #--------------------------------------------------

                r = (begin
                     + r'! *(?P<name>\w+) *:= *'
                     +r'new +(?P<className>\w+)'
                     + ' *( *\( *(\'(?P<id>\w+)\')? *\))?'
                     + end)
                m = re.match(r, line)
                if m:
                    variable=m.group('name')
                    classname=m.group('className')
                    id=m.group('id')
                    if DEBUG:
                        print('sxp: %s := new %s : %s' % (variable,id,classname))

                    ObjectCreation(
                        block=_get_block(),
                        variableName=variable,
                        class_=_reqClassModel().classNamed[classname],
                        id=id,
                        lineNo=_S.line_no
                    )
                    continue

                #--------------------------------------------------
                #--- attribute assignement
                #--------------------------------------------------

                r = (begin
                        + r'! *(set )? *(?P<name>\w+) *'
                        + r'\. *(?P<attribute>\w+) *'
                        + r':= *(?P<expr>.*) *'
                        + end )
                m = re.match(r, line)
                if m:
                    variable=m.group('name')
                    attribute=m.group('attribute')
                    expression=m.group('expr')
                    if DEBUG:
                        print ('sxp: %s.%s := %s' % (
                            variable, attribute, expression))
                    AttributeAssignment(
                        block=_get_block(),
                        variableName=variable,
                        attributeName=attribute,
                        expression=expression,
                        lineNo=_S.line_no,
                    )
                    continue

                #--------------------------------------------------
                #--- link creation
                #--------------------------------------------------

                r = (begin
                     + r'! *insert *\((?P<names>[\w, ]+)\) *'
                     + r'into +'
                     + r'(?P<associationName>\w+)'
                     + end )
                m = re.match(r, line)
                if m:
                    if not self.checkAllowed(
                            feature='assocClass',
                            lineNo=_S.line_no,
                            message=_entityError(
                                'Association classes', '. Skipped.'),
                            level=Levels.Error):
                        continue
                    names = [
                        n.strip()
                        for n in m.group('names').split(',')]
                    assoc=_reqClassModel().associationNamed[
                        m.group('associationName')]
                    if DEBUG:
                        print('sxp: new (%s) : %s' % (
                            ','.join(names),
                            assoc.name ))
                    LinkCreation(
                        block=_get_block(),
                        names=names,
                        association=assoc,
                        id=None,
                        lineNo=_S.line_no
                    )
                    continue

                #--------------------------------------------------
                #--- link object creation (old form)
                #--- create r1 : Rent between (a1,b2)
                #--------------------------------------------------
                # ex:
                r = (begin
                     + r'! *create +(?P<name>\w+) *: *'
                     +r'(?P<assocClassName>\w+) +'
                     + r'between +\((?P<names>[\w, ]+)\) *'
                     + end )
                m = re.match(r, line)
                if m:
                    assoc_class_name = m.group('assocClassName')
                    name = m.group('name')
                    names = m.group('objectList').replace(' ','').split(',')
                    ac = _reqClassModel().associationClassNamed[
                        assoc_class_name]
                    self.checkAllowed(
                            feature='createSyntax',
                            lineNo=_S.line_no,

                        message=_entityError(
                                ' Deprecated syntax.'),
                            level=Levels.Warning)
                    if DEBUG:
                        print(('sxp: new %s between (%s)' % (
                            assoc_class_name,
                            ','.join(names))
                        ))
                    LinkObjectCreation(
                        block=_get_block(),
                        variableName=name,
                        names=names,
                        id=None,
                        associationClass=ac,
                        lineNo=_S.line_no
                    )
                    continue

                #--------------------------------------------------
                #--- link object creation (new form)
                #--- v1 := new Rent('lila') between (r1,a2,v3)
                #--------------------------------------------------

                r = (begin
                     + r'! *(?P<name>\w+) *:='
                     + r' *new +(?P<assocClassName>\w+)'
                     + r' *( *\( *(\'(?P<id>\w+)\')? *\))?'
                     + r' *between +\((?P<objectList>[\w, ]+)\) *'
                     + end )
                m = re.match(r, line)
                if m:
                    if not self.checkAllowed(
                            feature='assocClass',
                            message=_entityError(
                                'Association classes', '. Skipped.'),
                            level=Levels.Error):
                        continue
                    assoc_class_name = m.group('assocClassName')
                    name = m.group('name')
                    id = m.group('id')
                    names = m.group('objectList').replace(' ','').split(',')
                    ac = _reqClassModel().associationClassNamed[assoc_class_name]
                    if DEBUG:
                        print(("sxp: new %s('%s') between (%s)" % (
                            assoc_class_name,
                            id,
                            ','.join(names)
                        )))
                    LinkObjectCreation(
                        block=_get_block(),
                        variableName=name,
                        names=names,
                        id=id,
                        associationClass=ac,
                        lineNo=_S.line_no
                    )
                    continue

                #--------------------------------------------------
                #--- object (or link object) destruction
                #--------------------------------------------------

                r = (begin
                     + r'! *destroy +(?P<name>\w+)'+ end )
                m = re.match(r, line)
                if m:
                    if not self.checkAllowed(
                            feature='delete',
                            message=_entityError(
                                'Object deletions', '.  Skipped.'),
                            level=Levels.Error):
                        continue
                    name = m.group('name')
                    if DEBUG:
                        print( 'sxp: delete object %s' % name )
                    ObjectDestruction(
                        block=_get_block(),
                        variableName=name,
                    )
                    # TODO implement deletion with ripple effect
                    LocalizedSourceIssue(
                        sourceFile=self,
                        level=Levels.Fatal,
                        message=(
                            'Object deletion is not implemented so far.'),
                        line=_S.line_no
                    )
                    continue
                    # check if this is an regular object or a link object
                    # if name in self.state.objects:
                    #     del self.state.objects[name]
                    # else:
                    #     del self.state.linkObject[name]
                    # continue

                #--------------------------------------------------
                #--- link destruction
                #--------------------------------------------------

                r = (begin
                     + r'! *delete *\((?P<objectList>[\w, ]+)\)'
                     + r' +from +(?P<associationName>\w+)'
                     + end )
                m = re.match(r, line)
                if m:
                    if not self.checkAllowed(
                            feature='delete',
                            lineNo=_S.line_no,
                            message=_entityError(
                                'Link deletions', '.  Skipped.'),
                            level=Levels.Error):
                        continue
                    object_names = \
                        m.group('objectList').replace(' ', '').split(',')
                    association_name = m.group('associationName')
                    # link_name = '_'.join(object_names)
                    # del self.state.links[link_name]
                    if DEBUG:
                        print( 'sxp: delete link from %s between %s' % (
                            association_name,
                            object_names
                        ))
                    # TODO implement deletion
                    LocalizedSourceIssue(
                        sourceFile=self,
                        level=Levels.Fatal,
                        message=(
                            'Link deletion is not implemented so far.'),
                        line=_S.line_no
                    )
                    continue




            #==========================================================
            #  results of evaluation
            #==========================================================

            if self.evaluateScenario and line.startswith('|||||:'): # sex

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
                        role=_reqClassModel()._findRole(
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
                        actual_card = current_cardinality_info['numberOfObjects']  # type: int

                        CardinalityViolationObject(
                            cardinalityViolation=card_eval,
                            violatingObject=(
                                current_cardinality_info['objectName']
                            ),
                            actualCardinality=(
                                actual_card
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
                    invariant=_reqClassModel()._findInvariant(
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
                        current_query_evaluation.subexpressions=[]
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

            # ------------------------------------------------------
            # ---- check
            # ------------------------------------------------------
            # WARNING: this rule MUST go after the rules thats starts
            # with 'check' something as this one will take precedence!
            r = begin + 'check *(?P<params>( -[avd])*)' + end
            m = re.match(r, line)
            if m:
                if not self.checkAllowed(
                        feature='assocClass',
                        message=_entityError(
                            'Checks', '. Skipped.'),
                        level=Levels.Error):
                    continue
                check = Check(
                    block=_get_block(),
                    verbose='v' in m.group('params'),
                    showFaultyObjects='d' in m.group('params'),
                    all='a' in m.group('params'),
                    lineNo=_S.line_no,
                )
                if self.evaluateScenario:
                    last_check_evaluation = _USEImplementedCheckEvaluation(
                        blockEvaluation=None,
                        op=check)
                continue

            # ------------------------------------------------------
            # ---- USE error type1
            # ------------------------------------------------------
            r = (
                begin
                +r'<(?P<filename>[^>]+)>'
                +r':? *'
                +r'(line *(?P<line>\d+) *:? *(?P<col>\d+))?'
                +r' *:?'
                +r'(?P<msg>.*)'
                +end)
            m = re.match(r, line)
            if m:
                filename=m.group('filename')
                assert filename=='input' # As far as we know
                errline=m.group('line')
                assert errline is None or errline=='1' # As far as we know
                errcol=(
                    int(m.group('col')) if m.group('col') is not None
                    else None)
                LocalizedSourceIssue(
                    sourceFile=self,
                    level=Levels.Error,
                    message=m.group('msg'),
                    line=_S.line_no, # the errline is always1
                    column=errcol
                )
                continue

            # ------------------------------------------------------
            # ---- USE error type2
            # ------------------------------------------------------

            r = begin + 'Error:? *(?P<msg>.*)' + end
            m = re.match(r, line)
            if m:
                LocalizedSourceIssue(
                    sourceFile=self,
                    level=Levels.Error,
                    message=m.group('msg'),
                    line=_S.line_no
                )
                continue

            # ------------------------------------------------------
            #---- Unrecognized line
            # ------------------------------------------------------

            LocalizedSourceIssue(
                sourceFile=self,
                level=Levels.Fatal,
                message=('Cannot parse line #%i.'%_S.line_no),
                line=_S.line_no
            )
            continue



class SexSource(_SexOrSoilSource):
    """
    Source corresponding to a scenario execution with execution
    results. The .soil file merged with the trace of the execution
    of USE .soil file.
    """
    def __init__(
            self,
            originalFileName,
            preprocessor=None,
            allowedFeatures=(
                    'permission',  # not used yet
                    'access',  # not used yet
                    'update',  # not used yet
                    'check',  # not used
                    'assertQuery',
                    'assocClass',
                    'delete',
                    'query',
                    'usecase',
                    'context',
                    'createSyntax',
                    'topLevelBlock')
    ):
        #type: (Text, Optional[Preprocessor], List[Text]) -> None
        """
        The process is the following:

        1.  If a preprocessor is provided first call it on
            the original soil filename and used the file returned
            for the rest of the process. If no preprocessor
            is given the original file is used unprocessed.

        2.  The resulting file is then executed by USE OCL.
            After some merging this leads to a .sex file with
            results of queries and checks computed by USE OCL.

        3.  The sex file is then parsed with the parseToFillModel.
            and the scenario is abstractly executed
            (see ScenarioEvaluation). This allows to get
            the evaluation of operations which result is not
            displayed by USE OCL (update operations).

        All this results with a ScenarioModel which
        has an associated ScenarioEvaluation.
        """



        # initialize the parser but with postponed parsing
        # no preprocessing take places
        super(SexSource, self).__init__(
            evaluateScenario=True,
            originalFileName=originalFileName,
            parsePrefix='^((\d{5}|\|{5}):)?',  #
            allowedFeatures=allowedFeatures
            )

        # TODO: remove this restriction
        # The classModel must exist
        # assert self.classModel is not None
        # assert self.classSource is not None

        # # The classModel must have a source to be parsed by USE
        # assert self.classModel.source is not None
        # # TODO: it would be possible to parse/evaluate
        # # In fact the scn without .use or to generate a source from
        # # the model. Low priority for now.




        try:

            # ---- (1) preprocessing soil file ----------------
            if preprocessor is None:
                preprocessed_soil_filename = originalFileName
            else:
                preprocessed_soil_filename = preprocessor.do(
                    issueOrigin=self,
                    filename=originalFileName)

            # ---- (2) reusing preprocessed use file ----------
            preprocessed_use_filename=Environment.getWorkerFileName(
                basicFileName=replaceExtension(
                    self.classSource.fileName,
                    '.use'))

            # ---- (2) sex generation (execution+merging) -----
            sex_file=self.__generateSexFile(
                soilFileName=preprocessed_soil_filename,
                useFileName=preprocessed_use_filename)
            self.doReadFiles(realFileName=sex_file)

            # ---- (3) parsing sex to model ------------------
            self.parseToFillModel()
            self.finalize()


        except FatalError as e:
            # The fatal error has already registered. Do nothing
            pass

        except Exception as e:
            # Some uncatched exception. Generate an error.
            # Not need to create a fatal one as the process
            # is already stopped.
            Issue(
                origin=self,
                level=Levels.Error,
                message='Exception: %s' % str(e)
            )
            raise #? should it be better do just pass ?
    #
    # def __preprocessOriginalFile(self, preprocessor, originalFileName):
    #     #type: (Callable[[Text, Any], Text], Text) -> Text
    #     if preprocessor is None:
    #         return originalFileName
    #     else:
    #         return preprocessor(originalFileName, self)


    def __generateSexFile(self, soilFileName, useFileName):
        #type: (Text, Text) -> Text
        """
        Execute the UseOCL tool with .use and .soil
        Can raise a FatalError.from modelscribes.base.preprocessors import (
    Preprocessor
)
        Return the filename of the sex file generated
        """

        # # Check that the class model is valid
        # if not classModel.isValid:
        #     raise FatalError(
        #         Issue(
        #             origin=self,
        #             level=Levels.Fatal,
        #             message='Class model is invalid' % self.fileName))
        if DEBUG>=2:
            print((
                'sxp: generating sex file from:\n'
                '    use=%s\n'
                '    soil=%s\n' ) % (
                    useFileName,
                    soilFileName
                    ))

        # Check that the soil file exists
        if not os.path.isfile(soilFileName):
            raise FatalError(
                Issue(
                    origin=self,
                    level=Levels.Fatal,
                    message='File not found: %s' % soilFileName))

        # Check that the use file exists
        if not os.path.isfile(useFileName):
            raise FatalError(
                Issue(
                    origin=self,
                    level=Levels.Fatal,
                    message='File not found: %s' % useFileName))

        # Execute USE OCL to generate the sex file
        try:
            # FIXME:1 must preprocess .cls file first to make it use
            sex_file=USEEngine.executeSoilFileAsSex(
                useFile=useFileName,
                soilFile=soilFileName,
                prequelFileName=self.prequelFileName)

            if DEBUG >= 2:
                print('sxp: sex file generation done (%s)' %
                      sex_file)
                print('       ')
            return sex_file

        except Exception as e:
            m='Error during USE execution: %s' % str(e)
            if DEBUG>=1:
                import traceback
                print('spx: '+'*'*40+'Exception')
                traceback.print_exc()
            Issue(
                origin=self,
                level=Levels.Fatal,
                message=m)


# class SoilSource(_SexOrSoilSource):
#     """
#     Source corresponding directly to the raw .soil source given
#     as the parameter.
#     WARNING: USE is *NOT* executed so some errors may
#     be left undiscovered. Moreover, there is no cardinality check,
#     no invariant checking, etc.
#     From this soil source, one can get an object model.
#     """
#     def __init__(
#             self,
#             soilFileName):
#             # classModel,
#             # usecaseModel=None):
#         #type: (Text, ClassModel) -> None
#         super(SoilSource, self).__init__(
#             evaluateScenario=False,
#             soilFileName=soilFileName,
#             parsePrefix='^',
#             preIssueMessages=[])
#         self.doParse(soilFileName)
#

