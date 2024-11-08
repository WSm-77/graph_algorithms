import sys
sys.path.insert(0, "../utils")
from test import Test
import dimacs


class FindUnion:
    def __init__(self, V) -> None:
        self.representants = {vertex : vertex for vertex in range(1, V+1)}
        self.levels = {vertex : 0 for vertex in range(1, V+1)}

    def find(self, vertex):
        if self.representants[vertex] != vertex:
            self.representants[vertex] = self.find(self.representants[vertex])
        return self.representants[vertex]

    def union(self, vertex1, vertex2):
        repr1 = self.find(vertex1)
        repr2 = self.find(vertex2)

        if repr1 == repr2:
            return

        if self.levels[repr1] > self.levels[repr2]:
            self.representants[repr2] = repr1
        else:
            self.representants[repr1] = repr2
            if self.levels[repr1] == self.levels[repr2]:
                self.levels[repr2] += 1

def tour_guide_find_union(graphEdges, V, source, target):
    graphEdges.sort(key=lambda x: x[2], reverse=True)

    findUnion = FindUnion(V)

    result = None
    for vertex, neighbour, cost in graphEdges:
        findUnion.union(vertex, neighbour)
        if findUnion.find(source) == findUnion.find(target):
            result = cost
            break

    return result

if __name__ == "__main__":
    graphsDir = "./graphs"
    myTest = Test(graphsDir, dimacs.loadWeightedGraph, dimacs.readSolution, lambda x, y: x, tour_guide_find_union, 1, 2)
    myTest.test_function()

