import json
import os

parentDir = os.listdir("assets/spine/")

data = {}

for i in parentDir:
    print(i)
    file = [x for x in (os.listdir(f"assets/spine/{i}")) if ".skel" in x]
    if len(file) > 1:
        # There should be only one skel in the folder
        # This happens when the developer packs by mistake
        for j in file:
            if j[0] == "_":
                continue
            if j[:-5].lower() not in i.lower():
                # skel name should be the same as the folder name
                continue
            data[j[:-5]] = f"assets/spine/{i}/{j}"
    else:
        if i[0] == "_":
            continue
        data[i] = f"assets/spine/{i}/" + ''.join(file)

if not(os.path.isdir("./data")):
    os.mkdir("./data")

# Sort the data by key by alphabet
data = dict(sorted(data.items()))

print(data)

with open("./data/models.json", "w") as f:
    json.dump(data, f, indent=6, sort_keys=True)
