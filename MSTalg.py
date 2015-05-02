import util

parent = dict()
rank = dict()

def make_set(vertice):
    parent[vertice] = vertice
    rank[vertice] = 0

def find(vertice):
    if parent[vertice] != vertice:
        parent[vertice] = find(parent[vertice])
    return parent[vertice]

def union(vertice1, vertice2):
    root1 = find(vertice1)
    root2 = find(vertice2)
    if root1 != root2:
        if rank[root1] > rank[root2]:
            parent[root2] = root1
        else:
            parent[root1] = root2
            if rank[root1] == rank[root2]: rank[root2] += 1

def MSTalg(graph):
  edges = []
  visited = []
  for i in range(graph.numCities):
    make_set(i)
    visited.append(i)
    for node, dist in enumerate(graph.edges[i]):
      if (node != i) and (node not in visited):
        edges.append((dist, i, node))
    minimum_spanning_tree = set()
    edges.sort()
  for edge in edges:
        weight, vertice1, vertice2 = edge
        if find(vertice1) != find(vertice2):
            union(vertice1, vertice2)
            minimum_spanning_tree.add(edge)
  return minimum_spanning_tree

T = 1 # number of test cases
#fout = open ("answer.out", "w")
for t in xrange(1, T+1):
    fin = open(str(t) + ".in", "r")
    N = int(fin.readline())
    d = [[] for i in range(N)]
    for i in xrange(N):
        d[i] = [int(x) for x in fin.readline().split()]
    c = fin.readline()

    graph = util.Graph(N, d, c)

    result = MSTalg(graph)
    print result


    # find an answer, and put into assign
#    assign = [0] * N
#    for i in xrange(N):
#        assign[i] = i+1
#
#    fout.write("%s\n" % " ".join(map(str, assign)))
#fout.close()
