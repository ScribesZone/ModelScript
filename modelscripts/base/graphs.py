

def isCyclic(g):
    """Return True if the directed graph g has a cycle.
    g must be represented as a dictionary mapping vertices to
    iterables of neighbouring vertices. For example:

    >>> isCyclic({1: (2,), 2: (3,), 3: (1,)})
    True
    >>> isCyclic({1: (2,), 2: (3,), 3: (4,)})
    False

    adapted from https://codereview.stackexchange.com/questions/86021/check-if-a-directed-graph-contains-a-cycle

    """
    path = set()
    visited = set()

    def visit(vertex):
        if vertex in visited:
            return False
        visited.add(vertex)
        path.add(vertex)
        for neighbour in g.get(vertex, ()):
            if neighbour in path or visit(neighbour):
                return True
        path.remove(vertex)
        return False

    return any(visit(v) for v in g)