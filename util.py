"""
Graph class, takes number of cities, edges listed as an adjacency matrix, and the colors of each node.  We can find a node which returns the color and the edges of a node n returned as a tuple
"""
        
class Graph(object):
    def __init__(self, numCities, edges, colors):
        self.numCities = numCities
        self.edges = edges
        self.colors = []
        for c in range(len(colors)):
            self.colors.append(colors[c])
        
    def findNode(self, n):
        return (self.colors[n], self.edges[n])

    def smallestBlueEdge(self, n1):
        dist = 1000
        for v in range(len(self.edges[n1])):
            if v != n1 and self.colors[v] == "B":
                if dist > self.edges[n1][v]:
                    dist = self.edges[n1][v]
                    blueEdge = (n1, v, dist)
        return blueEdge
    
    def smallestRedEdge(self, n1):
        dist = 1000
        for v in range(len(self.edges[n1])):
            if v != n1 and self.colors[v] == "R":
                if dist > self.edges[n1][v]:
                    dist = self.edges[n1][v]
                    redEdge = (n1, v, dist)
        return redEdge
def checkPath(graph, path):  
    temp = list(path)
    curr = temp[0][0]
    color = graph.colors[curr]
    colorCities = [(curr, color)]
    count = 1
    while len(temp) > 0:
        nextEdge = -1
        for e in temp:
            if e[0] == curr or e[1] == curr:
                nextEdge = e
                break
        if nextEdge == -1:
            return False
        elif nextEdge[0] == curr:
            curr = nextEdge[1]
            temp.remove(nextEdge)
        else:
            curr = nextEdge[0]
            temp.remove(nextEdge)
            
        if color == graph.colors[curr] and count == 3:
            return False
        elif color == graph.colors[curr]:
            colorCities.append((curr, color))
            count += 1
        else:
            color = graph.colors[curr]
            colorCities = [(curr, color)]
            count = 1
            
    return True

def getCost(graph, path):
    length = 0
    prev = -1
    for x in range(len(path)):
        if prev >= 0:
            length += graph.edges[prev][path[x][0]]
        prev = path[x][0]
    return length

def frontColor(graph, path, v):
    if len(path) < 4: return False
    return graph.colors[path[0][0]] == graph.colors[path[1][0]] and graph.colors[path[1][0]] == graph.colors[path[2][0]] and graph.colors[path[0][0]] == graph.colors[v]

def backColor(graph, path, v):
    if len(path) < 4: return False
    return graph.colors[path[-1][0]] == graph.colors[path[-2][0]] and graph.colors[path[-2][0]] == graph.colors[path[-3][0]] and graph.colors[path[-1][0]] == graph.colors[v]

def isEdge(path, edge):
    head = path[0]
    tail = path[-1]
    return head in [edge[1], edge[2]] or tail in [edge[1], edge[2]]
