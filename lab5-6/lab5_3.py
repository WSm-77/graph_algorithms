from graph import Node, create_graph
from lexBFS import lex_BFS
from utils.test import Test
import dimacs

def min_value_gt_zero_not_in_used(used: set):
    value = 1

    while value in used:
        value += 1

    return value

def find_chromatic_number(graph: list[Node], V: int, source: int = 1):
    lexOrder = lex_BFS(graph, V, source)

    chromaticNumber = 0

    color = {vertex : 0 for vertex in range(1, V + 1)}

    for vertex in lexOrder:
        neighbours: set = graph[vertex].neighbours

        used = {color[neighbour] for neighbour in neighbours}

        color[vertex] = min_value_gt_zero_not_in_used(used)

        chromaticNumber = max(chromaticNumber, color[vertex])

    return chromaticNumber

if __name__ == "__main__":
    graphsDir = "coloring"
    myTest = Test(graphsDir, dimacs.loadDirectedWeightedGraph, dimacs.readSolution, create_graph, find_chromatic_number, 1)
    myTest.test_all()
