# coding=utf-8

# TODO: improve error generation
# TODO: update the module comment as the parser is no longer based on canonical stuff
# TODO: implement role keyword arbitrary (with sequence of words then consumed iteratively)
# TODO: implement indentation based parsing for extra safety
# TODO: add options to the parser (indentationBased?, use parsing?, etc.)


"""
This module allows to analyze a USE OCL ``.use`` source file:


* The file is loaded with ``use`` interpreter.
* Then the ``info model`` command is issued.
* The canonical representation produced is finally parsed.
* A class model that conforms to a simple UML class metamodel is created
* and stored in scenario attribute.
* If errors are detected then errors contains the list of errors.

Either find some errors or create a class model
"""

#import os
import re
from typing import Text, Optional, Callable, Any

from modelscribes.base.symbols import (
    Symbol
)

from modelscribes.base.preprocessors import (
    Preprocessor
)

from modelscribes.base.parsers import DocCommentLines
from modelscribes.megamodels.sources import ModelSourceFile

from modelscribes.megamodels.metamodels import Metamodel
from modelscribes.base.issues import (
    Issue,
    LocalizedSourceIssue,
    Levels,
    FatalError
)
import modelscribes.use.engine
from modelscribes.metamodels.classes import (
    ClassModel,
    SimpleType,
    BasicType,
    Enumeration,
    EnumerationLiteral,
    Class,
    Attribute,
    Operation,
    Association,
    Role,
    AssociationClass,
    METAMODEL
)

from modelscribes.metamodels.classes.expressions import (
    PreCondition,
    PostCondition,
    Invariant
)

__all__ = (
    'UseModelSource'
)


def _removeExtraSpaces(x):
    return ' '.join(x.split())


