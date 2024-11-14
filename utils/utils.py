NO_EDGE = 0
INF = float("inf")

def edges_to_directed_weighted_matrix(graphEdges, V):
    matrix = [[NO_EDGE for _ in range(V)] for _ in range(V)]

    for vertex, neighbour, weight in graphEdges:
        vertex -= 1
        neighbour -= 1
        matrix[vertex][neighbour] = weight

    return matrix

def edges_to_weighted_matrix(graphEdges, V):
    matrix = [[NO_EDGE for _ in range(V)] for _ in range(V)]

    for vertex, neighbour, weight in graphEdges:
        vertex -= 1
        neighbour -= 1
        matrix[vertex][neighbour] = weight
        matrix[neighbour][vertex] = weight

    return matrix
