from graph import Node, create_graph

def get_first_set_element(setStruct: set):
    return next(iter(setStruct))

def lex_BFS(graph: list[Node], soruce: int):
    V = len(graph) - 1

    visitOrder = []

    verticisSet = set(range(1, V + 1))
    verticisSet.remove(source)
    predecessorList = [verticisSet, {source}]

    while predecessorList:
        vertex = get_first_set_element(predecessorList[-1])

        visitOrder.append(vertex)



    return predecessorList

if __name__ == "__main__":
    V = 8
    source = 1
    graphEdges = [(1, 6, 1), (3, 6, 1), (8, 6, 1), (6, 7, 1), (7, 8, 1), (3, 8, 1), (2, 8, 1), (5, 8, 1), (4, 8, 1), (4, 7, 1), (5, 7, 1)]
    graphListOfNodes = create_graph(V, graphEdges)
    result = lex_BFS(graphListOfNodes, 1)
    print(result)
