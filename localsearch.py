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

def testRandom(graph, edges):
    visited = []
    color = "a"
    count = 0
    for e in edges:
        if e[0] in visited:
            return False
        else:
            if color == graph.colors[e[0]] and count == 3:
                return False
            elif color == graph.colors[e[0]]:
                count += 1
            else:
                count = 1
                color = graph.colors[e[0]]
            visited.append(e[0])
    return True

def checkPath(graph, edges):  
    temp = list(edges)
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
    highest = 0
    edge = 0
    for e in edges:
        if e[2] > highest:
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
    return path, length



T = 1 # number of test cases
#fout = open ("answer.out", "w")
for t in xrange(58, 59):
    fin = open("instances/" + str(t) + ".in", "r")
    N = int(fin.readline())
    d = [[] for i in range(N)]
    for i in xrange(N):
        d[i] = [int(x) for x in fin.readline().split()]
    c = fin.readline()

    graph = util.Graph(N, d, c)
    
    print "Running on " + str(N) + " node graph"
    
    result = createRandomPath(graph)
    
#Test random path
    #print "Random: " + str(checkPath(graph, result))

    edges, length = localSearch2(graph, result)
    
#    if not checkPath(graph, edges):
#        print 'color wrong'
#        break
    
    print "Found path: "
    print edges
    print "With length " + str(length)
    print "_________________________________________"
    
    if len(edges) != N:
        print 'length wrong'
        break
    
    
# find an answer, and put into assign
#    assign = [0] * N
#    for i in xrange(N):
#        assign[i] = i+1
#
#    fout.write("%s\n" % " ".join(map(str, assign)))
#fout.close()