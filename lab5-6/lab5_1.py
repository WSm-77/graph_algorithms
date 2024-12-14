from graph import Node, create_graph
from lexBFS import lex_BFS
from POECheck import POECheck
from utils.test import Test
import dimacs

def get_first_set_element(setStruct: set):
    return next(iter(setStruct))

def is_chordal(graph: list[Node], V: int, source: int = 1):
    lexOrder = lex_BFS(graph, V, source)
    poeCheck = POECheck(lexOrder, graph)

    for vertex in range(2, V + 1):
        lexSmallerNeighbours = poeCheck.lexSmallerNeighbors[vertex]
        vertexParent = poeCheck.parents[vertex]
        parentLexSmallerNeighbours = poeCheck.lexSmallerNeighbors[vertexParent]

        if not lexSmallerNeighbours - {vertexParent} <= parentLexSmallerNeighbours:
            return False

    return True

if __name__ == "__main__":
    graphsDir = "chordal"
    myTest = Test(graphsDir, dimacs.loadDirectedWeightedGraph, lambda x: int(dimacs.readSolution(x)) != 0, create_graph, is_chordal, 1)
    myTest.test_all()
