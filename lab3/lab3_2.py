import dimacs

import sys
sys.path.insert(0, "../utils")
import utils
from test import Test

class Vertex:
    def __init__(self, idx) -> None:
        self.idx = idx
        self.edges = {}

    def add_edge(self, neighbourIdx, weight) -> None:
        self.edges[neighbourIdx] = self.edges.get(neighbourIdx, 0) + weight

    def get_weights_sum(self, verticiesIndicies):
        weightsSum = 0
        for vertexIdx in verticiesIndicies:
            if vertexIdx not in self.edges:
                continue

            weightsSum += self.edges[vertexIdx]

        return weightsSum

    def get_edges(self):
        return self.edges.items()

    def delete_edge(self, neighbourIdx):
        del self.edges[neighbourIdx]

    def __hash__(self) -> int:
        return hash(self.idx)

class Graph:
    def __init__(self, edgesList, V) -> None:
        self.edgesList = edgesList
        self.V = V

        self.verticies: dict[int, Vertex] = {}
        self.create_graph()

    def create_graph(self):
        for vertexIdx, neighbourIdx, weight in self.edgesList:
            if vertexIdx not in self.verticies:
                vertex = Vertex(vertexIdx)
                self.verticies[vertexIdx] = vertex
            if neighbourIdx not in self.verticies:
                neighbour = Vertex(neighbourIdx)
                self.verticies[neighbourIdx] = neighbour

            self.verticies[vertexIdx].add_edge(neighbourIdx, weight)
            self.verticies[neighbourIdx].add_edge(vertexIdx, weight)

    def get_connectivity_weight(self, vertexIdx, verticiesIndicies):
        return self.verticies[vertexIdx].get_weights_sum(verticiesIndicies)

    def get_verticies_list(self):
        return list(self.verticies.keys())

    def merge(self, vertex1, vertex2):
        # ensure that vertex1 has lower index
        if vertex2 < vertex1:
            vertex1, vertex2 = vertex2, vertex1

        for neighbourIdx, weight in self.verticies[vertex2].get_edges():
            self.verticies[vertex1].add_edge(neighbourIdx, weight)

        if vertex2 in self.verticies[vertex1].edges:
            self.verticies[vertex1].delete_edge(vertex2)

        del self.verticies[vertex2]

    def __len__(self):
        return len(self.verticies)

def get_cut(graph: Graph):
    verticiesIndiciesList = graph.get_verticies_list()
    firstVertex = verticiesIndiciesList[0]

    remainingVerticies = set(verticiesIndiciesList[1:])

    V = len(verticiesIndiciesList)
    cutVerticiesIndiciesSet = set()
    cutVerticiesIndiciesSet.add(firstVertex)

    minConnectivityVertex = firstVertex

    while len(remainingVerticies) > 1:
        minConnectivity = utils.INF
        for vertex in remainingVerticies:
            connectivity = graph.get_connectivity_weight(vertex, cutVerticiesIndiciesSet)
            if connectivity < minConnectivity:
                minConnectivity = connectivity
                minConnectivityVertex = vertex

        cutVerticiesIndiciesSet.add(minConnectivityVertex)
        remainingVerticies.remove(minConnectivityVertex)

    lastVertex = next(iter(remainingVerticies))
    currentCut = graph.get_connectivity_weight(lastVertex, cutVerticiesIndiciesSet)

    lastMinConnectivityVertex = minConnectivityVertex

    graph.merge(lastMinConnectivityVertex, lastVertex)

    return currentCut

def stoer_wagner(edgesList, V):
    graph = Graph(edgesList, V)

    minCut = utils.INF

    while len(graph) > 1:
        currentCut = get_cut(graph)
        minCut = min(minCut, currentCut)

    return minCut

if __name__ == "__main__":
    graphsDir = "./graphs"
    myTest = Test(graphsDir, dimacs.loadWeightedGraph, dimacs.readSolution, lambda x, *args: x, stoer_wagner)
    # myTest.test_graph("path")
    myTest.test_all()