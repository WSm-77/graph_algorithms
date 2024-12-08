from data import runtests

class FindUnion:
    def __init__(self, V) -> None:
        self.representants = {vertex : vertex for vertex in range(1, V+1)}
        self.levels = {vertex : 0 for vertex in range(1, V+1)}

    def find(self, vertex):
        if self.representants[vertex] != vertex:
            self.representants[vertex] = self.find(self.representants[vertex])
        return self.representants[vertex]

    def union(self, vertex1, vertex2) -> bool:
        repr1 = self.find(vertex1)
        repr2 = self.find(vertex2)

        if repr1 == repr2:
            return False

        if self.levels[repr1] > self.levels[repr2]:
            self.representants[repr2] = repr1
        else:
            self.representants[repr1] = repr2
            if self.levels[repr1] == self.levels[repr2]:
                self.levels[repr2] += 1

        return True

def min_max(val1, val2):
    if val2 < val1:
        val1, val2 = val2, val1
    return val1, val2

def get_adjustancy_list_graph(V: int, graphEdges: list[tuple[int, int, int]]) -> dict[int, set[int]]:
    graph = {vertex : set() for vertex in range(1, V + 1)}

    for vertex, neighbour, weight in graphEdges:
        graph[vertex].add(neighbour)
        graph[neighbour].add(vertex)

    return graph

def get_mst(V: int, graphEdges: list[tuple[int, int, int]]) -> list[tuple[int, int, int]]:
    """
    Get Minimal Spanning Tree of given graph

    :param V: number of verticies in graph
    :param graphEdges: graph representation as list of edges
    :returns: Minimal Spanning Tree graph representation as list of edges
    """
    unionStruct = FindUnion(V)

    graphEdges.sort(key = lambda x: x[2])

    mstEdges = []

    # number of edges in MST
    edgesLeft = V - 1

    for vertex, neighbour, weight in graphEdges:
        # check if current edge can be added to MST
        if unionStruct.union(vertex, neighbour):
            # make sure that vertex < neighbour
            vertex, neighbour = min_max(vertex, neighbour)

            mstEdges.append((vertex, neighbour, weight))
            edgesLeft -= 1

            # check if MST is already created
            if edgesLeft == 0:
                break

    return mstEdges

def solve(V: int, streets: list[tuple[int, int, int]], lords: list[int]):
    royalRouteEdges = get_mst(V, streets)

    print(streets)

    royalRouteGraph = get_adjustancy_list_graph(V, royalRouteEdges)

    print(royalRouteGraph)

solve(6, [
    (1, 2, 4),
    (2, 3, 5),
    (3, 4, 6),
    (4, 5, 8),
    (5, 6, 7),
    (1, 6, 9),
    (2, 5, 10)],
  [
    [1, 3],
    [2, 5],
    [4, 6]])

# runtests(solve)