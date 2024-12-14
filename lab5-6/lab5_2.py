from graph import Node, create_graph
from lexBFS import lex_BFS
from POECheck import POECheck
from utils.test import Test
import dimacs

def get_first_set_element(setStruct: set):
    return next(iter(setStruct))

def find_max_clique_size(graph: list[Node], V: int, source: int = 1):
    lexOrder = lex_BFS(graph, V, source)
    poeCheck = POECheck(lexOrder, graph)

    result = 0

    for vertex in lexOrder:
        lexSmallerNeighbours = poeCheck.lexSmallerNeighbors[vertex]

        result = max(result, len(lexSmallerNeighbours) + 1)

    return result

if __name__ == "__main__":
    graphsDir = "maxclique"
    myTest = Test(graphsDir, dimacs.loadDirectedWeightedGraph, dimacs.readSolution, create_graph, find_max_clique_size, 1)
    myTest.test_all()
