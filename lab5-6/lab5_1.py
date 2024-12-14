from graph import Node, create_graph
from utils.test import Test
import dimacs

def get_first_set_element(setStruct: set):
    return next(iter(setStruct))

def is_chordal(graph: list[Node], V: int, source: int):
    visitOrder = []
    visitedSet = set()

    verticisSet = set(range(1, V + 1))
    verticisSet.remove(source)
    toCheck = [verticisSet, {source}]

    vertexParent = None
    parentLexSmallerNeighbours = set()

    while toCheck:
        vertex = get_first_set_element(toCheck[-1])

        toCheck[-1].remove(vertex)

        # check if last set is empty
        if not toCheck[-1]:
            toCheck.pop()


        neighbours = graph[vertex].neighbours
        lexSmallerNeighbours = visitedSet & neighbours

        print("##################")
        print()
        print(vertex)
        print(lexSmallerNeighbours)
        print()
        print(vertexParent)
        print(parentLexSmallerNeighbours)
        print()

        if not lexSmallerNeighbours - {vertexParent} <= parentLexSmallerNeighbours:
            return False

        visitOrder.append(vertex)
        visitedSet.add(vertex)

        newToCheck = []

        for toCheckSet in toCheck:
            vertexNeighboursIntersection = toCheckSet & neighbours
            remaining = toCheckSet - vertexNeighboursIntersection
            if remaining:
                newToCheck.append(remaining)

            if vertexNeighboursIntersection:
                newToCheck.append(vertexNeighboursIntersection)

        toCheck = newToCheck
        vertexParent = vertex
        parentLexSmallerNeighbours = lexSmallerNeighbours

    return True

if __name__ == "__main__":
    # V = 8
    # source = 1
    # graphEdges = [(1, 6, 1), (3, 6, 1), (8, 6, 1), (6, 7, 1), (7, 8, 1), (3, 8, 1), (2, 8, 1), (5, 8, 1), (4, 8, 1), (4, 7, 1), (5, 7, 1)]
    # graphListOfNodes = create_graph(graphEdges, V)

    # result = is_chordal(graphListOfNodes, V, source)

    # print(result)

    graphsDir = "chordal"
    myTest = Test(graphsDir, dimacs.loadDirectedWeightedGraph, lambda x: dimacs.readSolution(x) != 0, create_graph, is_chordal, 1)
    graphName = "AT"
    myTest.test_graph(graphName)
