# coding=utf-8
"""
Access metamodel.

The structure of this package is the following::

    AccessModel
    <>--1 AccessSet
         <>--* Access

"""
from __future__ import absolute_import, division, print_function, unicode_literals
from typing import Text, List, Set, Dict, Optional, Union

from modelscripts.utils import Model

from modelscripts.metamodels.permissions import (
    Player,
    Op,
    Ops,
    Resource,
)

# Removed this to avoid circular dependency  accesses<->scenarios
# from modelscript.metamodels.scenarios import (
#     Block
# )

class AccessModel(Model):

    def __init__(self, source=None):
        super(AccessModel, self).__init__(
            source=source
        )
        self.accessSet=None


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


class Access(object):

    def __init__(self, op, resource, accessSet):
        #type: (Op, Resource, AccessSet) -> None
        self.op=op
        self.resource=resource
        self.accessSet=accessSet
        self.accessSet.add(self)

