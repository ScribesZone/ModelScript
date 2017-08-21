# coding=utf-8
from __future__ import unicode_literals, print_function, absolute_import, division
from typing import Text, Union, Optional, Dict, List

from modelscripts.use.use.printer import (
    UsePrinter
)



class Printer(UsePrinter):
    def __init__(self, classModel):
        super(Printer, self).__init__(model=classModel)
