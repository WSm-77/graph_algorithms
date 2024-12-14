def check_lex_BFS(G, order):
  n = len(G)
  pi = [None] * n
  for i, v in enumerate(order):
    pi[v] = i

  for i in range(n-1):
    for j in range(i+1, n-1):
      Ni = G[order[i]].neighbours
      Nj = G[order[j]].neighbours

      verts = [pi[v] for v in Nj - Ni if pi[v] < i]
      if verts:
        viable = [pi[v] for v in Ni - Nj]
        if not viable or min(verts) <= min(viable):
          return False

  return True
