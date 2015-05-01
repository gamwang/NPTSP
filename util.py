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
