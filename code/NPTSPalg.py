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

def MSTGreedy(graph, start):
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
    return path
def solveTSP(graph, N, debug = False):
    opt_result = None
    opt_length = sys.maxint
    for i in range(N):
        result_out = MSTGreedy(graph, i) 
        # cost
        length = util.getCost(graph, result_out)
        if opt_length > length and len(result_out) == N:
            opt_length = length
            opt_result = result_out  
    if opt_result == None:
        return opt_result
    out = map(lambda x: x[0] + 1, opt_result)
    if debug:
        print "Number of nodes: %d" % N
        print "Number of nodes in path: %d" % len(out)
        print "Cost: ", opt_length  
        print "Result: ", opt_result
    return out

def processCase(c, perm, d, name):
  # check it's valid
  v = [0] * N
  prev = 'X'
  count = 0
  for i in xrange(N):
    if v[perm[i]-1] == 1:
      if name != "Random":
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
      if name != "Random":
        print name + " Your tour cannot visit more than 3 same colored cities consecutively."
      return -1

  cost = 0
  for i in xrange(N-1):
    cur = perm[i]-1
    next = perm[i+1]-1
    cost += d[cur][next]

  return cost

def genRandom(c, d):
    x = [i + 1 for i in range(N)]
    random.shuffle(x)
    while processCase(c, x, d, "Random") == -1:
        random.shuffle(x)
    return x

if __name__ == "__main__":
    T = 495 # number of test cases
    fout = open ("answer2.out", "w")
    for t in xrange(1, T+1):
        fin = open("instances/"+str(t) + ".in", "r")
        N = int(fin.readline())
        d = [[] for i in range(N)]
        for i in xrange(N):
            d[i] = [int(x) for x in fin.readline().split()]
        c = fin.readline()

        graph = util.Graph(N, d, c)
        print "Input " + str(t)
        if N <= 10:
          #Brute Force
          result = findPath()
          result = createPath(result)
          sol = []
          for i in range(len(result)):
            sol.append(result[i][0]+1)
          l = processCase(c,sol,d,"Brute force")
          for k in range(len(result)):
            fout.write("{0} ".format(str(sol[k])))
            if k == N -1:
              fout.write("{0}\n".format(str(sol[k])))

          print ">>>>>>>>>>>>>> Bruteforce " + str(N) + " " + str(l)
          print "Path: " + str(sol)
        else:
          #Random
          resultRand = genRandom(c, d)
          lengthRand = processCase(c,resultRand,d, "Rand")

          #MST
          resultMST = MSTalg(graph)
          sol = createPathMST(graph, resultMST)
          resultMST = []
          for i in range(len(sol)):
            resultMST.append(sol[i][0]+1)
          lengthMST = processCase(c,resultMST,d, "MST")
          
          #Greedy
          resultGreedy = solveTSP(graph, N)
          if resultGreedy == None:
            resultGreedy = genRandom(c, d)
          lengthGreedy = processCase(c,resultGreedy,d, "Greedy")
          if lengthGreedy == -1:
            resultGreedy = genRandom(c,d)
            lengthGreedy = processCase(c, resultGreedy, d, "Greedy")

          #Local Search
          initial = createRandomPath(graph)
          sol, length, newPath = localSearch2(graph, initial)
          resultLocal = []
          for i in range(len(sol)):
            resultLocal.append(sol[i]+1)
          lengthLocal = processCase(c, resultLocal, d, "Local Search")
          
          if lengthLocal == -1:
            resultLocal = genRandom(c,d)
            lengthLocal = processCase(c, resultLocal, d, "Local Search")

          bestScore = min(lengthMST, lengthGreedy, lengthLocal, lengthRand)
          if bestScore == lengthLocal:
            print ">>>>>>>>>>>>>>>> Local Search " + str(N) + " " + str(lengthLocal)
            print "Path: " + str(resultLocal)
            result = resultLocal
          elif bestScore == lengthMST:
            print ">>>>>>>>>>>>>>>> MST " + str(N) + " " + str(lengthMST)
            print "Path: " + str(resultMST)
            result = resultMST
          elif bestScore == lengthGreedy:  
            result = resultGreedy
            print ">>>>>>>>>>>>>>>> Greedy " + str(N) + " " + str(lengthGreedy)
            print "Path: " + str(resultGreedy)
          else:
            print "Nothing works so GENERATING RANDOM YOLO"
            result = resultRand
          for k in range(len(result)):
            fout.write("{0} ".format(str(result[k])))
            if k == N -1:
              fout.write("{0}\n".format(str(result[k])))
    fout.close()


