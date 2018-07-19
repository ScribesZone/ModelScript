from typing import List, Text, Optional
from modelscripts.megamodels.elements import SourceModelElement

from modelscripts.metamodels.classes import (
    PackagableElement,
    Entity)

class Invariant(PackagableElement, Entity):

    def __init__(self, name, model, derivedItem, scopeItems,
                 package=None,
                 lineNo=None, description=None, astNode=None):
        super(Invariant, self).__init__(
            name=name,
            model=model,
            package=package,
            astNode=astNode,
            lineNo=lineNo,
            description=description)

        self.derivedItem = derivedItem
        #type: Optional['Item']

        self.scopeItems = scopeItems
        #type: List[Text,Optional[Text]]  # TODO: transform to ~"Item"

        self.oclInvariants=[]
        #type: List[OCLInvariant]

        # Back link
        model._invariantNamed[name]=self


class OCLInvariant(SourceModelElement):

    def __init__(self, invariant, contextClass,
                 lineNo=None, description=None, astNode=None):

        # add nth to invariant name except for 1st
        nth=str(len(invariant.oclInvariants)+1)
        suffix=nth if nth>=2 else ''

        super(OCLInvariant, self).__init__(
            name=invariant.name+suffix,
            model=invariant.model,
            astNode=astNode,
            lineNo=lineNo,
            description=description)

        self.contextClass=contextClass
        #type: Text # TODO:

        self.oclLines=[]
        #type: List[OCLLine]

        # back link
        invariant.oclInvariants.append(self)


class OCLLine(SourceModelElement):

    def __init__(self, oclInvariant, textLine,
                    astNode=None):
        # add nth to ocl invariant name
        suffix='_'+str(len(oclInvariant.oclLines)+1)
        super(OCLLine, self).__init__(
            name=oclInvariant.name+suffix,
            model=oclInvariant.model,
            astNode=astNode,
            lineNo=None,
            description=None)

        self.textLine=textLine
        #type: Text

        self.useOCLLineNo=None
        #type: Optional[int]
        # Filled by OCLChecker/USEPrinter

        #back link
        oclInvariant.oclLines.append(self)

