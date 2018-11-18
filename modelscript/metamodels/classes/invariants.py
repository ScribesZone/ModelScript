from typing import List, Text, Optional
from modelscript.megamodels.elements import SourceModelElement

from modelscript.metamodels.classes import (
    PackagableElement,
    Item)

class Invariant(PackagableElement, Item):

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
        #type: List[Text,Optional[Text]]
        # TODO:3 transform Invariant Item references to ~"Item"

        self.oclInvariants=[]
        #type: List[OCLInvariant]
        # A CLS logical invariant can contain various OCL invariant

        # Back link
        model._invariantNamed[name]=self

    @property
    def hasOCLCode(self):
        for ocl_inv in self.oclInvariants:
            if ocl_inv.hasOCLCode:
                return True
        else:
            return False


class OCLInvariant(SourceModelElement):

    def __init__(self, invariant, context=None,
                 lineNo=None, description=None, astNode=None):

        # add nth to invariant name except for 1st
        nth=len(invariant.oclInvariants)+1
        suffix=unicode(nth) if nth>=2 else ''

        super(OCLInvariant, self).__init__(
            name=invariant.name+suffix,
            model=invariant.model,
            astNode=astNode,
            lineNo=lineNo,
            description=description)

        self.context=context
        #type: OCLContext
        # Keeping this as a class
        # is useful to generate USE OCL code with
        # keeping record of the proper line number

        self.oclLines=[]
        #type: List[OCLLine]

        # back link
        invariant.oclInvariants.append(self)

    @property
    def hasOCLCode(self):
        return len(self.oclLines)>=1


class OCLContext(SourceModelElement):

    def __init__(self, invariant, class_,
                 lineNo=None, description=None, astNode=None):
        super(OCLContext, self).__init__(
            name=None,
            model=invariant.model,
            astNode=astNode,
            lineNo=lineNo,
            description=description)

        self.class_=class_
        #type: Text # TODO:3 do resolution on OCL class name

        # Back link
        invariant.context=self


class OCLLine(SourceModelElement):

    def __init__(self, oclInvariant, textLine,
                    astNode=None):
        # add nth to ocl invariant name
        suffix='_'+unicode(len(oclInvariant.oclLines)+1)
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
        # Filled by ClassOCLChecker/USEPrinter

        #back link
        oclInvariant.oclLines.append(self)

