class Node:
  def __init__(self, idx):
    self.idx = idx
    self.neighbours = set()              # zbiór sąsiadów

  def connect_to(self, v):
    self.neighbours.add(v)

def create_graph(edgesList, V):
    G: list[Node] = [None] + [Node(i) for i in range(1, V+1)]  # żeby móc indeksować numerem wierzchołka

    for (u, v, _) in edgesList:
        G[u].connect_to(v)
        G[v].connect_to(u)

    return G
