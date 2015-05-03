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