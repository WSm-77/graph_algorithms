import unittest
import os
import json
from utils import utils
from example import get_adjustancy_list_graph, get_mst, lords_protection

class LordsProtection(unittest.TestCase):
    def setUp(self):
        testCasesDir = "test_cases"
        graphName = "graph1.json"
        fileName = os.path.join(testCasesDir, graphName)

        with open(fileName, "r") as file:
            data = json.load(file)

        self.V = data["V"]
        self.streets = data["streets"]
        self.lords = data["lords"]
        self.royalRouteEdges = data["royalRouteEdges"]

        print(self.V)
        print(self.streets)
        print(self.lords)
        print(self.royalRouteEdges)

    def test_lords_protection(self):
        # given
        exceptedVerticiesProtectors = {1: [0], 2: [0, 1], 3: [0, 1], 4: [1, 2], 5: [1, 2], 6: [2]}

        # when
        royalRouteEdges = get_mst(self.V, self.streets)

        actualVerticiesProtectors = lords_protection(royalRouteEdges, get_adjustancy_list_graph(self.V, royalRouteEdges), self.lords)[2]

        # then
        self.assertEqual(actualVerticiesProtectors, exceptedVerticiesProtectors)

if __name__ == "__main__":
    unittest.main()
