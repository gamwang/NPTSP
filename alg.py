from util import *
from MSTJon import *


if __name__ == "__main__":
  T = 1 # number of test cases
  #fout = open ("answer.out", "w")
  for t in xrange(1, 4):
      print "#################", t, "###################"
      fin = open("inputs/JonIsTrash" + str(t) + ".in", "r")
      #fin = open("inputs/test_6" + ".in", "r")
      N = int(fin.readline())
      d = [[] for i in range(N)]
      for i in xrange(N):
          d[i] = [int(x) for x in fin.readline().split()]
      c = fin.readline()

      graph = util.Graph(N, d, c)
      result = MSTalg(graph)
      opt_result = None
      opt_length = 100000000
      for i in range(50):
        #print "%d'th trial" % i
        result_out = createPath(graph, result, i)
        length = 0
        prev = -1
        for x in range(len(result_out)):
            if prev >= 0:
                length += graph.edges[prev][result_out[x][0]]
            prev = result_out[x][0]
        #print length
        if opt_length > length:
            opt_length = length
            opt_result = result_out
      print opt_length  
      print opt_result
      #print "Result:"
      #length = 0
      #prev = -1
      #for x in range(len(result)):
          #if prev >= 0:
              #length += graph.edges[prev][result[x][0]]
          #print graph.edges[prev][result[x][0]]
          #prev = result[x][0]
          #print result[x]
      #print "Length: ", str(length)
