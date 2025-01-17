from utils.test import Test
import dimacs
import networkx as nx
from networkx.algorithms.flow import maximum_flow

def max_flow(graphEdges: list[tuple[int, int, int]], V: int, source: int):
    target = V
    nxGraph = nx.DiGraph()

    for vertex, neighbour, weight in graphEdges:
        nxGraph.add_edge(vertex, neighbour)

        nxGraph[vertex][neighbour]['capacity'] = weight

    maxFlow, _ = maximum_flow(nxGraph, source, target)

    return maxFlow

if __name__ == "__main__":
    graphsDir = "flow"
    graph_convert_function = lambda x, y: x
    myTest = Test(graphsDir, dimacs.loadDirectedWeightedGraph, dimacs.readSolution, graph_convert_function, max_flow, 1)
    myTest.test_all()


