import os.path

name = 1
potato = {}
while os.path.isfile(str(name) + ".in"):
    inp = open(str(name) + ".in", "r")
    size = inp.readline()
    size = size[:-1]
    try:
        i = int(size)
        if i < 15:
            print str(name) + " : " + str(i)
    except ValueError:
        pass
    if size not in potato:
        potato[size] = 1
    else:
        potato[size] += 1
    name += 1
    inp.close()
print sorted(potato)
