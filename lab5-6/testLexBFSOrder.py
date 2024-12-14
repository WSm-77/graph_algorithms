import unittest
import os
from dimacs import loadWeightedGraph
from graph import create_graph
from lexBFS import lex_BFS
from utils.lexBFSChecker import check_lex_BFS

class LexBFS(unittest.TestCase):
    def test_single_graph_lex_BFS_order(self):
        # given
        graphsDir = "chordal"
        graphName = "AT"
        V, graphEdges = loadWeightedGraph(os.path.join(graphsDir, graphName))
        graph = create_graph(V, graphEdges)

        # when
        order = lex_BFS(graph, V, 1)

        # then
        self.assertTrue(check_lex_BFS(graph, order))

    def test_all_graphs_lex_BFS_order(self):
        # given
        graphsDir = "chordal"

        cnt = 0
        for graphName in os.listdir(graphsDir):
            V, graphEdges = loadWeightedGraph(os.path.join(graphsDir, graphName))
            graph = create_graph(V, graphEdges)

            # when
            order = lex_BFS(graph, V, 1)

            # then
            self.assertTrue(check_lex_BFS(graph, order))

if __name__ == "__main__":
    unittest.main()
