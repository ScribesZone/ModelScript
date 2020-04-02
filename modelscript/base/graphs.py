# coding=utf-8
"""Graph management helpers"""

__all__ = (
    'genPaths',
    'cycles'
)

from typing import List, Callable, TypeVar

Node = TypeVar('Node')
GraphEdgesFun = Callable[[Node], List[Node]]


def genPaths(successors: GraphEdgesFun,
             start: Node,
             end: Node)\
        -> List[List[Node]]:
    """Generates all possible paths between a node and another.

    list(genPaths(g,'a','c')) could be like  [[b],[b,c]].
    This is a generator, so it does not return directly a list.
    The graph is represented as a successors function, that is a
    function that give a list of successors for a given node.
    The function must be defined for all nodes.
    This function could serve to identify cycles.
    Adapted from https://stackoverflow.com/questions/40833612/find-all-cycles-in-a-graph-implementation
    For the existence of cycle see also
    https://codereview.stackexchange.com/questions/86021/check-if-a-directed-graph-contains-a-cycle
    """
    fringe = [(start, [])]
    while fringe:
        # noinspection PyUnresolvedReferences
        state, path = fringe.pop()
        if path and state == end:
            yield [start]+path
            continue
        for next_state in successors(state):
            if next_state in path:
                continue
            fringe.append((next_state, path+[next_state]))


def cycles(nodes: List[Node],
           successors: GraphEdgesFun) \
        -> List[List[Node]]:
    """
    Return all the cycles that exist in a graph.
    The edges are given via a sucessors function. This function
    must be defined for all nodes.
    """
    return [
        path
        for node in nodes
            for path in genPaths(successors, node, node)]