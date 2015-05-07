import util
from collections import deque
import sys


graph = None
N = 0

def toColor(i):
    return graph.colors[i]

def last3Color(path):
    if len(path) < 3:
        return False, None
    c1 = toColor(path[-1])  
    c2 = toColor(path[-2])
    c3 = toColor(path[-3])
    if (c1 == "R" and c2 == "R" and c3 == "R"):
        return True, "R"
    elif (c1 == "B" and c2 == "B" and c3 == "B"):
        return True, "B"
    else:
        return False, None

def calcDist(path):
    length = 0
    prev = -1
    for x in path:
        if prev >= 0:
            length += graph.edges[prev][x]
        prev = x
    return length

def removeEmpty(paths):
    valid = []
    for p in paths:
        if p is None:
            continue
        valid.append(p)
    return valid

#[(path, dist), (path,dist)]
def returnShort(paths):
    
    paths = removeEmpty(paths)
    if len(paths) == 0:
        return None

    shortsofar = paths[0]
    for p in paths:
        if p[1] < shortsofar[1]:
            shortsofar = p
    return shortsofar

def findPath():
    bestSoFar = ()
    pathLeft = [x for x in range(0, N)]
    tup = bestPath([], pathLeft)
    return tup[0]

#shortest = ([2,1,4,3], 20)
#path = [4,2,1] [3]
#returns [(path, length of path)]
def bestPath(path, left):
    assert len(path) + len(left) == N 
    if len(path) == N:
        return (path, calcDist(path))
    
    collectPath = []
    isLast3Same, c = last3Color(path)
    for x in left:
        if (isLast3Same and
         ((c == "R" and toColor(x) == "R") or (c == "B" and toColor(x) == "B"))):
            continue
        newLeft = left[:]
        newLeft.remove(x)
        newPath = path[:]
        newPath.append(x)

        shortest = bestPath(newPath, newLeft)
        collectPath.append(shortest)

    if len(collectPath) == 0:
        return None

    return returnShort(collectPath)

def createPath(path):
    result = [0 for _ in range(N)]
    for x in range(len(path)):
        result[x] = (path[x], graph.colors[x])
    return result
				
if __name__ == "__main__":
    T = 1 # number of test cases
    #fout = open ("answer.out", "w")
    for t in xrange(1, 2):
        fin = open("instances/231" + ".in", "r")
        N = int(fin.readline())
        d = [[] for i in range(N)]
        for i in xrange(N):
            d[i] = [int(x) for x in fin.readline().split()]
        c = fin.readline()

        graph = util.Graph(N, d, c)

        result = findPath()
        result = createPath(result)
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
