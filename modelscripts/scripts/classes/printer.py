# coding=utf-8
from __future__ import unicode_literals, print_function, absolute_import, division
from typing import Text, Union, Optional, Dict, List

from modelscripts.use.use.printer import (
    UseSourcePrinter,
    UseModelPrinter
)



class ModelPrinter(UseModelPrinter):
    def __init__(self,
                 theModel,
                 summary=False,
                 displayLineNos=True):
        super(ModelPrinter, self).__init__(
            theModel=theModel,
            summary=summary,
            displayLineNos=displayLineNos)

class SourcePrinter(UseSourcePrinter):
    def __init__(self,
                 theSource,
                 summary=False,
                 displayLineNos=True):
        super(UseSourcePrinter, self).__init__(
            theSource=theSource,
            summary=summary,
            displayLineNos=displayLineNos)