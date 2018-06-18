from __future__ import absolute_import
import os
from typing import Dict, Text, Optional
from graphviz import (
    Digraph
)

THIS_DIR=os.path.dirname(__file__)
RES_DIR=os.path.join(THIS_DIR,'res')
IMAGE_DIR=os.path.join(RES_DIR,'images')

class Mapping(object):

    def __init__(self, prefix='id'):
        self.prefix = prefix
        self.nextCounts=dict()
        self.objToId=dict()
        #type: Dict[Text, object]
        self.idToObj=dict()
        #type: Dict[object, Text]

    def id(self, object, prefix=None):
        #type: (object, Optional[Text]) -> Text
        if object in self.objToId:
            return self.objToId[object]
        else:
            prefix = self.prefix if prefix is None else prefix
            if prefix not in self.nextCounts:
                count=1
            else:
                count=self.nextCounts[prefix]+1
            self.nextCounts[prefix] = count
            id=prefix+str(count)
            self.objToId[object]=id
            self.idToObj[id]=object
            return id

    def obj(self, id):
        #type: (Text) -> object
        return self.objToId[id]


def imagePath(relFilename):
    return os.path.join(IMAGE_DIR, relFilename)

