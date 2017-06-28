# coding=utf-8

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
#from pyuseocl.model import Model, Enumeration, Class, Attribute, \
#    Operation, Invariant, Association, Role, AssociationClass, \
#    PreCondition, PostCondition, BasicType


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
        self.canonicalLines = None  # Nothing yet
        self.canonicalLength = 0    # Nothing yet

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
        #       self.canonicalLines,
        #       self.canonicalLength
        self.__createCanonicalForm()
        if self.isValid:
            # Create the model by parsing the canonical form
            # fill  self.model,
            self.__parseCanonicalLinesAndCreateModel()
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
            self.canonicalLines = engine.out.splitlines()[2:-2]
            self.canonicalLength = len(self.canonicalLines)
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
                # print "MATCH",line,m.group('filename'),
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


    def __parseCanonicalLinesAndCreateModel(self):
        # self.__matches = None
        # self.__i = 0
        #
        # def until(regexp, force=True):
        #     self.__matches = None
        #     while self.__i < self.canonicalLength:
        #         print self.__i, ':', self.canonicalLines[self.__i]
        #         self.__matches = re.match(regexp,
        #                                   self.canonicalLines[self.__i])
        #         if self.__matches is not None:
        #             break
        #         else:
        #             self.__i += 1
        #     if self.__matches is None and force:
        #         raise Exception(
        #             'Error in parsing. Waiting for a line matching %s'
        #             % regexp)

        current_enumeration = None
        current_class = None
        current_association = None
        current_invariant = None
        current_operation = None
        current_operation_condition = None

        for (canonical_line_index,line) in enumerate(self.canonicalLines):
            # print '==',line
            r = r'^(constraints' \
                r'|attributes' \
                r'|operations' \
                r'|    begin' \
                r'|    end' \
                r'|' \
                r'|( *@(Test|Monitor)\(.*\)))$'
            m = re.match(r, line)
            if m:
                # these lines can be ignored
                continue

            #---- model --------------------------------------------------
            r = r'^model (?P<name>\w+)$'
            m = re.match(r, line)
            if m:
                self.model = pyuseocl.model.Model(
                    name=m.group('name'),
                    code=self.sourceLines)
                continue

            #----  enumeration on one line (use version 3) ---------------
            r = r'^enum (?P<name>\w+) { (?P<literals>.*) };?$'
            m = re.match(r, line)
            if m:
                pyuseocl.model.Enumeration(
                    name=m.group('name'),
                    model=self.model,
                    code=line,
                    literals=m.group('literals').split(', '))
                continue

            #---- enumeration header - line # 1 (use version 4) ------------
            r = r'^enum (?P<name>\w+) {$'
            m = re.match(r, line)
            if m:
                current_enumeration =\
                    pyuseocl.model.Enumeration(
                        name=m.group('name'),
                        model=self.model,
                        code=line)
                continue

            #---- enumeration literals - line #2 (use version 4) ------------
            if current_enumeration is not None:
                r = r'^ *(?P<literals>[\w_, ]*) *$'
                m = re.match(r, line)
                if m:
                    literals=m.group('literals').split(', ')
                    for literal in literals:
                        current_enumeration.addLiteral(literal)
                    continue

            #---- enumeration literals - line #3 (use version 4) ------------
            if current_enumeration is not None:
                r = r' *};$'
                m = re.match(r, line)
                if m:
                    current_enumeration =  None
                    continue


            #---- class --------------------------------------------------
            r = r'^((?P<abstract>abstract) )?class (?P<name>\w+)' \
                r'( < (?P<superclasses>(\w+|,)+))?$'
            m = re.match(r, line)
            if m:
                # parse superclasses series
                if m.group('superclasses') is None:
                    superclasses = ()
                else:
                    superclasses = m.group('superclasses').split(',')
                current_class = \
                    pyuseocl.model.Class(
                        name=m.group('name'),
                        model=self.model,
                        isAbstract=m.group('abstract') == 'abstract',
                        superclasses=superclasses
                    )
                continue

            #---- associationclass ---------------------------------------
            r = r'^((?P<abstract>abstract) )?associationclass (?P<name>\w+)' \
                r'( < (?P<superclasses>(\w+|,)+))?' \
                r'( between)?$'
            m = re.match(r, line)
            if m:
                # parse superclasses series
                if m.group('superclasses') is None:
                    superclasses = ()
                else:
                    superclasses = m.group('superclasses').split(',')
                ac = \
                    pyuseocl.model.AssociationClass(
                        name=m.group('name'),
                        model=self.model,
                        isAbstract=m.group('abstract') == 'abstract',
                        superclasses=superclasses
                    )
                current_class = ac
                current_association = ac
                continue

            #---- attribute ----------------------------------------------
            r = r'^  (?P<name>\w+) : (?P<type>\w+)$'
            m = re.match(r, line)
            if m:
                if current_class is not None:
                    # This could be an association class
                    pyuseocl.model.Attribute(
                        name=m.group('name'),
                        class_=current_class,
                        code=line,
                        type=m.group('type'))
                    continue

            #---- operation ----------------------------------------------
            r = r'^  (?P<name>\w+)' \
                r'(?P<params_and_result>[^=]*)' \
                r'( = )?$'
            # r = r'^  (?P<name>\w+)' \
            #    r'\((?P<parameters>.*)\)' \
            #    r'( : (?P<type>(\w|,|\))+))?' \
            #    r'( =)?'
            m = re.match(r, line)
            if m and '(' in line and ')' in line:
                if current_class is not None:
                    # print line
                    # This could be an association class
                    operation = \
                        pyuseocl.model.Operation(
                            name=m.group('name'),
                            model=self.model,
                            class_=current_class,
                            code=line,
                            signature=m.group('name')
                                      + m.group('params_and_result'))
                    if line.endswith(' = '):
                        current_operation = operation
                    else:
                        current_operation = None
                    #print '==',line
                    #print '   ', operation.signature
                    #print '   "%s"' % operation.full_signature
                    #print

                    continue

            #---- operation expression -----------------------------------
            r = r'^    (?P<expression>[^ ].*)$'
            m = re.match(r, line)
            if m:
                if current_operation is not None:
                    # This could be an association class
                    current_operation.expression = m.group('expression')
                    continue

            #---- association --------------------------------------------
            r = r'^(?P<kind>association|composition|aggregation) ' \
                r'(?P<name>\w+) between$'
            m = re.match(r, line)
            if m:
                current_association = \
                    pyuseocl.model.Association(
                        name=m.group('name'),
                        model=self.model,
                        kind=m.group('kind'))
                continue

            #---- role ---------------------------------------------------
            r = r'^  (?P<type>\w+)\[(?P<cardinality>[^\]]+)\] *' \
                r'(role (?P<name>\w+))?' \
                r'( qualifier \((?P<qualifiers>(\w| |:|,)*)\))?' \
                r'(?P<subsets>( subsets \w+)*)' \
                r'( (?P<union>union))?' \
                r'( (?P<ordered>ordered))?' \
                r'( (derived = (?P<expression>.*)))?$'
            m = re.match(r, line)
            if m:
                if current_association is not None:
                    # This could be an association class
                    # Parse the cardinality string
                    c = m.group('cardinality').split('..')
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
                        #print '***************', line
                        #print '**  ',m.group('subsets')
                        subsets = m.group('subsets').split('subsets ')[1:]
                        #print s
                    # Parse the 'qualifiers' series
                    if m.group('qualifiers') is None:
                        qualifiers = None
                    else:
                        qualifiers = \
                            [tuple(q.split(' : '))
                             for q in m.group('qualifiers').split(', ')]
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
                        expression=m.group('expression')
                    )
                    continue

            #---- invariant ----------------------------------------------
            r = r'^context (?P<vars>(\w| |,)+) : (?P<class>\w+)' \
                r'( (?P<existential>existential))? inv (?P<name>\w+):$'
            m = re.match(r, line)
            if m:
                variables = m.group('vars').split(', ')
                current_invariant = \
                    pyuseocl.model.Invariant(
                        name=m.group('name'),
                        model=self.model,
                        class_=m.group('class'),
                        variable=variables[0],
                        additionalVariables=variables[1:],
                        isExistential=
                        m.group('existential') == 'existential',
                    )
                continue

            #---- invariant expression -----------------------------------
            r = r'^  (?P<expression>[^ ].*)$'
            m = re.match(r, line)
            if m:
                if current_invariant is not None:
                    current_invariant.expression = m.group('expression')
                    current_invariant = None
                    continue

            #---- pre or post condition ----------------------------------
            r = r'^context (?P<class>\w+)::' \
                r'(?P<signature>\w+.*)$'
            m = re.match(r, line)
            if m:
                full_signature = \
                    '%s::%s' % (m.group('class'), m.group('signature'))
                operation = self.model.operations[full_signature]
                current_operation_condition = {
                    'class': m.group('class'),
                    'full_signature': full_signature,
                    'operation': operation
                }
                continue

            #---- body of pre or post condition --------------------------
            r = r'^  (?P<kind>(pre|post)) (?P<name>\w+): ' \
                r'(?P<expression>.*)$'
            m = re.match(r, line)
            if m:
                if current_operation_condition is not None:
                    operation = current_operation_condition['operation']
                    v = m.groupdict()
                    if v['kind'] == 'pre':
                        pyuseocl.model.PreCondition(
                            v['name'], self.model, operation, v['expression'])
                    else:
                        pyuseocl.model.PostCondition(
                            v['name'], self.model, operation, v['expression'])

                    current_operation_condition = None
                    continue

            #---- end of association, class, invariant or operation ------
            r = r'^(end)$'  # match empty line as well
            m = re.match(r, line)
            if m:
                current_class = None
                current_association = None
                continue

            #---- a line has not been processed.
            self.isValid = False
            error = 'Parser: cannot process cannonical line #%s: "%s"' % (canonical_line_index, line)
            self.errors.append(error)
            print error


    def __resolveModel(self):

        def __resolveSimpleType(name):
            """ Search the name in enumeration of basic type or register it.
            """
            if name in self.model.enumerations:
                return self.model.enumerations[name]
            elif name in self.model.basicTypes:
                return self.model.basicTypes[name]
            else:
                self.model.basicTypes[name] = \
                    pyuseocl.model.BasicType(name)
                return self.model.basicTypes[name]

        def __resolveClassType(name):
            """ Search in class names or association class names.
            """
            if name in self.model.classes:
                return self.model.classes[name]
            else:
                return self.model.associationClasses[name]

        def __resolveAttribute(attribute):
            # Resolve the attribute type
            attribute.type = __resolveSimpleType(attribute.type)

        def __resolveOperation(operation):
            # TODO: implement parsing of parameters and result type
            raise NotImplementedError('operation resolution not implemented')

        def __resolveClass(class_):
            # resolve superclasses
            class_.superclasses = \
                [__resolveClassType(name) for name in class_.superclasses]
            # resolve class attributes
            for a in class_.attributes.values():
                __resolveAttribute(a)
            # resolve class operations
            for op in class_.operations:
                pass  # TODO

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
            if role.association.isBinary:
                rs = role.association.roles.values()
                role.opposite = rs[1] if role is rs[0] else rs[0]

        def __resolveAssociation(association):
            association.arity = len(association.roles)
            association.isBinary = (association.arity == 2)
            for role in association.roles.values():
                __resolveRole(role)

        def __resolveInvariant(invariant):
            c = __resolveClassType(invariant.class_)
            invariant.class_ = c
            c.invariants[invariant.name] = invariant

        # resolve class (and class part of class associations)
        cs = self.model.classes.values() \
             + self.model.associationClasses.values()
        for c in cs:
            __resolveClass(c)

        # resolve association (and association part of class association)
        as_ = self.model.associations.values() \
              + self.model.associationClasses.values()
        for a in as_:
            __resolveAssociation(a)

        # resolve invariant
        for i in self.model.invariants:
            __resolveInvariant(i)

