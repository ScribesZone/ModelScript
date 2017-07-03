# coding=utf-8

# TODO: update the module comment as the parser is no longer based on canonical stuff
# TODO: implement role keyword arbitrary (with sequence of words then consumed iteratively)
# TODO: implement indentation based parsing for extra saftety
# TODO: add options to the parser (indentationBased?, use parsing?, etc.)

"""
This module allows to analyze a USE OCL ``.use`` source file:


* The file is loaded with ``use`` interpreter.
* Then the ``info model`` command is issued.
* The canonical representation produced is finally parsed.
* An model that conforms to a simple UML metamodel is created
* and stored in model attribute.
* If errors are detected then errors contains the list of errors.

Either find some errors or create a model (see :class:`pyuseocl.model.Model`)
"""

import os
import re

import pyuseocl.utils.errors
import pyuseocl.utils.sources
import pyuseocl.useengine
import pyuseocl.model
from pyuseocl.model import Invariant, PreCondition, PostCondition
# , \
#    Operation, Invariant, Association, Role, AssociationClass, \
#    PreCondition, PostCondition, BasicType

def removeExtraSpaces(x):
    return ' '.join(x.split())

class UseOCLModelFile(pyuseocl.utils.sources.SourceFile):
    """
    Abstraction of ``.use`` source file.
    This source file can be valid or not. In this later case
    a reference to the contained model will be available.
    """

    def __init__(self, useModelSourceFile):
        """
        Analyze the given source file and returns a UseOCLModelFile.
        If valid, this object contains a model, otherwise it contains the
        list of errors as well as the USE OCL command exit code.

        :param useModelSourceFile: The path of the '.use' source file to analyze
        :type useModelSourceFile: str

        Examples:
            see test.pyuseocl.test_analyzer
        """
        super(UseOCLModelFile, self).__init__(useModelSourceFile)

        #: (bool) Indicates if the model file is valid, that is
        #: can be successfully parsed and compiled with use.
        self.isValid = None         # Don't know yet
        self.lines = None  # Nothing yet
        self.length = 0    # Nothing yet

        #: (list[Error]) list of errors if any or empty list.
        self.errors = []            # No errors yet

        #: (int) exit code of use command.
        self.commandExitCode = None # Nothing yet

        #: (Model) Model representing the file in a conceptual way
        #: or None if self.isValid is false
        self.model = None  # Nothing yet, created by parse/resolve

        # Try to validate the model and fill
        #       self.isValid
        #       self.errors,
        #       self.commandExitCode,
        #       self.lines,
        #       self.length
        self.__createCanonicalForm()
        if self.isValid:
            # Create the model by parsing the canonical form
            # fill  self.model,
            self.__parseLinesAndCreateModel()
            self.__resolveModel()

    def saveCanonicalModelFile(self, fileName=None):
        """
        Save the model in the canonical form (returned by "info model")
        in a given file.

        Args:
            fileName (str|NoneType): The output file name or None.
                If no file name is provided then the name of the source
                is taken but the extension will be '.can.use' instead
                of '.use'

        Returns:
            str: the name of the file generated.

        """
        if fileName is None:
            fileName = os.path.splitext(self.fileName)[0] + '.can.use'
        f = open(fileName, 'w')
        f.write('\n'.join(self.canonicalLines))
        f.close()
        return fileName



    def printStatus(self):
        """
        Print the status of the file:

        * the list of errors if the file is invalid,
        * a short summary of entities (classes, attributes, etc.) otherwise
        """

        if self.isValid:
            print self.model
        else:
            print '%s error(s) in the model'  % len(self.errors)
            for e in self.errors:
                print e

    #--------------------------------------------------------------------------
    #    Class implementation
    #--------------------------------------------------------------------------

    def __createCanonicalForm(self):
        engine = pyuseocl.useengine.USEEngine
        self.commandExitCode = engine.analyzeUSEModel(self.fileName)
        if self.commandExitCode != 0:
            self.isValid = False
            self.errors = []
            for line in engine.err.splitlines():
                self.__addErrorFromLine(line)
        else:
            self.isValid = True
            self.errors = []
            # Remove 2 lines at the beginning (use intro + command)
            # and two lines at the end (information + quit command)
            # tmp = engine.out.splitlines()[2:-2]
            self.lines = [line.rstrip() for line in open(self.fileName, 'rU')]

            self.length = len(self.lines)
        return self.isValid

    def __addErrorFromLine(self, line):
        # testcases/useerrors/bart.use:line 27:26 no viable alternative at input '='
        # testcases/useerrors/empty.use:line 1:0 mismatched input '<EOF>' expecting 'model'
        # testcases/useerrors/model.use:line 1:5 mismatched input '<EOF>' expecting an identifier
        # testcases/useerrors/model.use:2:10: Undefined class `B'.
        # testcases/useerrors/card.use:line 4:4 extraneous input 'role' expecting [
        # testcases/useerrors/card1.use:4:5: Invalid multiplicity range `1..0'.
        # testcases/useerrors/card1.use:8:6: Class `C' cannot be a superclass of itself.
        p = r'^(?P<filename>.*)' \
            r'(:|:line | line )(?P<line>\d+):(?P<column>\d+)(:)?' \
            r'(?P<message>.+)$'
        m = re.match(p, line)
        if m:
            try:
                # sometimes the regexp fail.
                # e.g. with "ERROR oct. 11, 2015 3:57:00 PM java.util.pref ..."
                pyuseocl.utils.errors.LocalizedError(
                    sourceFile=self,
                    message=m.group('message'),
                    line=int(m.group('line')),
                    column=int(m.group('column')),
                    fileName=m.group('filename')   # FIXME if needed
                )
            except:
                pyuseocl.utils.errors.SourceError(self, line)
        else:
            pyuseocl.utils.errors.SourceError(self, line)


    def __parseLinesAndCreateModel(self):

        class DocCommentState(object):
            def __init__(self):
                self.lines = None

            def add(self, line):
                if self.lines is None:
                    self.lines=[]
                self.lines.append(line)

            def consume(self):
                if self.lines is None:
                    return None
                else:
                    _ = self.lines
                    self.lines=None
                    return _

            def clean(self):
                self.lines=None



        in_block_comment = False
        is_in_doc_comment = False
        last_doc_comment = DocCommentState()
        current_eol_comment = None
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

        for (line_index,line) in enumerate(self.lines):

            original_line = line
            # replace tabs by spaces
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
            # Line comment --
            #--------------------------------------------------


            # Full line comment
            r = r'^ *--(?P<comment>.*)$'
            m = re.match(r, line)
            if m:
                last_doc_comment.add(m.group('comment'))
                continue

            # Everything that follow is not part of a full line comment
            is_in_doc_comment = False



            # End of line (EOL comment)
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
                continue

            r = r'^ *between *$'
            m = re.match(r, line)
            if m:
                last_doc_comment.clean()
                current_enumeration = None
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
                continue

            #--------------------------------------------------
            # model --
            #--------------------------------------------------

            r = r'^ *model (?P<name>\w+) *$'
            m = re.match(r, line)
            if m:
                self.model = pyuseocl.model.Model(
                    name=m.group('name'),
                    code=self.sourceLines,
                    lineNo = line_no,
                    docComment = last_doc_comment.consume(),
                    eolComment = current_eol_comment
                )
                continue


            #--------------------------------------------------
            # enumeration --
            #--------------------------------------------------

            #---- first line of enumeration (may be one line only) -----------
            r = r'^ *enum +(?P<name>\w+) *{' \
                r' *(?P<literals>[\w+, ]*)' \
                r' *(?P<end>})? *;?' \
                r' *$'
            m = re.match(r, line)
            if m:
                current_context = None
                current_association = None
                current_class = None
                current_attribute = None
                current_operation = None
                literals=[ l
                    for l in m.group('literals').replace(' ','').split(',')
                    if l != ''
                ]
                enumeration = pyuseocl.model.Enumeration(
                    name=m.group('name'),
                    model=self.model,
                    code=line,
                    literals=literals,
                    lineNo=line_no,
                    docComment=last_doc_comment.consume(),
                    eolComment=current_eol_comment,
                )
                self.model.enumerationNamed[m.group('name')] = enumeration
                if m.group('end'):
                    current_enumeration = None
                else:
                    current_enumeration = enumeration
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
                        literals = [l
                                    for l in m.group('literals').replace(' ', '').split(',')
                                    if l != ''
                                    ]
                        for literal in literals:
                            current_enumeration.addLiteral(literal)
                    if m.group('end'):
                        current_enumeration = None
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
                current_class = \
                    pyuseocl.model.Class(
                        name=m.group('name'),
                        model=self.model,
                        isAbstract=m.group('abstract') == 'abstract',
                        superclasses=superclasses,
                        lineNo=line_no,
                        docComment=last_doc_comment.consume(),
                        eolComment=current_eol_comment,
                    )
                if m.group('end') is not None:
                    current_class = None
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
                current_context = None
                current_enumeration = None
                current_attribute = None
                current_operation = None
                # parse superclasses series
                if m.group('superclasses') is None:
                    superclasses = ()
                else:
                    superclasses = [c.strip() for c in m.group('superclasses').split(',')]
                    # print('YYY'+m.group('name'))
                    # print(superclasses)
                ac = \
                    pyuseocl.model.AssociationClass(
                        name=m.group('name'),
                        model=self.model,
                        isAbstract=m.group('abstract') == 'abstract',
                        superclasses=superclasses,
                        lineNo=line_no,
                        docComment=last_doc_comment.consume(),
                        eolComment=current_eol_comment,
                    )
                current_class = ac
                current_association = ac
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
                    # This could be in an association class
                    attribute = pyuseocl.model.Attribute(
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
                    current_enumeration = None
                    current_attribute = None
                    current_condition = None
                    # print('....... ' + str(line_no) + ': ' + line)

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
                    # print('XXX add operation "%s"' % signature)
                    expr=m.group('expr')
                    operation = \
                        pyuseocl.model.Operation(
                            name=m.group('name'),
                            model=self.model,
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
                current_association = \
                    pyuseocl.model.Association(
                        name=m.group('name'),
                        model=self.model,
                        kind=m.group('kind'),
                        lineNo=line_no,
                        docComment=last_doc_comment.consume(),
                        eolComment=current_eol_comment,
                    )
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
                        subsets = removeExtraSpaces(m.group('subsets')).split('subsets ')[1:]
                    # Parse the 'qualifiers' series
                    if m.group('qualifiers') is None:
                        qualifiers = None
                    else:
                        qualifiers = \
                            [tuple(q.split(':'))
                             for q in m.group('qualifiers').replace(' ','').split(',')]
                    pyuseocl.model.Role(
                        name=m.group('name'), # could be empty, but will get default
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
                    continue

            # ---- class context and may be invariant name ----------------------------------------------
            # Could be a model invariant
            #   context
            # rcontext=(
            #     r' *(?P<context>context)'
            #     r' +((?P<vars>[\w ,]+) *:)?'
            #     r' *(?P<classname>\w+)'
            #     r' *(::(?P<signature>\w+\([\w, \(\):]*\)))?'
            # )
            # rcond=(
            #     r' *(?P<existential>existential)?'
            #     r' *(?P<cond>pre|post|inv)'
            #     r' *(?P<name>\w+)?'
            #     r' *:'
            #     r'(?P<expr>.*)'
            # )
            # z='^(%s)?(%s)? *$' % (rcontext,rcond)
            rcontext=(
                r' *(?P<context>context)'
                r' +((?P<vars>[\w ,]+) *:)?'
                r' *(?P<classname>\w+)'
                # r' *(::(?P<signature>\w+\([\w, \(\):]*\)))?'
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
            # print z
            r=re.compile(z)
            # print rcontext
            # print rcond
            # print('++++++ '+r)

            # print('°°°°°°°°°°'+line)
            m = re.match(r, line)
            if m:
                # print('%'*30)
                if m.group('context') is not None or m.group('cond') is not None:
                    # print('cond '+str(line_no)+':'+line)

                    if m.group('context'):
                        # print(':::           context '+m.group('classname'))
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
                        # print(':::        '+m.group('cond')+' '+(m.group('name') if m.group('name') is not None
                        # else '<noname>' + ':'))
                        condname = '' if m.group('name') is None else m.group('name')
                        if m.group('cond') == 'inv':
                            # An invariant can have no context at all. Deal with it.
                            if current_context is None:
                                classname = None
                                variables = None
                            else:
                                classname = current_context['classname']
                                variables = current_context['variables']
                            # 'classname']
                            variable = None if variables is None else variables[0]
                            additionalVariables = \
                                None if variables is None or len(variables) < 2 \
                                else variables[1:]
                            current_condition = pyuseocl.model.Invariant(
                                name=condname,
                                model=self.model,
                                class_=classname,
                                variable=variable,
                                additionalVariables=additionalVariables,
                                isExistential=m.group('existential') == 'existential',
                                expression=m.group('expr'),
                                lineNo=line_no,
                                docComment=last_doc_comment.consume(),
                                eolComment=current_eol_comment,
                            )
                            # print('     inv '+condname+' created')
                        elif m.group('cond') == 'pre':
                            classname = current_context['classname']
                            current_condition = pyuseocl.model.PreCondition(
                                name=condname,
                                model=self.model,
                                class_=classname,
                                operation=current_context['signature'],
                                expression=m.group('expr'),
                                lineNo=line_no,
                                docComment=last_doc_comment.consume(),
                                eolComment=current_eol_comment,
                            )
                            # print('     pre '+condname+' created')
                        elif m.group('cond') == 'post':
                            classname = current_context['classname']
                            current_condition = pyuseocl.model.PostCondition(
                                name=condname,
                                model=self.model,
                                class_=classname,
                                operation=current_context['signature'],
                                expression=m.group('expr'),
                                lineNo=line_no,
                                docComment=last_doc_comment.consume(),
                                eolComment=current_eol_comment,
                            )
                            # print('     post '+condname+' created')
                    continue
            # print('//////////'+line)


            #===========================================================
            #  Continuation stuff
            #===========================================================

            # From here and below only lines that are nested inside
            # entities, so don't use comments if not used before
            last_doc_comment.clean()

            # ---- condition body -----
            # must be before the operation
            # print('#'*80)
            if current_condition is not None:
                # print('00000000 '+str(line_no)+':'+line)
                r = r'^ *(?P<expression>.*) *$'
                m = re.match(r, line)
                if m:
                    # print('match')
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
                continue

            #---- a line has not been processed.
            self.isValid = False
            error = 'PyUseOCL parser: cannot process line #%s: "%s"' % (line_no, line)
            self.errors.append(error)
            # print('****',error)



    def __resolveModel(self):

        def __resolveSimpleType(name):
            """ Search the name in enumeration of basic type or register it.
            """
            if name in self.model.enumerationNamed:
                return self.model.enumerationNamed[name]
            elif name in self.model.basicTypeNamed:
                return self.model.basicTypeNamed[name]
            else:
                self.model.basicTypeNamed[name] = \
                    pyuseocl.model.BasicType(name)
                return self.model.basicTypeNamed[name]

        def __resolveClassType(name):
            """ Search in class names or association class names.
            """
            if name in self.model.classNamed:
                return self.model.classNamed[name]
            else:
                return self.model.associationClassNamed[name]

        def __resolveAttribute(attribute):
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
        #print ('=====', self.model.classes)
        #print ('=====', self.model.classes)

        cs = self.model.classes \
             + self.model.associationClasses
        # print ('**************',cs)
        for c in cs:
            __resolveClass(c)

        # resolve association (and association part of class association)
        as_ = self.model.associations \
              + self.model.associationClasses
        for a in as_:
            __resolveAssociation(a)

        # resolve invariant
        for i in self.model._conditions:
            __resolveCondition(i)

