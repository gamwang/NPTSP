import random
import util

def createRandomPath(graph):
    currCity = random.randint(0, graph.numCities - 1)
    start = currCity
    edges = []
    notVisited = set(range(0, graph.numCities))
    notVisited.remove(currCity)
    color = graph.colors[currCity]
    count = 1
    while len(edges) < 49:
        nextEdge = random.sample(notVisited, 1)[0]
        if graph.colors[nextEdge] == color and count == 3:
            continue
        elif graph.colors[nextEdge] == color:
            count += 1
        else:
            count = 1
            color = graph.colors[nextEdge]
        if nextEdge in notVisited:
            edges.append((currCity, nextEdge, graph.edges[currCity][nextEdge], graph.colors[currCity], graph.colors[nextEdge]))
            print "Curr" + str((currCity == nextEdge))
            currCity = nextEdge
            notVisited.remove(currCity)
    last = edges[48][1]
    print "last" + str((last == start))
    edges.append((last, start, graph.edges[currCity][nextEdge], graph.colors[last], graph.colors[start]))
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


def take2SameColor(graph, edges, v):
    possible = []
    for e in edges:
        if e[0] == v or e[1] == v:
            possible.append(e)
    for e in possible:
        if graph.colors[e[0]] != graph.colors[e[1]]:
            return 0
    color = graph.colors[e[0]]
    edge1 = random.sample(possible, 1)[0]
    if color == 'R':
        other = []
        for e in edges:
            if e[3] == 'R' and e[4] == 'R' and e != edge1:
                other.append(e)
    elif color == 'B':
        other = []
        for e in edges:
            if e[3] == 'B' and e[4] == 'B' and e != edge1:
                other.append(e)
                
    edge2 = random.sample(other, 1)[0]
    count = 0
    while (edge2[0] == edge1[0] or edge2[0] == edge1[1] or edge2[1] == edge1[0] or edge2[1] == edge1[1]) and count < 20:
        edge2 = random.sample(other, 1)[0]
        count += 1
    if count == 20:
        return 0
    return (edge1, edge2)


def switch2(graph, edges, length):
    """Switch two edges in a graph with the same color, returns new edge list and length of path"""
    for i in range(graph.numCities):
        pair = take2SameColor(graph, edges, i)
        if pair == 0:
            continue
        else: 
            edge1 = pair[0]
            edge2 = pair[1]
            newEdge1 = (edge1[0], edge2[1], graph.edges[edge1[0]][edge2[1]], graph.colors[edge1[0]], graph.colors[edge2[1]])
            newEdge2 = (edge1[1], edge2[0], graph.edges[edge1[1]][edge2[0]], graph.colors[edge1[1]], graph.colors[edge2[0]])
            newList = list(edges)
            newList.remove(edge1)
            newList.append(newEdge1)
            newList.remove(edge2)
            newList.append(newEdge2)

            temp = list(newList)
            count = 0
            newLength = 0
            curr = temp[0][0]
            while len(temp) > 0:
                for e in temp:
                    if e[0] == curr or e[1] == curr:
                        edge = e
                        break
                if edge[0] == curr:
                    curr = edge[1]
                elif edge[1] == curr:
                    curr = edge[0]
                if (edge not in temp):
                    break
                temp.remove(edge)
                newLength += edge[2]
                count += 1
                
            if count != 50:
                newList = list(edges)
                newEdge1 = (edge1[0], edge2[0], graph.edges[edge1[0]][edge2[0]], graph.colors[edge1[0]], graph.colors[edge2[0]])
                newEdge2 = (edge1[1], edge2[1], graph.edges[edge1[1]][edge2[1]], graph.colors[edge1[1]], graph.colors[edge2[1]])

                newList.remove(edge1)
                newList.append(newEdge1)
                newList.remove(edge2)
                newList.append(newEdge2)

                newLength = sum([edge[2] for edge in newList])
                temp = list(newList)
                count = 0
                newLength = 0
                curr = temp[0][0]
                while len(temp) > 0:
                    for e in temp:
                        if e[0] == curr or e[1] == curr:
                            edge = e
                            break
                    if edge[0] == curr:
                        curr = edge[1]
                    elif edge[1] == curr:
                        curr = edge[0]
                    if (edge not in temp):
                        break
                    temp.remove(edge)
                    newLength += edge[2]
                    count += 1
                
            if (newLength < length):
                print newEdge1[0] == newEdge1[1] or newEdge2[0] == newEdge2[1]
                return (newList, newLength)
    return 0
        
    

def switch2WithColor(graph, edges):
    """Switch two edges in a grph with different colors, returns new edge list and length of path"""
    

    
def checkPath(graph, edges):  
    temp = list(edges)
    curr = temp[0][0]
    while len(temp) > 0:
        nextEdge = -1
        for e in temp:
            if e[0] == curr or e[1] == curr:
                nextEdge = e
                break
        if nextEdge == -1:
            print temp
            return "error"
        elif nextEdge[0] == curr:
            curr = nextEdge[1]
            temp.remove(nextEdge)
        else:
            curr = nextEdge[0]
            temp.remove(nextEdge)
    return 'yay'

def localSearch2(graph, edges):
    """asd"""
    length = sum([edge[2] for edge in edges])
    x = 0
    newPath = edges
    while x < 100:
        print length
        count = 0
        result = switch2(graph, edges, length)
        if result == 0:
            break
        else:
            newPath, newLength = result
            edges = newPath
            length = newLength
            count += 1
            x += 1

    print checkPath(graph, newPath)


T = 1 # number of test cases
#fout = open ("answer.out", "w")
for t in xrange(1, 2):
    fin = open("inputs/JonIsTrash" + str(t) + ".in", "r")
    N = int(fin.readline())
    d = [[] for i in range(N)]
    for i in xrange(N):
        d[i] = [int(x) for x in fin.readline().split()]
    c = fin.readline()

    graph = util.Graph(N, d, c)
    
    result = createRandomPath(graph)
    
#Test random path
#    for e in range(len(result)):
#        print "Edge " + str(e)
#        print result[e]
#    print testRandom(graph, result)

    path = localSearch2(graph, result)
    
    
    
    
# find an answer, and put into assign
#    assign = [0] * N
#    for i in xrange(N):
#        assign[i] = i+1
#
#    fout.write("%s\n" % " ".join(map(str, assign)))
#fout.close()