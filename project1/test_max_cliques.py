import unittest
import os
import json
from example import get_non_coliding_lords_graph, bron_kerbosch

class MaxClique(unittest.TestCase):
    def json_data_to_dict_graph(self, jsonDataGraph: dict[str, list[int]], convertKeys = lambda x: x, convertValues = lambda x: x):
        return {convertKeys(key) : convertValues(value) for key, value in jsonDataGraph.items()}

    def test_max_cliques1(self):
        # given
        testCasesDir = "test_cases"
        graphName = "colidingGraph1.json"
        fileName = os.path.join(testCasesDir, graphName)
        expected = [{0, 1, 2, 3}, {0, 1, 2, 4}, {3, 5}, {4, 5}]

        # when
        with open(fileName, "r") as file:
            data = json.load(file)

        colisionGraph = self.json_data_to_dict_graph(data["colisionGraph"], int, set)

        nonColisionGraph = get_non_coliding_lords_graph(colisionGraph, len(colisionGraph))

        # print(nonColisionGraph)

        # then
        maxCliques = bron_kerbosch(nonColisionGraph)
        self.assertEqual(len(maxCliques), len(expected))
        for superVertex in maxCliques:
            self.assertIn(superVertex, expected)

    def test_max_cliques2(self):
        # given
        testCasesDir = "test_cases"
        graphName = "colidingGraph2.json"
        fileName = os.path.join(testCasesDir, graphName)
        expected = [{0, 1, 2, 3, 4}, {3, 4, 5}]

        # when
        with open(fileName, "r") as file:
            data = json.load(file)

        colisionGraph = self.json_data_to_dict_graph(data["colisionGraph"], int, set)

        nonColisionGraph = get_non_coliding_lords_graph(colisionGraph, len(colisionGraph))

        # print(nonColisionGraph)

        maxCliques = bron_kerbosch(nonColisionGraph)

        # print(maxCliques)

        # then
        maxCliques = bron_kerbosch(nonColisionGraph)
        self.assertEqual(len(maxCliques), len(expected))
        for superVertex in maxCliques:
            self.assertIn(superVertex, expected)

    def test_max_cliques3(self):
        # given
        testCasesDir = "test_cases"
        graphName = "nonColidingGraph3.json"
        fileName = os.path.join(testCasesDir, graphName)
        expected = [{0, 1, 7}, {0, 6, 7}, {1, 2, 7}, {2, 3, 7}, {3, 4, 7}, {4, 5, 7}, {5, 6, 7}]

        # when
        with open(fileName, "r") as file:
            data = json.load(file)

        nonColisionGraph = self.json_data_to_dict_graph(data["colisionGraph"], int, set)

        # print(nonColisionGraph)

        maxCliques = bron_kerbosch(nonColisionGraph)

        # print(maxCliques)

        # then
        maxCliques = bron_kerbosch(nonColisionGraph)
        self.assertEqual(len(maxCliques), len(expected))
        for superVertex in maxCliques:
            self.assertIn(superVertex, expected)

if __name__ == "__main__":
    unittest.main()
