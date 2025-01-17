from utils.test import Test
import dimacs
import networkx as nx
from networkx.algorithms.planarity import check_planarity

def is_planar(graphEdges: list[tuple[int, int]], V: int):
    nxGraph = nx.Graph()
    nxGraph.add_edges_from(graphEdges)

    isPlanar, _ = check_planarity(nxGraph)

    return isPlanar

if __name__ == "__main__":
    graphsDir = "planarity"
    graph_convert_function = lambda x, y: [(v, n) for v, n, _ in x]
    myTest = Test(graphsDir, dimacs.loadDirectedWeightedGraph, dimacs.readSolution, graph_convert_function, is_planar)
    myTest.test_all()


