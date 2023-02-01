import json
import os

import requests

from getModelsGlobal import downloadFile, getResourceURL, updateBaData

data = {}

# 1 for offline, 0 for online but cors issue
_type = 1

option = {
    "skipExisting": True
}

if not (os.path.isdir("./data")):
    os.mkdir("./data")

if __name__ == "__main__":
    # updateBaData first
    updateBaData()

    resUrl = getResourceURL()
    baseUrl = '/'.join(resUrl.split("/")[0:-1])
    res = requests.get(resUrl).json()["resources"]
    for asset in res:
        if "Audio/VOC_JP/" in asset["resource_path"] and "MemorialLobby" in asset["resource_path"]:
            keyEvent = ''.join(
                asset["resource_path"].split("/")[-1].split(".")[:-1])
            fname = ''.join(asset["resource_path"].split("/")[-1])

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
                downloadFile(baseUrl + "/" + asset["resource_path"], path)
                data[keyEvent] = path
            else:
                # online ver (cors ?)
                data[keyEvent] = baseUrl + "/" + asset["resource_path"]

    print(data)
    with open("./data/audio.json", "w") as f:
        json.dump(data, f, indent=4)
    print("="*30)
    print("Done!")
