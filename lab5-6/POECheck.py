from graph import Node

class POECheck:
    def __init__(self, lexOrder: list, graph: list[Node]):
        self.lexSmallerNeighbors = {lexOrder[0] : set()}
        self.parents = {lexOrder[0] : lexOrder[0]}

        visitedSet = {lexOrder[0]}

        n = len(lexOrder)

        for idx in range(1, n):
            vertex = lexOrder[idx]

            self.lexSmallerNeighbors[vertex] = visitedSet & graph[vertex].neighbours

            potentialParentIdx = idx - 1
            while potentialParentIdx >= 0:
                potentialParent = lexOrder[potentialParentIdx]

                if potentialParent in self.lexSmallerNeighbors[vertex]:
                    self.parents[vertex] = potentialParent
                    break

                potentialParentIdx -= 1

            visitedSet.add(vertex)

