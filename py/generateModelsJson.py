import json
import os

parentDir = os.listdir("assets/spine/")

data = {}

for i in parentDir:
    # There may be more than one skel in the folder, and there's also possibility of pack mistakes.
    # Currently, not handling this.
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

"""
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
    elif len(file) == 0:
        # No skel file in the folder
        continue
    else:
        # Only one skel file in the folder
        if i[0] == "_":
            continue
        data[i] = f"assets/spine/{i}/" + ''.join(file)
"""


if not (os.path.isdir("./data")):
    os.mkdir("./data")

with open("./data/models.json", "w") as f:
    json.dump(data, f, indent=6, sort_keys=True)
