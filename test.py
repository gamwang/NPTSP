import util

def greedyAlgorithm(graph):
    bestCost = 1000000000000000000
    bestPath = []
    for i in range(graph.numCities):
        curr = i
        visited = [i]
        color = graph.colors[curr]
        count = 1
        cost = 0
        while len(visited) != graph.numCities:
            smallest = 100000000000000000000
            nextNode = -1
            for node, dist in enumerate(graph.edges[curr]):
                if (node != curr) and (node not in visited):
                    if smallest > dist:
                        smallest = dist
                        nextNode = node
#            if count > 3:
#                return -1
#            elif color == graph.colors[nextNode]:
#                count += 1
#            else:
#                color = graph.colors[nextNode]
#                count = 1
            cost += graph.edges[curr][nextNode]
            curr = nextNode
            visited.append(curr)
        if bestCost > cost:
            bestCost = cost
            bestPath = visited
    return (bestCost, bestPath)


T = 1 # number of test cases
#fout = open ("answer.out", "w")
for t in xrange(7, 8):
    fin = open(str(t) + ".in", "r")
    N = int(fin.readline())
    d = [[] for i in range(N)]
    for i in xrange(N):
        d[i] = [int(x) for x in fin.readline().split()]
    c = fin.readline()

    graph = util.Graph(N, d, c)
    
    result = greedyAlgorithm(graph)
    print "Length:"
    print result[0]
    print "Path:"
    for x in range(len(result[1])):
        print (result[1][x], graph.colors[result[1][x]])

    
    # find an answer, and put into assign
#    assign = [0] * N
#    for i in xrange(N):
#        assign[i] = i+1
#
#    fout.write("%s\n" % " ".join(map(str, assign)))
#fout.close()

