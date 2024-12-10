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

        V = data["V"]
        streets = data["streets"]
        lords = data["lords"]
        royalRouteEdges = list(map(tuple, data["royalRouteEdges"]))
        verticiesProtectors = self.json_data_to_dict_graph(data["verticiesProtectors"], int)

        # print(V)
        # print(streets)
        # print(lords)
        # print(royalRouteEdges)
        # print(verticiesProtectors)

        # when
        royalRouteEdges = get_mst(V, streets)

        actualVerticiesProtectors = lords_protection(royalRouteEdges, get_adjustancy_list_graph(V, royalRouteEdges), lords)[1]

        # then
        self.assertEqual(royalRouteEdges, royalRouteEdges)
        self.assertEqual(actualVerticiesProtectors, verticiesProtectors)

if __name__ == "__main__":
    unittest.main()