class UseModelSource(ModelSourceFile):
    """
    Abstraction of ``.use`` source file.
    This source file can be valid or not. In this later case
    a reference to the contained class model will be available.
    """

    def __init__(self,
                 originalFileName,
                 preprocessor=None,
                 allowedFeatures=(
                         'enum',
                         'assocClass',
                         'operation',
                         'inv',
                         'pre/post'),
                 ):
        #type: (Text, Optional[Preprocessor]) -> None
        """
        Execute the given .use file with use interpreter, then
        parse the result (possiblity with errors) and finally
        build and return a UseModelSource.

        If the source is 'use valid', this the UseModelSource contains a
        class model, otherwise it contains the list of errors
        as well as the USE OCL command exit code.

        :param originalFileName:
            The path of the '.use' source file to analyze
        Examples:
            see test.modelscript.test_parser
        """

        #: class model representing the file in a conceptual way
        #: start with an empty class model but will be set to None
        #: in case of Errors

        # noinspection PySuperArguments

        self.commandExitCode = None #type: Optional[int]
        """Exit code of use command"""

        self.isOldUSEFile=originalFileName.endswith('.use')
        # Filled by __executeUSEToExtractErrors

        super(UseModelSource, self).__init__(
            fileName=originalFileName,
            prequelFileName=originalFileName,
            realFileName=None,  # will be set later
            readFileLater=False,
            fillImportBoxLater=False,
            parseFileLater=True,
            noSymbolChecking=self.isOldUSEFile,
            # activate the patch to recognize USE OCL "model <name>"
            allowedFeatures=allowedFeatures,
            recognizeUSEOCLNativeModelDefinition=True)



        try:

            # ---- (1) preprocessing -------------------------------------
            if preprocessor is None:
                use_filename=originalFileName
            else:
                use_filename=preprocessor.do(
                    issueOrigin=self,
                    filename=originalFileName)
            self.doReadFiles(realFileName=use_filename)


            # ---- (3) parsing sex to model ------------------------------
            self.parseToFillModel()
            self.finalize()

        except FatalError as e:
            # The fatal error has already registered. Do nothing
            pass

        except Exception as e:
            # Some uncatched execption. Generate an error.
            # Not need to create a fatal one as the process
            # is already stopped.
            Issue(
                origin=self,
                level=Levels.Error,
                message='Exception: %s' % str(e)
            )
            raise #? should it be better do just pass ?




    #--------------------------------------------------------------------------
    #    Class implementation
    #--------------------------------------------------------------------------

    @classmethod
    def __dir__(cls):
        # return super(UseModelSource, cls).__dir__()
        return ['basename','extension']

    @property
    def classModel(self):
        m=self.model #type: ClassModel
        return m


    @property
    def metamodel(self):
        #type: () -> Metamodel
        return METAMODEL


    def parseToFillModel(self):
        # Try to validate the class model and fill
        #       self.errors,
        #       self.commandExitCode,
        self.__executeUSEToExtractErrors()

        if self.isValid:
            # No errors. Parse the regular .use source file.
            # (There is no comment in the output of use)
            self.__parseLinesAndCreateModel()
            self.__resolveModel()

    def __executeUSEToExtractErrors(self):
        """
        Execute USE to first check if there are syntax errors.
        If they are such errors then fill the .errors[]
        Otherwise read the original .use file.
        Another implementation would be to get the "cannonical
        form" generated by USE but this is not convenient since
        comments are removed.
        """
        engine = modelscribes.use.engine.USEEngine
        try:
            self.commandExitCode = engine.analyzeUSEModel(
                self.realFileName,
                prequelFileName=self.prequelFileName)
        except Exception as e:
            Issue(
                origin=self,
                level=Levels.Fatal,
                message=('Cannot execute "use" tool. %s' % str(e))
            )
        if self.commandExitCode != 0:
            #create errors from the ouput generated by USE
            for line in engine.err.splitlines():
                self.__addErrorFromLine(line)
            #TODO: check this comment
            # Remove 2 lines at the beginning (use intro + command)
            # and two lines at the end (information + quit command)
            # tmp = engine.out.splitlines()[2:-2]
            # self.sourceLines = [line.rstrip() for line in open(self.fileName, 'rU')]

        return self.isValid

    def __addErrorFromLine(self, line):
        #type: (Text) -> None
        """
        Convert a use error line into an LocalizedSourceIssue.

        USE generate errors like:
            testcases/useerrors/bart.use:line 27:26 no viable alternative at input '='
            testcases/useerrors/empty.use:line 1:0 mismatched input '<EOF>' expecting 'model'
            testcases/useerrors/model.use:line 1:5 mismatched input '<EOF>' expecting an identifier
            testcases/useerrors/model.use:2:10: Undefined class `B'.
            testcases/useerrors/card.use:line 4:4 extraneous input 'role' expecting [
            testcases/useerrors/card1.use:4:5: Invalid multiplicity range `1..0'.
            testcases/useerrors/card1.use:8:6: Class `C' cannot be a superclass of itself.
        """
        p = r'^(?P<filename>.*)' \
            r'(:|:line | line )(?P<line>\d+):(?P<column>\d+)(:)?' \
            r'(?P<message>.+)$'
        try:
            m = re.match(p, line)
            if m:
                # sometimes the regexp fail.
                # e.g. with "ERROR oct. 11, 2015 3:57:00 PM java.util.pref ..."
                LocalizedSourceIssue(
                    sourceFile=self,
                    level=Levels.Error,
                    message=m.group('message'),
                    line=int(m.group('line')),
                    column=int(m.group('column')),
                    fileName=m.group('filename') # FIXME if needed (note ???)
                    )
                return
        except FatalError:
            pass
        Issue(
            origin=self,
            level=Levels.Error,
            message='USE: %s' % line)



    def __parseLinesAndCreateModel(self):


        def _entityError(e, suffix=''):
            return '%s are not allowed%s' % (e, suffix)


        in_block_comment = False
        is_in_doc_comment = False
        last_doc_comment = DocCommentLines()
        current_eol_comment = None
        current_element=self.classModel
        current_enumeration = None
        current_class = None
        current_attribute = None    # could be also in association class
        current_operation = None    # could be also in association class
        current_association = None  # could be also association class
        current_context = None      # Context of an inv|pre|post. None or Dict
                                    #   'variables' : Optional[List[str]]
                                    #   'classname': str
                                    #   'signature': Optional[str]
        current_condition = None    # invariant, precondition or condition
        current_operation_condition = None

        for (line_index,line) in enumerate(self.realSourceLines):

            original_line = line
            line = line.replace('\t',' ')
            line_no = line_index+1




            #--------------------------------------------------
            # Annotation lines
            #--------------------------------------------------
            r = r' *@(Test|Monitor).*$'
            m = re.match(r, line)
            if m:
                # these lines can be ignored
                last_doc_comment.clean()
                continue

            #--------------------------------------------------
            # Single and multi line /* */
            #--------------------------------------------------

            # replace inline /* */ by spaces
            line = re.sub(r'(/\*.*?\*/)',' ',line)

            # deal with /* comments
            r = r'^ */\*.*$'
            m = re.match(r, line)
            if m:
                in_block_comment = True
                last_doc_comment.clean()
                continue

            if in_block_comment:
                r = r'^.*\*/(?P<rest>.*)$'
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

            r = r'^\s*$'
            m = re.match(r, line)
            if m:
                last_doc_comment.clean()
                continue

            #--------------------------------------------------
            # Description
            #--------------------------------------------------

            r = '^ *--\|(?P<line>.*)$'
            m = re.match(r, line)
            if m:
                _line=m.group('line')
                print('OO'*10, _line, type(current_element))
                if current_element is not None:
                    current_element.description.addNewLine(
                        stringLine=_line,
                        lineNo=line_no,
                    )
                continue

            #--------------------------------------------------
            # Line comment --
            #--------------------------------------------------


            #TODO: add here support for processing @ commands

            # Full line comment
            # r = r'^ *--(?P<comment> *([^@].*)?)$'  <--- without @
            r = r'^ *--(?P<comment>.*)$'
            m = re.match(r, line)
            if m:
                c=m.group('comment')
                last_doc_comment.add(c)
                continue

            # Everything that follow is not part of a full line comment
            is_in_doc_comment = False



            # End of line (EOL comment)
            # r = r'^(?P<content>.*?)--(?P<comment> *([^@].*)?)$'  iwthout @
            r = r'^(?P<content>.*?)--(?P<comment>.*)$'
            m = re.match(r, line)
            if m:
                # There is a eol comment on this line
                # all following cases can use this variable
                current_eol_comment = m.group('comment')
                # we go though the next cases without the eol
                line=m.group('content')
            else:
                current_eol_comment = None

            #--------------------------------------------------
            # Blocks : TODO: check this
            #--------------------------------------------------

            # # TODO: check if this is safe
            # r = r'^( '\
            #     r'| *begin' \
            #     r'| +end' \
            #     r'| *between' \
            #     r')$'
            # m = re.match(r, line)
            # if m:
            #     # these lines can be ignored
            #     continue


            r = r'^ *constraints *$'
            m = re.match(r, line)
            if m:
                last_doc_comment.clean()
                current_enumeration = None
                current_attribute = None
                current_operation = None
                current_condition = None
                current_operation_condition = None
                current_element = None
                continue

            r = r'^ *attributes *$'
            m = re.match(r, line)
            if m:
                last_doc_comment.clean()
                current_enumeration = None
                current_attribute = None
                current_operation = None
                current_condition = None
                current_operation_condition = None
                current_element = None
                continue

            r = r'^ *between *$'
            m = re.match(r, line)
            if m:
                last_doc_comment.clean()
                current_enumeration = None
                current_element = None
                continue

            r = r'^ *operations *$'
            m = re.match(r, line)
            if m:
                last_doc_comment.clean()
                current_enumeration = None
                current_attribute = None
                current_operation = None
                current_condition = None
                current_operation_condition = None
                current_element = None
                continue

            #--------------------------------------------------
            # model --
            #--------------------------------------------------

            r = r'^ *model (?P<name>\w+) *$'
            m = re.match(r, line)
            if m:
                c=self.classModel
                c.name=m.group('name')
                c.code=self.realSourceLines
                c.lineNo = line_no
                c.docComment = last_doc_comment.consume()
                c.eolComment = current_eol_comment
                continue


            #--------------------------------------------------
            # enumeration --
            #--------------------------------------------------

            #---- first line of enumeration (may be one line only) ---
            r = r'^ *enum +(?P<name>\w+) *{' \
                r' *(?P<literals>[\w+, ]*)' \
                r' *(?P<end>})? *;?' \
                r' *$'
            m = re.match(r, line)
            if m:
                if not self.checkAllowed(
                        feature='enum',
                        lineNo=line_no,
                        message=_entityError(
                            ' Enumerations'),
                        level=Levels.Fatal):
                    continue
                current_context = None
                current_association = None
                current_class = None
                current_attribute = None
                current_operation = None
                literal_values=[ l
                    for l in m.group('literals').replace(' ','').split(',')
                    if l != ''
                ]

                if not self.isOldUSEFile and not Symbol.is_CamlCase(m.group('name')):
                    LocalizedSourceIssue(
                        sourceFile=self,
                        level=Levels.Warning,
                        message=(
                            '"%s" should start with an uppercase.'
                            % m.group('name')),
                        line=line_no
                    ) # TODO: add column
                enumeration = Enumeration(
                    name=m.group('name'),
                    model=self.classModel,
                    code=line,
                    lineNo=line_no,
                    docComment=last_doc_comment.consume(),
                    eolComment=current_eol_comment,
                )
                for literal_value in literal_values:
                    EnumerationLiteral(
                        name=literal_value,
                        enumeration=enumeration,
                        lineNo=line_no
                    )

                self.classModel.enumerationNamed[m.group('name')] = enumeration

                if m.group('end'):
                    current_enumeration = None
                    current_element=None
                else:
                    current_enumeration = enumeration
                    current_element=enumeration
                continue

            #---- enumeration literals, may be with end ------------
            if current_enumeration is not None:
                r = r'^ *(?P<literals>[\w, ]*)?' \
                    r' *(?P<end>})? *;?' \
                    r' *$'
                current_context = None
                current_association = None
                current_class = None
                current_attribute = None
                current_operation = None
                m = re.match(r, line)
                if m:
                    if m.group('literals') is not None:
                        literal_values = [l
                                    for l in m.group('literals').replace(' ', '').split(',')
                                    if l != ''
                                    ]
                        for literal_value in literal_values:
                            # if not self.isOldUSEFile and not Symbol.is_camlCase(literal_value):
                            #     LocalizedSourceIssue(
                            #         sourceFile=self,
                            #         level=Levels.Warning,
                            #         message=(
                            #             '"%s" should start with an lowercase.'
                            #             % literal_value),
                            #         line=line_no
                            #     )  # TODO: add column
                            EnumerationLiteral(
                                name=literal_value,
                                enumeration=current_enumeration,
                                lineNo=line_no
                            )
                            current_element=literal_value
                    if m.group('end'):
                        current_enumeration = None
                        current_element=None
                    continue

            #---- class --------------------------------------------------
            r = r'^ *((?P<abstract>abstract) +)?class +(?P<name>\w+)' \
                r'( *< *(?P<superclasses>(\w+| *, *)+))? *(?P<end> end)?' \
                r' *$'
            m = re.match(r, line)
            if m:
                current_enumeration = None
                current_association = None
                current_attribute = None
                current_operation = None
                # parse superclasses series
                if m.group('superclasses') is None:
                    superclasses = ()
                else:
                    superclasses = [c.strip() for c in m.group('superclasses').split(',')]
                if not self.isOldUSEFile and  not Symbol.is_CamlCase(m.group('name')):
                    LocalizedSourceIssue(
                        sourceFile=self,
                        level=Levels.Warning,
                        message=(
                            '"%s" should start with an uppercase.'
                            % m.group('name')),
                        line=line_no
                    ) # TODO: add column
                current_class = Class(
                        name=m.group('name'),
                        model=self.classModel,
                        isAbstract=m.group('abstract') == 'abstract',
                        superclasses=superclasses,
                        lineNo=line_no,
                        docComment=last_doc_comment.consume(),
                        eolComment=current_eol_comment,
                    )
                current_element=current_class
                if m.group('end') is not None:
                    current_class = None
                    current_element = None
                else:
                    current_context = {
                        'variables': None,
                        'classname': m.group('name'),
                        'signature': None,
                    }
                continue

            #---- associationclass ---------------------------------------
            r = r'^ *((?P<abstract>abstract) +)?associationclass +(?P<name>\w+)' \
                r'( *< *(?P<superclasses>(\w+| *, *)+))?' \
                r'( +(between)? *)?' \
                r' *$'
            m = re.match(r, line)
            if m:
                if not self.checkAllowed(
                        feature='assocClass',
                        lineNo=line_no,
                        message=_entityError(
                            'Association classes'),
                        level=Levels.Fatal):
                    continue
                current_context = None
                current_enumeration = None
                current_attribute = None
                current_operation = None
                # parse superclasses series
                if m.group('superclasses') is None:
                    superclasses = ()
                else:
                    superclasses = [c.strip() for c in m.group('superclasses').split(',')]
                    # print(superclasses)
                if not self.isOldUSEFile and not Symbol.is_CamlCase(m.group('name')):
                    LocalizedSourceIssue(
                        sourceFile=self,
                        level=Levels.Warning,
                        message=(
                            '"%s" should start with an uppercase.'
                            % m.group('name')),
                        line=line_no
                    ) # TODO: add column
                ac = AssociationClass(
                        name=m.group('name'),
                        model=self.classModel,
                        isAbstract=m.group('abstract') == 'abstract',
                        superclasses=superclasses,
                        lineNo=line_no,
                        docComment=last_doc_comment.consume(),
                        eolComment=current_eol_comment,
                    )
                current_class = ac
                current_association = ac
                current_element=ac
                continue

            #---- attribute ----------------------------------------------
            # Set(String) is allowed. See test CarRental2
            # Tuple( x : Tuple(x : Integer), y : Tuple(y : Integer)) : See test 030
            r = r'^ *(?P<name>\w+)' \
                r' *: *(?P<type>\w+[(),:\w+ ]*)' \
                r' *((?P<keyword>derive|init) *[=:](?P<expression>.*))?' \
                r' *;?' \
                r' *$'
            m = re.match(r, line)
            if m:
                current_enumeration = None
                current_operation = None
                if current_class is not None:
                    current_enumeration = None
                    current_operation = None
                    is_derived = m.group('keyword') == 'derive'
                    is_init = m.group('keyword') == 'init'
                    expression = m.group('expression')
                    if not self.isOldUSEFile and not Symbol.is_camlCase(m.group('name')):
                        LocalizedSourceIssue(
                            sourceFile=self,
                            level=Levels.Warning,
                            message=(
                                '"%s" should start with an lowercase.'
                                % m.group('name')),
                            line=line_no
                        )  # TODO: add column
                    # This could be in an association class
                    attribute = Attribute(
                        name=m.group('name'),
                        class_=current_class,
                        code=line,
                        type=m.group('type').replace(' ',''),
                        isDerived=is_derived,
                        isInit=is_init,
                        expression=expression,
                        lineNo=line_no,
                        docComment=last_doc_comment.consume(),
                        eolComment=current_eol_comment,
                    )
                    current_attribute = attribute
                    current_element=attribute
                    continue

            #---- operation ----------------------------------------------
            r = r'^ *(?P<name>\w+)' \
                r' *\((?P<parameters>[\w ,:\(\)]*)\)' \
                r'( *: *(?P<type>[\w,\(\) ]+))?' \
                r'( *=(?P<expr>.*))?' \
                r' *$'
            m = re.match(r, line)
            if m and '(' in line and ')' in line:
                if current_class is not None:
                    if not self.checkAllowed(
                            feature='operation',
                            lineNo=line_no,
                            message=_entityError(
                                'Operations'),
                            level=Levels.Fatal):
                        continue
                    current_enumeration = None
                    current_attribute = None
                    current_condition = None

                    # This could be an association class
                    parameters = m.group('parameters').replace(' ','')
                    result = '' if m.group('type') is None else m.group('type').replace(' ','')
                    resultstr = '' if result == '' else ':'+result
                    signature = '%s(%s)%s' % (
                        # current_class.name,
                        m.group('name'),
                        parameters,
                        resultstr
                    )
                    signature = signature.replace(' ','')
                    expr=m.group('expr')
                    if not self.isOldUSEFile and not Symbol.is_camlCase(m.group('name')):
                        LocalizedSourceIssue(
                            sourceFile=self,
                            level=Levels.Warning,
                            message=(
                                '"%s" should start with an lowercase.'
                                % m.group('name')),
                            line=line_no
                        )  # TODO: add column
                    operation = Operation(
                            name=m.group('name'),
                            class_=current_class,
                            code=line,
                            signature=signature,
                            expression=expr,
                            lineNo=line_no,
                            docComment=last_doc_comment.consume(),
                            eolComment=current_eol_comment,
                        )
                    current_operation = operation
                    current_context = {
                        'variables': None,
                        'classname': current_class.name,
                        'signature': signature,
                    }
                    current_element=operation
                    continue



            #---- association --------------------------------------------
            r = r'^ *(?P<kind>association|composition|aggregation) *' \
                r'(?P<name>\w+) *(between)?' \
                r' *$'
            m = re.match(r, line)
            if m:
                current_enumeration = None
                current_class = None
                current_attribute = None
                current_operation = None
                current_context = None
                if not self.isOldUSEFile and not Symbol.is_CamlCase(m.group('name')):
                    LocalizedSourceIssue(
                        sourceFile=self,
                        level=Levels.Warning,
                        message=(
                            '"%s" should start with an uppercase.'
                            % m.group('name')),
                        line=line_no
                    )  # TODO: add column
                current_association = Association(
                        name=m.group('name'),
                        model=self.classModel,
                        kind=m.group('kind'),
                        lineNo=line_no,
                        docComment=last_doc_comment.consume(),
                        eolComment=current_eol_comment,
                    )
                current_element=current_association
                continue

            r = r'^ *(?P<type>\w+) *\[(?P<cardinality>[^\]]+)\]' \
                r' *(role +(?P<name>\w+))?' \
                r' *( +qualifier *\( *(?P<qualifiers>(\w| |:|,)*) *\))?' \
                r' *(?P<subsets>( +subsets +\w+)*)' \
                r' *( +(?P<union>union))?' \
                r' *( +(?P<ordered>ordered))?' \
                r' *( +(derived *= *(?P<expression>.*)))? *;?'\
                r' *?$'
            #---- role ---------------------------------------------------
            # rtypcard=r'(?P<type>\w+) *\[(?P<cardinality>[^\]]+)\]'
            # rname=r'role +(?P<name>\w+)'
            # rqualifier=r'qualifier *\( *(?P<qualifiers>(\w| |:|,)*) *\)'
            # r =
            #     r'(?P<subsets>( +subsets +\w+)*)' \
            #     r' *( +(?P<union>union))?' \
            #     r' *( +(?P<ordered>ordered))?' \
            #     r' *( +(derived *= *(?P<expression>.*)))? *;?'\
            #     r' *?$'
            # r=' *%(rtypcard)s *(%(rname)s)?( *(%(rqualifier)s|))*' % {
            #     'rtypcard': rtypcard,
            #     'rname': rname,
            #     'rqualifier':rqualifier,

            m = re.match(r, line)
            if m:
                if current_association is not None:
                    current_enumeration = None
                    current_attribute = None
                    current_operation = None
                    # This could be an association class
                    # Parse the cardinality string
                    c = m.group('cardinality').replace(' ','').split('..')
                    if c[0] == '*':
                        min = 0
                        max = None
                    elif len(c) == 1:
                        min = int(c[0])
                        max = min
                    else:
                        min = int(c[0])
                        max = None if c[1] == '*' else int(c[1])
                    # Parse the 'subsets' series
                    if m.group('subsets') == '':
                        subsets = None
                    else:
                        subsets = _removeExtraSpaces(m.group('subsets')).split('subsets ')[1:]
                    # Parse the 'qualifiers' series
                    if m.group('qualifiers') is None:
                        qualifiers = None
                    else:
                        qualifiers = \
                            [tuple(q.split(':'))
                             for q in m.group('qualifiers').replace(' ','').split(',')]
                    role_name=m.group('name')
                    if role_name is None or role_name=='':
                        # Create an issue although the parser
                        # will use the name of the class by default
                        LocalizedSourceIssue(
                            sourceFile=self,
                            level=Levels.Warning,
                            message=(
                                'The name of the role is not defined.'),
                            line=line_no
                        )  # TODO: add column
                    elif not self.isOldUSEFile and not Symbol.is_camlCase(role_name):
                        LocalizedSourceIssue(
                            sourceFile=self,
                            level=Levels.Warning,
                            message=(
                                '"%s" should start with a lowercase.'
                                % role_name),
                            line=line_no
                        )  # TODO: add column

                    role=Role(
                        name=m.group('name'), # could be None, but will get default
                        association=current_association,
                        type=m.group('type'),
                        cardMin=min,
                        cardMax=max,
                        isOrdered=m.group('ordered') == 'ordered',
                        qualifiers=qualifiers,
                        subsets=subsets,
                        isUnion=m.group('union') == 'union',
                        expression=m.group('expression'),
                        lineNo=line_no,
                        docComment=last_doc_comment.consume(),
                        eolComment=current_eol_comment,
                    )
                    current_element=role
                    continue

            rcontext=(
                r' *(?P<context>context)'
                r' +((?P<vars>[\w ,]+) *:)?'
                r' *(?P<classname>\w+)'
                r' *(::(?P<signature>\w+\([\w, \(\):]*\) *(:([\w ,\(\):]+))?))?'
            )
            rcond=(
                r' *(?P<existential>existential)?'
                r' *(?P<cond>pre|post|inv)'
                r' *(?P<name>\w+)?'
                r' *:'
                r'(?P<expr>.*)'
            )
            z='^(%s)?(%s)? *$' % (rcontext,rcond)
            r=re.compile(z)
            m = re.match(r, line)
            if m:
                if m.group('context') is not None or m.group('cond') is not None:

                    if m.group('context'):
                        # The context is specified => this is a top level condition
                        current_enumeration = None
                        current_class = None
                        current_association = None
                        current_attribute = None
                        current_operation = None
                        variables = None if m.group('vars') is None \
                            else m.group('vars').replace(' ','').split(',')
                        classname = m.group('classname')
                        signature=None if m.group('signature') is None \
                            else m.group('signature').replace(' ','')
                        current_context = {
                            'variables': variables,
                            'classname': classname,
                            'signature': signature,
                        }

                    if m.group('cond'):

                        condname = '' if m.group('name') is None else m.group('name')
                        if m.group('cond') == 'inv':
                            # An invariant can have no context at all. Deal with it.
                            if not self.checkAllowed(
                                    feature='inv',
                                    lineNo=line_no,
                                    message=_entityError(
                                        'Invariants', '.  Skipped.'),
                                    level=Levels.Fatal):
                                continue
                            if current_context is None:
                                classname = None
                                variables = None
                            else:
                                classname = current_context['classname']
                                variables = current_context['variables']
                            variable = None if variables is None else variables[0]
                            additionalVariables = \
                                None if variables is None or len(variables) < 2 \
                                else variables[1:]
                            current_condition = Invariant(
                                name=condname,
                                model=self.classModel,
                                class_=classname,
                                variable=variable,
                                additionalVariables=additionalVariables,
                                isExistential=m.group('existential') == 'existential',
                                expression=m.group('expr'),
                                lineNo=line_no,
                                docComment=last_doc_comment.consume(),
                                eolComment=current_eol_comment,
                            )
                            current_element = current_condition
                        elif m.group('cond') == 'pre':
                            if not self.checkAllowed(
                                    feature='pre/post',
                                    lineNo=line_no,
                                    message=_entityError(
                                        'Preconditions', '.  Skipped.'),
                                    level=Levels.Fatal):
                                continue
                            classname = current_context['classname']
                            current_condition = PreCondition(
                                name=condname,
                                model=self.classModel,
                                class_=classname,
                                operation=current_context['signature'],
                                expression=m.group('expr'),
                                lineNo=line_no,
                                docComment=last_doc_comment.consume(),
                                eolComment=current_eol_comment,
                            )
                            current_element = current_condition
                        elif m.group('cond') == 'post':
                            if not self.checkAllowed(
                                    feature='pre/post',
                                    lineNo=line_no,
                                    message=_entityError(
                                        'Postconditions', '.  Skipped.'),
                                    level=Levels.Fatal):
                                continue
                            classname = current_context['classname']
                            current_condition = PostCondition(
                                name=condname,
                                model=self.classModel,
                                class_=classname,
                                operation=current_context['signature'],
                                expression=m.group('expr'),
                                lineNo=line_no,
                                docComment=last_doc_comment.consume(),
                                eolComment=current_eol_comment,
                            )
                            current_element = current_condition
                    continue


            #===========================================================
            #  Continuation stuff
            #===========================================================

            # From here and below only lines that are nested inside
            # entities, so don't use comments if not used before
            last_doc_comment.clean()

            # ---- condition body -----
            # must be before the operation
            if current_condition is not None:
                r = r'^ *(?P<expression>.*) *$'
                m = re.match(r, line)
                if m:
                    expression=m.group('expression')
                    if expression != 'end' or 'begin' in current_condition.expression:
                        current_condition.expression += '\n' + expression
                    continue

            # ---- attribute expression -----------------------------------
            if current_attribute is not None:
                r = r'^( *(?P<keyword>derive|init)? *[=:])?(?P<expression>.*)' \
                    r' *$'
                m = re.match(r, line)
                if m:
                    is_derived = m.group('keyword') == 'derive'
                    is_init = m.group('keyword') == 'init'
                    expression = m.group('expression')
                    if is_derived:
                        current_attribute.isDerived = True
                    elif is_init:
                        current_attribute.isInit = True
                    if expression is not None:
                        if current_attribute.expression is None:
                            current_attribute.expression = expression
                        else:
                            current_attribute.expression += '\n'+expression
                    continue

            # ---- operation expression -----------------------------------
            if current_operation is not None:
                r = r'^ *(?P<expression>.*)' \
                    r' *$'
                m = re.match(r, line)
                if m:
                    expression = m.group('expression')
                    if expression is not None:
                        if current_operation.expression is None:
                            if expression != 'end':
                                current_operation.expression = expression
                        else:
                            if expression != 'end' or 'begin' in current_operation.expression:
                                current_operation.expression += '\n'+expression
                    continue


            #---- end of association, class, invariant or operation ------
            # TODO: check if this is safe. Not sure as this could be
            # some nested begin end in an operation
            r = r'^(end *)' \
                r' *$'  # match empty line as well
            m = re.match(r, line)
            if m:
                current_class = None
                current_attribute = None
                current_operation = None
                current_association = None
                current_condition = None
                current_element = None
                continue

            #---- a line has not been processed.
            LocalizedSourceIssue(
                sourceFile=self,
                level=Levels.Fatal,
                message=('Cannot process "%s"' % line),
                line=line_no
            )



    def __resolveModel(self):

        def __resolveSimpleType(name):
            #type: (Text)-> SimpleType
            """
            Search the name in enumeration of basic type
            or create a new BasicType.
            """
            if name in self.classModel.simpleTypeNamed:
                return self.classModel.simpleTypeNamed[name]
            else:
                self.classModel.basicTypeNamed[name] = \
                    BasicType(self.model, name)
                return self.classModel.basicTypeNamed[name]

        def __resolveClassType(name):
            """
            Search in class names or association class names.
            The name must exist (no problem because of USE execution)
            """
            if name in self.classModel.classNamed:
                return self.classModel.classNamed[name]
            else:
                return self.classModel.associationClassNamed[name]


        def __resolveAttribute(attribute):
            #type: (Attribute) -> None
            # Resolve the attribute type
            attribute.type = __resolveSimpleType(attribute.type)

        def __resolveOperation(operation):
            if operation.expression is None:
                return
            # remove extra space and blank line
            operation.expression = (
                '\n'.join([
                    ' '.join(l.split())
                    for l in operation.expression.split('\n')
                    if ' '.join(l.split()) != ''])
            )
            if operation.expression == '':
                operation.expression = None

        def __resolveClass(class_):
            # resolve superclasses
            class_.superclasses = \
                [__resolveClassType(name) for name in class_.superclasses]
            # resolve class attributes
            for a in class_.attributes:
                __resolveAttribute(a)
            # resolve class operations
            for op in class_.operations:
                __resolveOperation(op)

        def __resolveSubsets(role):
            # TODO: implement subsets role search
            raise NotImplementedError('subset resolution not implemented')

        def __resolveRole(role):
            # resolve role type
            role.type = __resolveClassType(role.type)
            # resolve qualifier types
            if role.qualifiers is not None:
                qs = role.qualifiers
                role.qualifiers = []
                for (n, t) in qs:
                    role.qualifiers.append((n, __resolveSimpleType(t)))
            if role.subsets is not None:
                for s in role.subsets:
                    pass  # TODO _resolveSubset(role)
            # if role.association.isBinary:
            #     rs = role.association.roles
            #     role.opposite = rs[1] if role is rs[0] else rs[0]

        def __resolveAssociation(association):
            for role in association.roles:
                __resolveRole(role)
            # resolve outgoing and incoming roles for class
            # this must be done after role resolutions
            for role in association.roles:
                target_class = role.type
                target_class.incomingRoles.append(role)
                for opprole in role.opposites:
                    target_class.outgoingRoles.append(opprole)


        def __resolveCondition(condition):

            def nextAnonymousId(ids, prefix):
                anonymous_ids = [
                    int(id[len(prefix):]) for id in ids
                    if re.match('^'+prefix+'[0-9]+$', id)
                ]
                if anonymous_ids:
                    return prefix+str(max(anonymous_ids)+1)
                else:
                    return prefix+'1'

            def computeId(name, dict, prefix):
                # deal with anonymous condition. (inv: pre: or post:)
                if name == '':
                    return nextAnonymousId(dict.keys(), prefix)
                else:
                    return name


            if condition.class_ is None:
                pass  # TODO: check if we should do something for toplevel invariant
            else:
                c = __resolveClassType(condition.class_)
                condition.class_=c
                condition.expression=condition.expression.strip()
                # print 'resolve '+condition.name+' from '+c.name
                # print '        '+str(type(c))
                if isinstance(condition, Invariant):
                    # Store the invariant in the class
                    id = computeId(condition.name, c.invariantNamed, '_inv')
                    c.invariantNamed[id] = condition
                elif isinstance(condition, PreCondition):
                    # print '        ' + str(condition.operation)
                    signature=condition.operation
                    op=c.operationWithSignature[signature]
                    id = computeId(condition.name, op.conditionNamed, '_pre')
                    op.conditionNamed[id]=condition
                elif isinstance(condition, PostCondition):
                    # print '        ' + str(condition.operation)

                    signature=condition.operation
                    op=c.operationWithSignature[signature]
                    id = computeId(condition.name, op.conditionNamed, '_post')
                    op.conditionNamed[id]=condition

        # def __resolveOperationCondition(preOrPost):
        #     if preOrPost.class_ is None:
        #         pass  # TODO: check if we should do something for toplevel invariant
        #     else:
        #         c = __resolveClassType(preOrPost.class_)
        #         preOrPost.expression = (
        #             '\n'.join([
        #                 ' '.join(l.split())
        #                 for l in preOrPost.expression.split('\n')
        #                 if ' '.join(l.split()) != ''])
        #         )
        #         c.invariantNamed[preOrPost.name] = preOrPost

        # resolve class (and class part of class associations)


        cs = self.classModel.classes \
             + self.classModel.associationClasses
        for c in cs:
            __resolveClass(c)

        # resolve association (and association part of class association)
        as_ = self.classModel.associations \
              + self.classModel.associationClasses
        for a in as_:
            __resolveAssociation(a)

        # resolve invariant
        for i in self.classModel._conditions:
            __resolveCondition(i)


    def __preprocessOriginalFile(self, preprocessor, originalFileName):
        #type: (Callable[[Text, Any], Text], Text) -> Text
        if preprocessor is None:
            return originalFileName
        else:
            return preprocessor(originalFileName, self)