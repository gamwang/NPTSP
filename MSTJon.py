import util
from collections import deque
import sys

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
        result_out = createPath(graph, i) 
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
