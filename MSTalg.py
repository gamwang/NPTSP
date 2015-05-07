import util
from collections import deque

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
             if (node != i) and(node not in visited):
                 edges.append((dist, i, node, graph.colors[i]))
        minimum_spanning_tree = set()
        edges.sort()
    for edge in edges:
        weight, vertice1, vertice2, color = edge
        if find(vertice1) != find(vertice2):
            union(vertice1, vertice2)
            minimum_spanning_tree.add(edge)
    return minimum_spanning_tree

def createPath(graph, edges):
    edges = sorted(list(edges), key = lambda x: x[1])
    length = len(edges)
    for e in range(length):
        edges.append((edges[e][0], edges[e][2], edges[e][1], edges[e][3]))
    visited = []
    path = []

    stack = []
    for e in range(len(edges)):
        if (edges[e][1] == 0 or edges[e][2] == 0):
            stack.append(edges[e])
    visited = [0]
    path = [(0, graph.colors[0])]

    while len(stack) > 0:
        edge = stack.pop()
        if edge[1] in visited and edge[2] in visited:
            continue
        if edge[1] not in visited:
            v = edge[1]
        elif edge[2] not in visited:
            v = edge[2]
    for e in range(len(edges)):
        if (edges[e][1] == v or edges[e][2] == v):
            stack.append(edges[e])
    visited.append(v)
    path.append((v, graph.colors[v]))
    return path
				
if __name__ == "__main__":
    T = 1 # number of test cases
    #fout = open ("answer.out", "w")
    for t in xrange(1, 2):
        fin = open("JonIsTrash" + str(t) + ".in", "r")
        N = int(fin.readline())
        d = [[] for i in range(N)]
        for i in xrange(N):
            d[i] = [int(x) for x in fin.readline().split()]
        c = fin.readline()

        graph = util.Graph(N, d, c)

        result = MSTalg(graph)
        result = createPath(graph, result)
        print "Edges:"
        stuff = sorted(edges, key=lambda x: x[1])
        for x in range(len(stuff)):
            print stuff[x]
        print "Result:"
        length = 0
        prev = -1
        for x in range(len(result)):
            if prev >= 0:
                length += graph.edges[prev][result[x][0]]
            prev = result[x][0]
            print result[x]
        print "Length: " + str(length)

        # find an answer, and put into assign
    #    assign = [0] * N
    #    for i in xrange(N):
    #        assign[i] = i+1
    #
    #    fout.write("%s\n" % " ".join(map(str, assign)))
    #fout.close()
