from graph import Node, create_graph
from lexBFS import lex_BFS
from utils.test import Test
import dimacs

class POECheck:
    def __init__(self, lexOrder: list, graph: list[Node]):
        self.lexSmallerNeighbors = {lexOrder[0] : set()}
        self.parents = {lexOrder[0] : None}

        visitedSet = {lexOrder[0]}

        n = len(lexOrder)

        for idx in range(1, n):
            vertex = lexOrder[idx]

            self.lexSmallerNeighbors[vertex] = visitedSet & graph[vertex].neighbours

            potentialParentIdx = idx - 1
            while potentialParentIdx >= 0:
                potentialParent = lexOrder[potentialParentIdx]

                if potentialParent in self.lexSmallerNeighbors[vertex]:
                    self.parents[vertex] = potentialParent
                    break

                potentialParentIdx -= 1

            visitedSet.add(vertex)



def get_first_set_element(setStruct: set):
    return next(iter(setStruct))

def is_chordal(graph: list[Node], V: int, source: int = 1):
    lexOrder = lex_BFS(graph, V, source)
    poeCheck = POECheck(lexOrder, graph)

    print(poeCheck.lexSmallerNeighbors)
    print(poeCheck.parents)

    # return

    for vertex in range(2, V + 1):
        lexSmallerNeighbours = poeCheck.lexSmallerNeighbors[vertex]
        vertexParent = poeCheck.parents[vertex]
        parentLexSmallerNeighbours = poeCheck.lexSmallerNeighbors[vertexParent]

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
    myTest.test_all()
