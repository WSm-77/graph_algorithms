import unittest
import os
import json
from example import get_adjustancy_list_graph, get_mst, lords_protection

class LordsProtection(unittest.TestCase):
    def json_data_to_dict_graph(self, jsonDataGraph: dict[str, list[int]], convertKeys = lambda x: x, convertValues = lambda x: x):
        return {convertKeys(key) : convertValues(value) for key, value in jsonDataGraph.items()}

    def test_lords_protection(self):
        # given
        testCasesDir = "test_cases"
        graphName = "graph1.json"
        fileName = os.path.join(testCasesDir, graphName)

        with open(fileName, "r") as file:
            data = json.load(file)

        self.V = data["V"]
        self.streets = data["streets"]
        self.lords = data["lords"]
        self.royalRouteEdges = list(map(tuple, data["royalRouteEdges"]))
        self.verticiesProtectors = self.json_data_to_dict_graph(data["verticiesProtectors"], int)

        print(self.V)
        print(self.streets)
        print(self.lords)
        print(self.royalRouteEdges)
        print(self.verticiesProtectors)

        # when
        royalRouteEdges = get_mst(self.V, self.streets)

        actualVerticiesProtectors = lords_protection(royalRouteEdges, get_adjustancy_list_graph(self.V, royalRouteEdges), self.lords)[1]

        # then
        self.assertEqual(royalRouteEdges, self.royalRouteEdges)
        self.assertEqual(actualVerticiesProtectors, self.verticiesProtectors)

if __name__ == "__main__":
    unittest.main()
