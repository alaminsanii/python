import os
import shutil

def generatetable(n):
    table = ""
    for i in range(1, 11):
        table += f"{n} * {i} = {n*i}\n"

    os.makedirs("tables_2", exist_ok=True)  # cleaner than try/except
    with open(f"tables_2/table__{n}.txt", "w") as f:
        f.write(table)

# Clear old directory before generating
if os.path.exists("tables_2"):
    shutil.rmtree("tables_2")

for i in range(1, 29):
    generatetable(i)
