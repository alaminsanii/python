import os

def generatetable(n, directory):
    table = ""
    for i in range(1, 11):
        table += f"{n} * {i} = {n*i}\n"

    with open(f"{directory}/table__{n}.txt", "w") as f:
        f.write(table)

# Find the next available directory number
counter = 2
while os.path.exists(f"tables_{counter}"):
    counter += 1

directory = f"tables_{counter}"
os.makedirs(directory)

for i in range(1, 21):
    generatetable(i, directory)

print(f"Tables saved in: {directory}")