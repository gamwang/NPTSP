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

def createPath(graph, start):
    #preprocess
    visited = [start]
    path = [(start, graph.colors[start])]
    tmp = []
    for i, e in enumerate(graph.edges[start]):
        if i not in visited:
            tmp.append([e, start, i, graph.colors[i]])
    tmp = sorted(tmp, key=lambda x: x[0])
    tmp.reverse() 
    stack = []
    for item in tmp:
      stack.append(item)
    # Greedily find a path
    while len(stack) > 0:
        edge = stack.pop()
        if edge[1] in visited and edge[2] in visited and not isEdge(path, edge):
            continue
        if edge[1] not in visited:
            v = edge[1]
            u = edge[2]
        else:
            v = edge[2]
            u = edge[1]
        inserted = False
        # Choose whether the edge is for head or tail of the path
        flg = u == path[-1][0]
        if flg and not util.backColor(graph, path, v): 
            visited.append(v)
            path.append((v, graph.colors[v])) 
            inserted = True
        if not flg and not util.frontColor(graph, path, v) and not inserted: 
            visited.append(v)
            path.insert(0, (v, graph.colors[v])) 
            inserted = True
        if inserted:
            #print "path: ", path
            tmp = []
            for i, e in enumerate(graph.edges[path[-1][0]]):
                if i not in visited:
                    tmp.append([e, path[-1][0], i, graph.colors[i]])
            for i, e in enumerate(graph.edges[path[0][0]]):
                if i not in visited:
                    tmp.append([e, path[0][0], i, graph.colors[i]])
            tmp = sorted(tmp, key=lambda x: x[0])
            tmp.reverse() 
            stack = []
            for item in tmp:
              stack.append(item)
            #print "stack: ", stack
    return path

