import util
from collections import deque
import sys
import random

parent = dict()
rank = dict()
graph = None
N = 0

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

def createPathMST(graph, edges):
    edges = sorted(list(edges), key = lambda x: x[1])
    length = len(edges)
    for e in range(length):
        edges.append((edges[e][0], edges[e][2], edges[e][1], edges[e][3]))
    best = []
    bestlen = sys.maxint
    for i in range(graph.numCities):
      tally = []
      for s in range(graph.numCities):
          tally.append(s)
      visited = []
      path = []
      stack = []
      for e in range(len(edges)):
          if (edges[e][1] == i or edges[e][2] == i):
              stack.append(edges[e])
      visited = [i]
      pathgroup = []
      path = [(i, graph.colors[i])]
      count = (1,graph.colors[i])
      while len(stack) > 0:
          edge = stack.pop()
          if edge[1] in visited and edge[2] in visited:
              continue
          if edge[1] not in visited:
              v = edge[1]
          elif edge[2] not in visited:
              v = edge[2]
          if graph.colors[v] == count[1]:
              count = (count[0]+1,graph.colors[v])
              if count[0] > 3:
                continue
          else:
              count = (1, graph.colors[v])
          i = 0
          tmp = []
          for e in graph.edges[v]:
              tmp.append([e,v, i, graph.colors[i]])
              i += 1
          tmp = sorted(tmp, key=lambda x: x[0])
          tmp.reverse()
          for item in tmp:
            stack.append(item)
          visited.append(v)
          path.append((v, graph.colors[v]))
      for i in visited:
          tally.remove(i)
      while len(tally) > 0:
          v = tally.pop()
          bestdump = sys.maxint
          bestloc = len(path)+1
          for i in range(1,len(path)):
            if (graph.colors[v] != path[i][1] and graph.colors[v] != path[i+1][1]):
                path.insert(i+1,(v,graph.colors[v]))
                if calcLength(path) < bestdump:
                  bestdump = calcLength(path)
                  bestloc = i+1
                path.remove((v,graph.colors[v]))
          path.insert(bestloc,(v,graph.colors[v]))
      length = calcLength(path)
      if (length < bestlen):
        best = path
        bestlen = length
    return best


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
        path.append(curr+1)
        edges.remove(nextEdge)
    return path, length

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

def calcLength(result):
  length = 0
  prev = -1
  for x in range(len(result)):
      if prev >= 0:
          length += graph.edges[prev][result[x][0]]
      prev = result[x][0]
  return length

def processCase(c, perm, d, name):
  # check it's valid
  v = [0] * N
  prev = 'X'
  count = 0
  for i in xrange(N):
    if v[perm[i]-1] == 1:
      print name + " Your answer must be a permutation of {1,...,N}."
      return -1
    v[perm[i]-1] = 1

    cur = c[perm[i]-1]
    if cur == prev:
      count += 1
    else:
      prev = cur
      count = 1

    if count > 3:
      print name + " Your tour cannot visit more than 3 same colored cities consecutively."
      return -1

  cost = 0
  for i in xrange(N-1):
    cur = perm[i]-1
    next = perm[i+1]-1
    cost += d[cur][next]

  return cost


if __name__ == "__main__":
    T = 495 # number of test cases
    fout = open ("answer1.out", "w")
    for t in xrange(135, T+1):
        fin = open("instances/"+str(t) + ".in", "r")
        N = int(fin.readline())
        d = [[] for i in range(N)]
        for i in xrange(N):
            d[i] = [int(x) for x in fin.readline().split()]
        c = fin.readline()

        graph = util.Graph(N, d, c)

        if N <= 10:
          result = findPath()
          result = createPath(result)
          sol = []
          for i in range(len(result)):
            sol.append(result[i][0]+1)
          l = processCase(c,sol,d, "bruteforce")
          for k in range(len(result)):
            fout.write("{0} ".format(str(sol[k])))
            if k == N -1:
              fout.write("{0}\n".format(str(sol[k])))

          print "bruteforce " + str(N) + " " + str(l)
          print "Path: " + str(sol)
        else:
          resultMST = MSTalg(graph)
          resultMST = createPathMST(graph, resultMST)
          sol = []
          for i in range(len(resultMST)):
            sol.append(resultMST[i][0]+1)
          lengthMST = processCase(c,sol,d, "MST")
          #resultLocal = createRandomPath(graph)
          #pathLocal, lengthLocal = localSearch2(graph, resultLocal)
          #lengthLocal = processCase(c,pathLocal,d, "Local")
          #print "Local: " + str(pathLocal)
          #if lengthLocal == -1 and lengthMST == -1:
            #fout.write("No solution lol oops\n")
            #continue
          #if lengthLocal == -1 or lengthMST < lengthLocal:
          print "MST " + str(N) + " " + str(lengthMST)
          print "Path: " + str(sol)
          result = sol
          """elif lengthLocal != -1:
            result = pathLocal
            print "localSearch " + str(N) + " " + str(lengthLocal)
            print "Path: " + str(pathLocal)"""
          #else:
            #print "ERROR, no solution?"
            #fout.write("no solutionnn!!! wrong\n")
            #continue
          for k in range(len(result)):
            fout.write("{0} ".format(str(result[k])))
            if k == N -1:
              fout.write("{0}\n".format(str(result[k])))
    fout.close()
