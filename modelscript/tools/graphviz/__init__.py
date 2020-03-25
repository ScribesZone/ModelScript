
import os
from typing import Dict, Text, Optional
from graphviz import (
    Digraph,
    Graph,
)

THIS_DIR=os.path.dirname(__file__)
RES_DIR=os.path.join(THIS_DIR,'res')
IMAGE_DIR=os.path.join(RES_DIR,'images')

class Mapping(object):

    def __init__(self, prefixId='id'):
        self.prefixId = prefixId
        self.nextCounts=dict()
        self.objToId=dict()
        #type: Dict[Text, object]
        self.idToObj=dict()
        #type: Dict[object, Text]

    def id(self, object, prefixId=None):
        #type: (object, Optional[Text]) -> Text
        if object in self.objToId:
            return self.objToId[object]
        else:
            prefixId = (
                self.prefixId if prefixId is None
                else prefixId)
            if prefixId not in self.nextCounts:
                count=1
            else:
                count=self.nextCounts[prefixId]+1
            self.nextCounts[prefixId] = count
            id=prefixId+str(count)
            self.objToId[object]=id
            self.idToObj[id]=object
            return id

    def obj(self, id):
        #type: (Text) -> object
        return self.objToId[id]


class MDigraph(Digraph, Mapping):

    def __init__(self,
                 name=None,
                 comment=None,
                 filename=None,
                 directory=None,
                 format=None,
                 engine=None,
                 encoding='utf-8',
                 graph_attr=None,
                 node_attr=None,
                 edge_attr=None,
                 body=None,
                 strict=False,
                 prefixId='id'):
        Digraph.__init__(self,
                 name=name,
                 comment=comment,
                 filename=filename,
                 directory=directory,
                 format=format,
                 engine=engine,
                 encoding=encoding,
                 graph_attr=graph_attr,
                 node_attr=node_attr,
                 edge_attr=edge_attr,
                 body=body,
                 strict=strict)
        Mapping.__init__(self,
                prefixId=prefixId)




def imagePath(relFilename):
    return os.path.join(IMAGE_DIR, relFilename)

