import os
import json

parentDir = os.listdir("assets/spine/")

data = {}

for i in parentDir:
    print(i)
    file = [x for x in (os.listdir(f"assets/spine/{i}")) if ".skel" in x]
    if len(file) > 1:
        for j in file:
            if j[0] == "_":
                continue
            data[j[:-5]] = f"assets/spine/{i}/{j}"
    else:
        if i[0] == "_":
            continue
        data[i] = f"assets/spine/{i}/" + ''.join(file)

if not(os.path.isdir("./data")):
    os.mkdir("./data")

with open("./data/models.json", "w") as f:
    json.dump(data, f, indent=6, sort_keys=True)