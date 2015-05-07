import os.path
import random as rand
import sys

if (len(sys.argv) - 1) < 1:
    print("Usage: python genRandGraph.py NUM [NUMVER], NUM being number of graphs to generate")
    sys.exit()

name = 1
numGen = int(sys.argv[1])
setNumVer = None
if (len(sys.argv) - 1) == 2:
    setNumVer = int(sys.argv[2])
 
while os.path.isfile("graphs/" + "_" + str(name) + ".in"):
    name += 1

for _ in range(numGen):
    inp = open("_" + str(name) + ".in", "w")
    if setNumVer is None:
        numVer = 1
        while (numVer % 2 != 0):
            numVer = rand.randint(2, 50)
    else:
        numVer = setNumVer
    inp.write("{0}\n".format(numVer))
    
    temp = [0 for _ in range(numVer)]
    m = [temp[:] for _ in range(numVer)]
    for i in range(numVer):
        for j in range(numVer):
            if i == j:
                inp.write("0")
            elif (i - j) < 0:
                m[i][j] = str(rand.randint(0, 100))
                inp.write(m[i][j])
            else:
                inp.write(m[j][i])
            inp.write(" ")
            if j == (numVer - 1):
                inp.write("\n")
    
    r = numVer / 2
    b = numVer / 2
    coloring = ""
    while r > 0 and b > 0:
        if rand.randint(0, 1) == 1:
            r -= 1
            coloring += "R"
        else:
            b -= 1
            coloring += "B"

    while r > 0:
        coloring += "R"
        r -= 1
    while b > 0:
        coloring += "B"
        b -= 1

    inp.write(coloring + "\n")
    inp.close()
    print("_" + str(name) + ".in")
    name += 1

