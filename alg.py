from util import *
from MSTJon import *
import sys


if __name__ == "__main__":
  T = 1 # number of test cases
  #fout = open ("answer.out", "w")
  failed = 0
  for t in xrange(2, 495):
      print "#################", t, ".in###################"
      fin = open("instances/" + str(t) + ".in", "r")
      N = int(fin.readline())
      d = [[] for i in range(N)]
      for i in xrange(N):
          d[i] = [int(x) for x in fin.readline().split()]
      c = fin.readline()

      graph = util.Graph(N, d, c)
      opt_result = None
      opt_length = 100000000
      for i in range(N):
        #print "%d'th trial" % i
        result_out = createPath(graph, i) 
        # Checking if color is correct
        #print "Is color all good? ", checkPath(graph, result_out)
        # cost
        length = getCost(graph, result_out)
        if opt_length > length:
            opt_length = length
            opt_result = result_out 
      print "Number of nodes: %d" % N
      print "Number of nodes in path: %d" % len(result_out)
      if N != len(result_out):
          failed += 1
      print "# failed: ", failed
      print "Cost: ", opt_length  
      print "Result: ", opt_result 
