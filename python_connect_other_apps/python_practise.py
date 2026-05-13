


import pdb

pdb.set_trace()   # Execution pauses here
file = open("file.txt", "r")
lines = file.readlines()
for line in lines:
    print(line)
file.close()