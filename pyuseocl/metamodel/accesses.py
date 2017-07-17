# coding=utf-8
"""
"""
from __future__ import absolute_import, division, print_function, unicode_literals
from typing import Text, List, Set, Dict, Optional, Union

from pyuseocl.metamodel.permissions import (
    Player,
    Op,
    Ops,
    Resource,
)

# Removed this to avoid circular dependency  accesses<->scenarios
# from pyuseocl.metamodel.scenarios import (
#     Block
# )


class Access(object):

    def __init__(self, op, resource, accessSet):
        #type: (Op, Resource, AccessSet) -> None
        self.op=op
        self.resource=resource
        self.accessSet=accessSet
        self.accessSet.add(self)

class AccessSet(object):

    def __init__(self, container):
        ## see import type: (Union[Block]) -> None
        # currently accesses are extracted only from AccessSet
        # but it could be nice to extract them from invariants
        # and from interactive ocl expression ??
        # There is a relation with "player" but not sure what
        # is best
        self.accesses=[] #type: List[Access]
        self.container=container

    def add(self, access):
        #type: (Access) -> None
        self.accesses.append(access)

    @property
    def resources(self):
        #type: ()->Set(Resource)
        return {
            a.resource
            for a in self.accesses
        }
    def resourceOps(self, resource):
        #type: (Resource) -> Ops
        ops = [
            a.op
            for a in self.accesses
            if a.resource==resource ]
        return set(ops)
