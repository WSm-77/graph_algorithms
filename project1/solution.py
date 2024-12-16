from data import runtests
import sys

sys.setrecursionlimit(10_000)

class POECheck:
    def __init__(self, lexOrder: list, graph: dict[int, set[int]]):
        self.lexOrder = lexOrder
        self.lexSmallerNeighbors = {lexOrder[0] : set()}
        self.parents = {lexOrder[0] : lexOrder[0]}

        visitedSet = {lexOrder[0]}

        n = len(lexOrder)

        for idx in range(1, n):
            vertex = lexOrder[idx]

            self.lexSmallerNeighbors[vertex] = visitedSet & graph[vertex]

            visitedSet.add(vertex)

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

    return lordsRoutesLengths, vertexProtectors

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

def does_create_clique(lordsList, nonColisionGraph):
    lordsCnt = len(lordsList)

    for firstIdx in range(lordsCnt):
        firstLord = lordsList[firstIdx]
        for secondIdx in range(firstIdx + 1, lordsCnt):
            secondLord = lordsList[secondIdx]

            if secondLord not in nonColisionGraph[firstLord]:
                return False

    return True

def get_max_protected_route_length_brute_force(lordsRoutesLengths, nonColisionGraph):
    lordsCnt = len(nonColisionGraph)

    maxProtectedRouteLength = 0

    for number in range(1, 2 ** lordsCnt):
        lordsList = []

        numberCp = number

        for lordID in range(lordsCnt):
            if numberCp % 2 == 1:
                lordsList.append(lordID)

            numberCp >>= 1

        if does_create_clique(lordsList, nonColisionGraph):
            currentRouteLenght = 0

            for lordID in lordsList:
                currentRouteLenght += lordsRoutesLengths[lordID]

            maxProtectedRouteLength = max(maxProtectedRouteLength, currentRouteLenght)

    return maxProtectedRouteLength

def get_pivot(verticies: set, graph: dict[int, set[int]]):
    maxDegree = -1
    pivot = None
    for vertex in verticies:
        degree = len(graph[vertex])
        if maxDegree < degree:
            maxDegree  = degree
            pivot = vertex

    return pivot

def bron_kerbosch(graph: dict[int, set[int]]):
    def backtrack(clique, remaining, excluded):
        nonlocal maxCliques, graph
        if not remaining and not excluded:
            maxCliques.append(clique)
            return

        if not remaining:
            return

        pivot = get_pivot(remaining, graph)
        pivotNeighbours = graph[pivot]
        disjointRemaining = remaining - pivotNeighbours

        for vertex in disjointRemaining:
            neighbours = graph[vertex]
            backtrack(clique | {vertex}, remaining & neighbours, excluded & neighbours)
            remaining = remaining - {vertex}
            excluded = excluded | {vertex}

    maxCliques = []

    backtrack(set(), set(graph.keys()), set())

    return maxCliques

def get_first_set_element(setStruct: set):
    return next(iter(setStruct))

def lex_BFS(graph: dict[int, set[int]], V: int, source: int = 0):
    visitOrder = []
    visitedSet = set()

    verticisSet = set(range(V))
    verticisSet.remove(source)
    toCheck = [verticisSet, {source}]

    while toCheck:
        vertex = get_first_set_element(toCheck[-1])

        toCheck[-1].remove(vertex)

        # check if last set is empty
        if not toCheck[-1]:
            toCheck.pop()

        neighbours = graph[vertex]

        visitOrder.append(vertex)
        visitedSet.add(vertex)

        newToCheck = []

        for toCheckSet in toCheck:
            vertexNeighboursIntersection = toCheckSet & neighbours
            remaining = toCheckSet - vertexNeighboursIntersection
            if remaining:
                newToCheck.append(remaining)

            if vertexNeighboursIntersection:
                newToCheck.append(vertexNeighboursIntersection)

        toCheck = newToCheck

    return visitOrder

def find_independent_set_with_max_weight(lordsColisionGraph: dict[int, set[int]], lordsPathLengths: dict[int, int]):
    V = len(lordsColisionGraph)

    lexOrder = lex_BFS(lordsColisionGraph, V)

    poeCheck = POECheck(lexOrder, lordsColisionGraph)

    BLUE = 0
    RED = 1

    colours = {lordID : None for lordID in lordsColisionGraph.keys()}
    weightsCopy = {key : value for key, value in lordsPathLengths.items()}

    for lordID in reversed(lexOrder):
        if weightsCopy[lordID] <= 0:
            weightsCopy[lordID] = 0
            continue

        colours[lordID] = RED

        for lexSmallerNeighbour in poeCheck.lexSmallerNeighbors[lordID]:
            weightsCopy[lexSmallerNeighbour] -= weightsCopy[lordID]
            if weightsCopy[lexSmallerNeighbour] < 0:
                weightsCopy[lexSmallerNeighbour] = 0

        weightsCopy[lordID] = 0

    blueVertices = set()

    for lordID in lexOrder:
        if colours[lordID] != RED:
            continue

        hasBlueNeighbours = False

        for neighbour in lordsColisionGraph[lordID]:
            if neighbour in blueVertices:
                hasBlueNeighbours = True
                break

        if not hasBlueNeighbours:
            colours[lordID] = BLUE
            blueVertices.add(lordID)

    return blueVertices

def solve(V: int, streets: list[tuple[int, int, int]], lords: list[int]):
    lordsCnt = len(lords)

    royalRouteEdges = get_mst(V, streets)

    royalRouteGraph = get_adjustancy_list_graph(V, royalRouteEdges)

    lordsRoutesLengths, vertexProtectors = lords_protection(royalRouteEdges, royalRouteGraph, lords)

    colisionGraph = get_coliding_lords_graph(V, lordsCnt, vertexProtectors)

    heaviestIndependentSet = find_independent_set_with_max_weight(colisionGraph, lordsRoutesLengths)

    maxSum = 0

    for lordID in heaviestIndependentSet:
        maxSum += lordsRoutesLengths[lordID]

    return maxSum

runtests(solve)
