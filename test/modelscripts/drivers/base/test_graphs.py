from modelscripts.base.graphs import (
    genPaths,
    cycles)

class TestGraph(object):

    def testGraph1(self):
        graph = {1: [2,3], 2: [4], 3: [4], 4: []}
        succs=lambda x:graph[x]
        assert list(genPaths(succs, 4,1))==[]
        assert list(genPaths(succs, 3,3))==[]
        assert list(genPaths(succs, 3,4))==[[3,4]]
        assert list(genPaths(succs, 1,4))==[[1,3,4],[1,2,4]]
        assert list(genPaths(succs, 1,1))==[]
        assert list(genPaths(succs, 4,4))==[]
        assert cycles(graph.keys(), succs)== []

    def testGraph2(self):
        graph = {1: [2, 3, 5], 2: [1], 3: [1], 4: [2], 5: [2]}
        succs=lambda x:graph[x]
        assert list(genPaths(succs, 1,4))==[]
        assert list(genPaths(succs, 1,2))== \
               [[1, 5, 2], [1, 3, 1, 5, 2], [1, 3, 1, 2], [1, 2]]
        assert list(genPaths(succs, 1,1))== \
               [[1, 5, 2, 1], [1, 3, 1], [1, 2, 1]]
        assert list(genPaths(succs, 1,2))==\
               [[1, 5, 2], [1, 3, 1, 5, 2], [1, 3, 1, 2], [1, 2]]
        assert cycles(graph.keys(), succs)== \
               [[1, 5, 2, 1], [1, 3, 1], [1, 2, 1],
                [2, 1, 5, 2], [2, 1, 2],
                [3, 1, 3],
                [5, 2, 1, 5]]

    def testGraph3(self):
        graph = {1: [1]}
        succs=lambda x:graph[x]
        assert list(genPaths(succs, 1,1))==[[1,1]]
        assert cycles(graph.keys(), succs)== [[1,1]]


# graph1={ 1: [2, 3, 5], 2: [1], 3: [1], 4: [2], 5: [2] }
# graph2={1:[2],2:[3],3:[1],4:[1]}
# graph3={1: [2], 2: [3], 3: [4], 4:[]}
# graph4={1: [2], 2: [1], 3: [2], 4:[4]}
