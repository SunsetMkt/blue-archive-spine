import json
import os

import requests

from getModelsJapan import downloadFile, getBaseResourceURL

data = {}

# 1 for offline, 0 for online but cors issue
_type = 1

option = {
    "skipExisting": True
}

if not (os.path.isdir("./data")):
    os.mkdir("./data")

if __name__ == "__main__":
    baseUrl = getBaseResourceURL() + '/MediaResources'
    resUrl = baseUrl + '/MediaCatalog.json'
    # https://prod-clientpatch.bluearchiveyostar.com/r47_1_22_46zlzvd7mur326newgu8_2 + /MediaResources/MediaCatalog.json
    res = requests.get(resUrl).json()["Table"]
    for asset in res:
        if "Audio/VOC_JP/" in res[asset]["path"] and "MemorialLobby" in res[asset]["path"]:
            keyEvent = ''.join(
                res[asset]["path"].split("/")[-1].split(".")[:-1])
            fname = ''.join(res[asset]["path"].split("/")[-1])

            # download ver
            if _type:
                path = f"./assets/audio/{fname}"
                print("="*30)
                print(fname)
                if os.path.isfile(path):
                    print("Already downloaded. Skipping.")
                    data[keyEvent] = path
                    continue
                if not (os.path.isdir("./assets/audio")):
                    os.mkdir("./assets/audio/")
                downloadFile(baseUrl + "/" + res[asset]["path"], path)
                data[keyEvent] = path
            else:
                # online ver (cors ?)
                data[keyEvent] = baseUrl + "/" + res[asset]["path"]

    print(data)
    with open("./data/audio.json", "w") as f:
        json.dump(data, f, indent=4)
    print("="*30)
    print("Done!")
