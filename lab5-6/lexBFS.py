from graph import Node

def get_first_set_element(setStruct: set):
    return next(iter(setStruct))

def lex_BFS(graph: list[Node], V: int, source: int):
    visitOrder = []
    visitedSet = set()

    verticisSet = set(range(1, V + 1))
    verticisSet.remove(source)
    toCheck = [verticisSet, {source}]

    while toCheck:
        vertex = get_first_set_element(toCheck[-1])

        toCheck[-1].remove(vertex)

        # check if last set is empty
        if not toCheck[-1]:
            toCheck.pop()

        neighbours = graph[vertex].neighbours

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
