import random
import util

def createRandomPath(graph):
    currCity = random.randint(0, graph.numCities - 1)
    start = currCity
    edges = []
    notVisited = range(0, graph.numCities)
    notVisited.remove(currCity)
    color = graph.colors[currCity]
    while len(edges) < graph.numCities - 1:
        v = random.randint(0, len(notVisited) - 1)
        nextEdge = notVisited[v]
        if graph.colors[nextEdge] == color:
            continue
        else:
            color = graph.colors[nextEdge]
        if nextEdge in notVisited:
            edges.append((currCity, nextEdge, graph.edges[currCity][nextEdge], graph.colors[currCity], graph.colors[nextEdge]))
            currCity = nextEdge
            notVisited.remove(currCity)
    last = edges[graph.numCities - 2][1]
    edges.append((last, start, graph.edges[start][last], graph.colors[last], graph.colors[start]))
    return edges

def checkPath(graph, edges):  
    temp = list(edges)
    curr = temp[0][0]
    start = curr
    color = graph.colors[curr]
    count = 1
    lap = 0
    x = 0
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
        elif nextEdge[1] == curr:
            curr = nextEdge[0]
        if x < graph.numCities:
            x += 1
        else:
            lap = 1
        if lap == 1:
            temp.remove(nextEdge)
        if color == graph.colors[curr] and count >= 3:
            return False
        elif color == graph.colors[curr]:
            count += 1
        else:
            color = graph.colors[curr]
            count = 1
    return True

def switch2Edges(graph, edges, length):
    for i in range(graph.numCities):
        possible = []
        other = list(edges)
        for e in edges:
            if e[0] == i or e[1] == i:
                possible.append(e)
                other.remove(e)
        for edge1 in possible:
            for edge2 in other:
                newList = list(edges)
                newEdge1 = (edge1[0], edge2[1], graph.edges[edge1[0]][edge2[1]], graph.colors[edge1[0]], graph.colors[edge2[1]])
                newEdge2 = (edge1[1], edge2[0], graph.edges[edge1[1]][edge2[0]], graph.colors[edge1[1]], graph.colors[edge2[0]])
                newList.remove(edge1)
                newList.append(newEdge1)
                newList.remove(edge2)
                newList.append(newEdge2)
                
                if not checkPath(graph, newList):
                    newList = list(edges)
                    newEdge1 = (edge1[0], edge2[0], graph.edges[edge1[0]][edge2[0]], graph.colors[edge1[0]], graph.colors[edge2[0]])
                    newEdge2 = (edge1[1], edge2[1], graph.edges[edge1[1]][edge2[1]], graph.colors[edge1[1]], graph.colors[edge2[1]])

                    newList.remove(edge1)
                    newList.append(newEdge1)
                    newList.remove(edge2)
                    newList.append(newEdge2)
                    
                    if not checkPath(graph, newList):
                        continue
                newLength = sum([edge[2] for edge in newList])
                if newLength < length:
                    return (newList, newLength)
    return 0

def localSearch2(graph, edges):
    """asd"""
    length = sum([edge[2] for edge in edges])
    x = 0
    newPath = edges
    while True:
        count = 0
        result = switch2Edges(graph, edges, length)
        if result == 0:
            break
        else:
            newPath, newLength = result
            edges = newPath
            if newLength == length:
                break
            length = newLength
            count += 1
            x += 1
    
    if not checkPath(graph, newPath):
        print "error in path edges line 108"
    thing = list(edges)
    highest = 0
    edge = 0
    for e in edges:
        if e[2] >= highest:
            highest = e[2]
            edge = e
    edges.remove(edge)
    length -= highest
    
    curr = edge[0]
    path = [curr]
    while len(path) < graph.numCities:
        for e in edges:
            if e[0] == curr or e[1] == curr:
                nextEdge = e
                break
        if e[0] == curr:
            curr = e[1]
        else:
            curr = e[0]
        path.append(curr)
        edges.remove(nextEdge)
    return path, length, thing

def checkVertices(graph, path):
    color = 'a'
    count = 0
    seen = []
    for v in path:
        if v in seen:
            return False
        else:
            seen.append(v)
        #print str(v) + ", color: " + str(graph.colors[v])
        if color != graph.colors[v]:
            color = graph.colors[v]
            count = 1
        elif color == graph.colors[v] and count == 3:
            return False
        elif color == graph.colors[v]:
            count += 1
    return True
    

T = 1 # number of test cases
fout = open ("answer2.out", "w")
for t in xrange(240, 496):
    fin = open("instances/" + str(t) + ".in", "r")
    N = int(fin.readline())
    d = [[] for i in range(N)]
    for i in xrange(N):
        d[i] = [int(x) for x in fin.readline().split()]
    c = fin.readline()

    graph = util.Graph(N, d, c)
    
    print "Running on " + str(t) + ".in"
    print str(N) + " node graph"
    
    result = createRandomPath(graph)
    
#Test random path
    print "Random: " + str(checkPath(graph, result))

    path, length, newPath = localSearch2(graph, result)
    print "Found path"
    
    print "Checking validity of path..."
    if not checkVertices(graph, path):
        print "invalid path"
        print path
        break
    else:
        print "clear"
    
    print "Path: "
    print path
    print "With length " + str(length)
    print "_________________________________________"
    
    if len(path) != N:
        print 'length wrong'
        break
    
    
# find an answer, and put into assign
    assign = [0] * N
    for i in xrange(N):
        assign[i] = path[i] + 1

    fout.write("%s\n" % " ".join(map(str, assign)))
fout.close()