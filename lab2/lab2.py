from collections import deque

from utils.test import Test
import utils.utils as ut
from utils import dimacs

def get_parents_bfs(graphMatrix, flow, visited, visitedId, source, target):
    V = len(graphMatrix)

    toCheck = deque([source])
    visited[source] = visitedId
    parents = [None for _ in range(V)]

    foundPath = False

    while toCheck:
        vertex = toCheck.popleft()

        if vertex == target:
            foundPath = True
            break

        for neighbour in range(V):
            edgeWeight = graphMatrix[vertex][neighbour] - flow[vertex][neighbour]
            # check if we can send water via this edge and if neighbour is not visited
            if edgeWeight > 0 and visited[neighbour] != visitedId:
                visited[neighbour] = visitedId
                parents[neighbour] = vertex
                toCheck.append(neighbour)

    return foundPath, parents

def get_parents_dfs(graphMatrix, flow, visited, visitedId, source, target):
    def dfs_visit(vertex):
        visited[vertex] = visitedId

        if vertex == target:
            return True

        for neighbour in range(V):
            edgeWeight = graphMatrix[vertex][neighbour] - flow[vertex][neighbour]
            # check if we can send water via this edge and if neighbour is not visited
            if edgeWeight > 0 and visited[neighbour] != visitedId:
                parents[neighbour] = vertex
                if dfs_visit(neighbour):
                    return True

        return False
    # end def

    V = len(graphMatrix)

    parents = [None for _ in range(V)]

    foundPath = dfs_visit(source)

    return foundPath, parents

def update_flow(graphMatrix, flow, target, parents):
    V = len(graphMatrix)

    # find bottleneck
    bottleneck = float("inf")

    prev, vertex = parents[target], target
    while prev is not None:
        edgeWeight = graphMatrix[prev][vertex] - flow[prev][vertex]
        bottleneck = min(bottleneck, edgeWeight)
        prev, vertex = parents[prev], prev

    # update flow
    prev, vertex = parents[target], target
    while prev is not None:
        flow[prev][vertex] += bottleneck
        flow[vertex][prev] -= bottleneck
        prev, vertex = parents[prev], prev

def ford_fulkerson(graphMatrix, V, source, get_parents_method):
    target = V - 1
    flow = [[0 for _ in range(V)] for _ in range(V)]

    visited = [0 for _ in range(V)]
    visitedId = 0

    while True:
        visitedId += 1

        foundPath, parents = get_parents_method(graphMatrix, flow, visited, visitedId, source, target)

        if not foundPath:
            break

        update_flow(graphMatrix, flow, target, parents)

    maxFlow = 0
    for vertex in range(V):
        maxFlow += flow[vertex][target]

    return maxFlow

def edges_to_directed_weighted_matrix(graphEdges, V):
    NO_EDGE = 0
    matrix = [[NO_EDGE for _ in range(V)] for _ in range(V)]

    for vertex, neighbour, weight in graphEdges:
        vertex -= 1
        neighbour -= 1
        matrix[vertex][neighbour] = weight

    return matrix

if __name__ == "__main__":
    graphsDir = "./flow"
    myTest = Test(graphsDir, dimacs.loadDirectedWeightedGraph, dimacs.readSolution, ut.edges_to_directed_weighted_matrix, ford_fulkerson, 0, get_parents_bfs)
    myTest.test_all()
