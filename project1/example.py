from data import runtests

class FindUnion:
    def __init__(self, V) -> None:
        self.representants = {vertex : vertex for vertex in range(1, V + 1)}
        self.levels = {vertex : 0 for vertex in range(1, V + 1)}

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

def lords_protection(royalRouteEdges: list[tuple[int, int, int]], royalRouteGraph: dict[int, set[int]], lords: list[int]):
    def dfs_visit(vertex):
        nonlocal lordID, lordCities, royalRouteGraph, visitedIDs

        visitedIDs[vertex] = lordID

        isOnLordsRoute = False

        for neighbour in royalRouteGraph[vertex]:
            if visitedIDs[neighbour] == lordID:
                continue

            # check if edge (vertex, neighbour) is protected by current lord
            if dfs_visit(neighbour):
                isOnLordsRoute = True

                orderedStreetTuple = (min_max(vertex, neighbour))
                weight = streetObjects[orderedStreetTuple]
                lordsRoutesLengths[lordID] += weight

        if vertex in lordCities:
            isOnLordsRoute = True

        if isOnLordsRoute:
            vertexProtectors[vertex].append(lordID)

        return isOnLordsRoute
    # end def

    V = len(royalRouteGraph)

    streetObjects = {(vertex, neighbour) : weight for vertex, neighbour, weight in royalRouteEdges}

    vertexProtectors = {vertex : [] for vertex in range(1, V + 1)}
    lordsRoutesLengths = {}

    visitedIDs = {vertex : None for vertex in range(1, V + 1)}

    for lordID, lordCities in enumerate(lords):
        startCity = lordCities[0]
        lordsRoutesLengths[lordID] = 0
        lordCities = set(lordCities)

        dfs_visit(startCity)

    return streetObjects, lordsRoutesLengths, vertexProtectors

def get_non_coliding_lords_graph(colisionGraph: dict[int, set[int]], lordsCnt):
    lordsSet = {lordID for lordID in range(lordsCnt)}

    noColisionsGraph = {}

    for vertex in colisionGraph.keys():
        noColisionsGraph[vertex] = lordsSet - colisionGraph[vertex] - {vertex}

    return noColisionsGraph

def get_coliding_lords_graph(V, lordsCnt, vertexProtectors):
    colisionsGraph = {lordID : set() for lordID in range(lordsCnt)}

    for vertex in range(1, V + 1):
        colidingLordsList = vertexProtectors[vertex]

        numberOfColidingLords = len(colidingLordsList)

        for firstLordIdx in range(numberOfColidingLords):
            firstLordID = colidingLordsList[firstLordIdx]
            for secondLordIdx in range(firstLordIdx + 1, numberOfColidingLords):
                secondLordID = colidingLordsList[secondLordIdx]
                colisionsGraph[firstLordID].add(secondLordID)
                colisionsGraph[secondLordID].add(firstLordID)

    return colisionsGraph

def get_max_cliques(nonColisionGraph: dict[int, set[int]]):
    maxCliquesList: list[set[int]] = []
    potentialCliques: list[tuple[set[int], set[int]]] = []

    for lordID in nonColisionGraph.keys():
        toDeleteIndicies = []

        neighbourLordsSet = nonColisionGraph[lordID]

        if not neighbourLordsSet:
            maxCliquesList.append({lordID})
            continue

        for idx in range(len(potentialCliques)):

            superVertex, potentialLordsInSuperVertex = potentialCliques[idx]

            if lordID in potentialLordsInSuperVertex:
                neighbourLordsIntersection = potentialLordsInSuperVertex & neighbourLordsSet
                remainingNeighbourLords = potentialLordsInSuperVertex - neighbourLordsIntersection - {lordID}

                # add current lord to super vertex
                extendedSuperVertex = superVertex | {lordID}

                if neighbourLordsIntersection:
                    potentialCliques[idx] = (extendedSuperVertex, neighbourLordsIntersection)
                else:
                    maxCliquesList.append(extendedSuperVertex)
                    toDeleteIndicies.append(idx)

                if remainingNeighbourLords:
                    potentialCliques.append((superVertex, remainingNeighbourLords))

        neighbourLordsSet = neighbourLordsSet - {checkedLordID for checkedLordID in range(lordID)}

        if neighbourLordsSet:
            potentialCliques.append(({lordID}, neighbourLordsSet))

        # remove finished cliques
        deletedCnt = 0
        for toDeleteInOriginalListIdx in toDeleteIndicies:
            toDeleteIndex = toDeleteInOriginalListIdx - deletedCnt

            del potentialCliques[toDeleteIndex]
            deletedCnt += 1

    return maxCliquesList

def solve(V: int, streets: list[tuple[int, int, int]], lords: list[int]):
    lordsCnt = len(lords)

    royalRouteEdges = get_mst(V, streets)

    print(streets)

    royalRouteGraph = get_adjustancy_list_graph(V, royalRouteEdges)

    print(royalRouteGraph)

    streetObjects, lordsRoutesLengths, vertexProtectors = lords_protection(royalRouteEdges, royalRouteGraph, lords)

    print(lordsRoutesLengths)
    print(streetObjects)
    print(vertexProtectors)

    colisionGraph = get_coliding_lords_graph(V, lordsCnt, vertexProtectors)

    print(colisionGraph)

    nonColisionGraph = get_non_coliding_lords_graph(colisionGraph, lordsCnt)

    print(nonColisionGraph)

    maxCliques = get_max_cliques(nonColisionGraph)

    print(maxCliques)

    maxSum = 0
    for maxClique in maxCliques:
        currentSum = 0
        for lordID in maxClique:
            currentSum += lordsRoutesLengths[lordID]

        maxSum = max(maxSum, currentSum)

    return maxSum

result = solve(6, [
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

print(result)

# runtests(solve)
