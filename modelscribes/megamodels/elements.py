# coding=utf-8

from modelscribes.metamodels.textblocks import (
    TextBlockModel
)

class ModelElement(object):

    def __init__(self):
        self.stereotypes=[]
        self.tags=[]
        self.description=TextBlockModel.empty()



 # ModelElement.__init__(self)