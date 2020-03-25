# coding=utf-8
"""
    Parse a given .stc file and return the information
    associated with each check point output, that is, information
    about invariant success and invariant failure.
    Returns a UseOuput object, defined as following::

    UseOutput
    <>-* CheckPointOutput
       -- useOutput
       <>-* InvariantOutput

    InvariantOutput
    -- className
    -- invariantName
    -- hasFailed
    <|-- InvariantSuccessOutput
    <|-- InvariantFailureOutput
        --* violatingObjectNames
        -- violatingObjectType
        -- resultValue
        -- resultType
        --* subexpressions
"""


from typing import List, Text, Optional
import re
from collections import OrderedDict


#---------- output structure ---------------------------------------------

class UseOutput(object):
    """
    A list of CheckPointOutut
    """

    def __init__(self):
        self.checkPoints=[]
        #type: List[CheckPointOutput]


class CheckPointOutput(object):

    def __init__(self, useOutput):
        self.useOutput=useOutput
        self.invariantOutputs=[]
        #type: List[InvariantOutput]

        # Back link
        self.useOutput.checkPoints.append(self)


class InvariantOutput(object):

    def __init__(self, checkPointOutput,
                 className, invariantName, hasFailed):
        self.checkPointOutput=checkPointOutput
        self.className=className  # class or association class
        self.invariantName=invariantName
        self.hasFailed=hasFailed

        # Back link
        self.checkPointOutput.invariantOutputs.append(self)


class InvariantSuccessOutput(InvariantOutput):

    def __init__(self,
                 checkPointOutput,
                 className, invariantName):
        super(InvariantSuccessOutput, self).__init__(
            checkPointOutput=checkPointOutput,
            className=className,
            invariantName=invariantName,
            hasFailed=False)


class InvariantFailureOutput(InvariantOutput):

    def __init__(self,
                 checkPointOutput,
                 className, invariantName):
        super(InvariantFailureOutput, self).__init__(
            checkPointOutput=checkPointOutput,
            className=className,
            invariantName=invariantName,
            hasFailed=True)

        # These attributes are set later when parsing lines after lines
        self.violatingObjectNames=[]
        #type: List[Text]

        self.violatingObjectType=None
        #type: Optional[Text]

        self.resultValue=None
        #type: Optional[Text]

        self.resultType=None
        #type: Optional[Text]

        self.subexpressions=[]
        #type: List[Text]




#---------- parser ----------------------------------------------------

class UseCheckOutputsParser(object):
    """
    Parse a given .stc file and return the information
    associated with each check point output, that is information
    about invariant success and invariant failure.
    """

    def __init__(self, useOutputFile):
        self.useOutputFile=useOutputFile
        with open(useOutputFile) as f:
            lines = f.readlines()
        lines = [x.rstrip() for x in lines]
        self.lines=lines
        self.useOutput=UseOutput()


    def parse(self):
        begin=r' *'
        end=' *$'
        current_check_output=None
        #type: Optional[CheckPointOutput]
        current_invariant_failure=None
        for line in self.lines:
            print('66'*10, line)
            r=(begin
                +r'checked \d+ invariants in .*'
                +end)
            m = re.match(r, line)
            if m:
                current_invariant_failure=None
                current_check_output=None
                continue

            r=(begin
               +'checking invariants...'
               +end)
            m = re.match(r, line)
            if m:
                current_check_output=\
                    CheckPointOutput(
                        useOutput=self.useOutput)
                continue

            r=(begin
                +r'checking invariant \(\d+\) `'
                +r'(?P<class>\w+)'
                +r'::(?P<invname>\w+)'
                +r'\': '
                +r'(?P<result>OK|FAILED)\.'
                +end)
            m = re.match(r, line)
            if m:
                has_failed=m.group('result')=='FAILED'
                class_name=m.group('class')
                invariant_name=m.group('invname')

                if not has_failed:
                    InvariantSuccessOutput(
                        checkPointOutput=current_check_output,
                        className=class_name,
                        invariantName=invariant_name)
                else:
                    current_invariant_failure = \
                        InvariantFailureOutput(
                            checkPointOutput=current_check_output,
                            className=class_name,
                            invariantName=invariant_name)
                continue

            if current_invariant_failure:

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
                    +r' *-> Set\{(?P<expr>[\w ,]+)\}'
                    +r' : Set\((?P<type>\w+)\)'
                    +end)
                m = re.match(r, line)
                if m:
                    names=[ x.strip()
                            for x in m.group('expr').split(',')
                            if x!='' ]

                    current_invariant_failure\
                        .violatingObjectNames=names
                    current_invariant_failure\
                        .violatingObjectType=m.group('type')
                    current_invariant_failure=None
                    continue

                # WARNING: this rule MUST be after the one
                # like -> Set\{ ...
                # Otherwise this one catch the other one
                r=(begin
                    +r'  -> (?P<expr>.*) : (?P<type>.*)'
                    +end)
                m = re.match(r, line)
                if m:
                    current_invariant_failure\
                        .resultValue=m.group('expr')
                    current_invariant_failure\
                        .resultType=m.group('type')
                    continue

                # WARNING: this rule MUST be at the end
                # Otherwise this one catch the other ones
                r=(begin
                    +r'  (?P<expr>.*)'
                    +end)
                m = re.match(r, line)
                if m:
                    current_invariant_failure.subexpressions.append(
                        m.group('expr'))
                    continue
        return self.useOutput
