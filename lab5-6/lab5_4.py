from graph import Node, create_graph
from lexBFS import lex_BFS
from utils.test import Test
import dimacs

def vertex_cover(graph: list[Node], V: int, source: int = 1):
    lexOrder = lex_BFS(graph, V, source)

    lexOrder.reverse()

    independentSet = set()

    for vertex in lexOrder:
        neighbours = graph[vertex].neighbours

        independentSetIntersection = neighbours & independentSet

        if not independentSetIntersection:
            independentSet.add(vertex)

    return len({vertex for vertex in range(1, V + 1)} - independentSet)

if __name__ == "__main__":
    graphsDir = "vcover"
    myTest = Test(graphsDir, dimacs.loadDirectedWeightedGraph, dimacs.readSolution, create_graph, vertex_cover, 1)
    myTest.test_all()
