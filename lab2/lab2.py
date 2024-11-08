import dimacs
# import os
# import time
from collections import deque

import sys
sys.path.insert(0, "../utils")
from test import Test
import utils as ut

# from utils.test import Test
# import utils.utils as ut

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


def ford_fulkerson(graphMatrix, source, target, get_parents_method):
    V = len(graphMatrix)
    flow = [[0 for _ in range(V)] for _ in range(V)]

    visited = [0 for _ in range(V)]
    visitedId = 0

    while True:
        visitedId += 1

        foundPath, parents = get_parents_method(graphMatrix, flow, visited, visitedId, source, target)

        if not foundPath:
            break

        # print(foundPath)
        # print(parents)

        update_flow(graphMatrix, flow, target, parents)

    maxFlow = 0
    for vertex in range(V):
        maxFlow += flow[vertex][target]

    return maxFlow

def ford_fulkerson_for_test(graphMatrix, V, source, get_parents_method):
    target = V - 1
    flow = [[0 for _ in range(V)] for _ in range(V)]

    visited = [0 for _ in range(V)]
    visitedId = 0

    while True:
        visitedId += 1

        foundPath, parents = get_parents_method(graphMatrix, flow, visited, visitedId, source, target)

        if not foundPath:
            break

        # print(foundPath)
        # print(parents)

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

# def test_graph(graphName: str, flow_function):
#     pathToFile = os.path.join(graphsDir, graphName)
#     V, graphEdges = dimacs.loadDirectedWeightedGraph(pathToFile)

#     source = 0
#     target = V - 1
#     graphMatrix = edges_to_directed_weighted_matrix(graphEdges, V)
#     print(*graphMatrix, sep="\n")
#     solution = int(dimacs.readSolution(pathToFile))
#     print(solution)
#     mySolution = flow_function(graphMatrix, source, target)
#     print(mySolution)

# def test_function(flow_function):
#     passed = 0
#     failed = 0
#     total = 0

#     for fileName in os.listdir(graphsDir):
#         print(f"\n\n######### {fileName} #########\n\n")

#         pathToFile = os.path.join(graphsDir, fileName)
#         V, graphEdges = dimacs.loadDirectedWeightedGraph(pathToFile)

#         source = 0
#         target = V - 1
#         graphMatrix = edges_to_directed_weighted_matrix(graphEdges, V)

#         # test bfs approach
#         startBfs = time.time()
#         mySolutionBfs = flow_function(graphMatrix, source, target, get_parents_bfs)
#         endBfs = time.time()
#         timeElapsedBfs = endBfs - startBfs

#         # test dfs approach
#         startDfs = time.time()
#         mySolutionDfs = flow_function(graphMatrix, source, target, get_parents_dfs)
#         endDfs = time.time()
#         timeElapsedDfs = endDfs - startDfs

#         solution = int(dimacs.readSolution(pathToFile))

#         testStatusMessage = "PASSED"
#         if solution == mySolutionBfs == mySolutionDfs:
#             passed += 1
#         else:
#             testStatusMessage = "FAILED"
#             failed += 1

#         print(f"correct solution: {solution}")
#         print(f"my solution bfs: {mySolutionBfs}")
#         print(f"time (BFS): {timeElapsedBfs:.3f} [s]")
#         print(f"my solution dfs: {mySolutionDfs}")
#         print(f"time (DFS): {timeElapsedDfs:.3f} [s]")
#         print()
#         print(f"test status: {testStatusMessage}")

#         total += 1

#     print("\nsummarize:")
#     print(f"passed: {passed}/{total}")
#     print(f"failed: {failed}/{total}")

def test():
    graphsDir = "./flow"
    myTest = Test(graphsDir, dimacs.loadDirectedWeightedGraph, dimacs.readSolution, ut.edges_to_directed_weighted_matrix, ford_fulkerson_for_test, 0, get_parents_bfs)
    myTest.test_function()

if __name__ == "__main__":
    graphsDir = "./flow"
    # test_function(ford_fulkerson)
    test()
