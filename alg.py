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
      out = solveTSP(graph, N, True)
      if out == None:
          failed += 1
      print "# Failed: ", failed
      print out
