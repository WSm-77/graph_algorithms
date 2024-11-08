import dimacs
import os
import sys
sys.path.insert(0, "../utils")
from test import Test
import time
from collections import deque



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

def edges_to_weighted_matrix(graphEdges, V):
    NO_EDGE = 0
    matrix = [[NO_EDGE for _ in range(V)] for _ in range(V)]

    for vertex, neighbour, weight in graphEdges:
        vertex -= 1
        neighbour -= 1
        matrix[vertex][neighbour] = weight
        matrix[neighbour][vertex] = weight

    return matrix

def min_cut(graphMatrix, V):
    V = len(graphMatrix)
    s = 0

    results = []

    cnt = 0

    for t in range(1, V):
        results.append(ford_fulkerson(graphMatrix, s, t, get_parents_bfs))
        cnt += 1
        print(f"{cnt}. min_cut")

    return min(results)

def test_graph(graphName: str, flow_function):
    pathToFile = os.path.join(graphsDir, graphName)
    V, graphEdges = dimacs.loadWeightedGraph(pathToFile)
    print(sorted(graphEdges))

    source = 0
    target = V - 1
    graphMatrix = edges_to_weighted_matrix(graphEdges, V)

    print(*graphMatrix, sep="\n")

    solution = int(dimacs.readSolution(pathToFile))

    print(solution)

    mySolution = flow_function(graphMatrix, source, target, get_parents_bfs)

    print(mySolution)

def test_function(flow_function):
    passed = 0
    failed = 0
    total = 0

    for fileName in os.listdir(graphsDir):
        print(f"\n\n######### {fileName} #########\n\n")

        pathToFile = os.path.join(graphsDir, fileName)
        V, graphEdges = dimacs.loadDirectedWeightedGraph(pathToFile)

        source = 0
        target = V - 1
        graphMatrix = edges_to_weighted_matrix(graphEdges, V)

        # test bfs approach
        startBfs = time.time()
        mySolutionBfs = flow_function(graphMatrix, source, target, get_parents_bfs)
        endBfs = time.time()
        timeElapsedBfs = endBfs - startBfs

        solution = int(dimacs.readSolution(pathToFile))

        testStatusMessage = "PASSED"
        if solution == mySolutionBfs:
            passed += 1
        else:
            testStatusMessage = "FAILED"
            failed += 1

        print(f"correct solution: {solution}")
        print(f"my solution bfs: {mySolutionBfs}")
        print(f"time (BFS): {timeElapsedBfs:.3f} [s]")
        print()
        print(f"test status: {testStatusMessage}")

        total += 1

    print("\nsummarize:")
    print(f"passed: {passed}/{total}")
    print(f"failed: {failed}/{total}")

def test():
    graphsDir = "./graphs"
    myTest = Test(graphsDir, dimacs.loadDirectedWeightedGraph, dimacs.readSolution, edges_to_weighted_matrix, min_cut)
    myTest.test_graph("cycle")
    myTest.test_function()


if __name__ == "__main__":
    graphsDir = "./graphs"
    # test_function(ford_fulkerson)
    # test_graph("cycle", min_cut)
    test()

