import os
from io import BytesIO

import requests
import unitypack
from PIL import ImageOps

# conf
option = {
    # will skip resources that already downloaded.
    "skipExistingDownloadedResource": True,
    # will skip assets that already exists.
    "skipExistingAssets": True
}

ba_api = "https://yostar-serverinfo.bluearchiveyostar.com/r48_2q1alt6gvk5igdsj4hl2.json"


def getVersion():
    data = requests.get(ba_api).json()
    return data["ConnectionGroups"][0]['OverrideConnectionGroups'][-1]['Name']


def getBaseResourceURL():
    '''
    Return resource url for Blue Archive
    '''
    data = requests.get(ba_api).json()
    print(data)
    return data["ConnectionGroups"][0]['OverrideConnectionGroups'][-1]['AddressablesCatalogUrlRoot']
    # https://prod-clientpatch.bluearchiveyostar.com/r47_1_22_46zlzvd7mur326newgu8_2 + /Android/bundleDownloadInfo.json


def getModelsList():
    '''
    Return list of Blue Archive characters url path.
    '''
    data = []
    base_url = getBaseResourceURL()
    res_url = base_url + '/Android/bundleDownloadInfo.json'
    res = requests.get(res_url).json()
    for asset in res["BundleFiles"]:
        if "spinecharacters-" in asset["Name"] or "spinelobbies-" in asset["Name"] or "spinebackground-" in asset["Name"]:
            # append url and path
            data.append(base_url + '/Android/' + asset["Name"])
    return data


def downloadFile(url, fname):
    src = requests.get(url).content
    with open(fname, 'wb') as f:
        f.write(src)


def extractTextAsset(object, dest):
    data = object.read()
    if(type(data.script) == bytes):
        with open(f"{dest}/{data.name}", "wb") as f:
            f.write(data.script)
    elif(type(data.script) == str):
        with open(f"{dest}/{data.name}", "wb") as f:
            f.write(bytes(str(data.script), 'utf-8'))
    else:
        raise Exception("Not handled")


def extractTexture2D(object, dest):
    data = object.read()
    img = ImageOps.flip(data.image)
    output = BytesIO()
    img.save(output, format="png")
    with open(f"{dest}/{data.name}.png", "wb") as f:
        f.write(output.getvalue())


def extractCharacter(src, dest):
    with open(src, "rb") as f:
        bundle = unitypack.load(f)
        for asset in bundle.assets:
            # print("%s: %s:: %i objects" % (bundle, asset, len(asset.objects)))
            for id, object in asset.objects.items():
                # print(id, object)
                # extract skel & atlas
                if object.type == "TextAsset":
                    data = object.read()
                    if ".atlas" in data.name or ".skel" in data.name:
                        print(data.name)
                        extractTextAsset(object, dest)
                # extract texture
                elif object.type == "Texture2D":
                    data = object.read()

                    print(data.name + ".png")
                    extractTexture2D(object, dest)


if __name__ == "__main__":
    # make folder
    if not(os.path.isdir("./downloaded_resource")):
        os.makedirs("./downloaded_resource")
    if not(os.path.isdir("./assets")):
        os.makedirs("./assets")
    if not(os.path.isdir("./assets/spine")):
        os.makedirs("./assets/spine")
    if not(os.path.isdir("./data")):
        os.makedirs("./data")

    # There are several ResourceURL to a version
    ver = getBaseResourceURL() + "/Android/bundleDownloadInfo.json"
    print(ver)
    if(os.path.isfile("./data/version.txt")):
        with open("./data/version.txt", "r") as f:
            ver_temp = f.read()
        if str(ver) == str(ver_temp):
            print(f"[{ver}] No new update. Stopping.")
            exit(1)
        else:
            print(f"Update {ver_temp} to {ver}")
            with open("./data/version.txt", "w") as f:
                f.write(ver)
    else:
        with open("./data/version.txt", "w") as f:
            f.write(ver)

    # get model list
    model_list = getModelsList()

    # download list of model list
    for index, model in enumerate(model_list, start=1):
        print("="*30)
        print(f"{index}/{len(model_list)}")
        fname = model.split("/")[-1]
        destDownload = f"./downloaded_resource/{fname}"

        print(fname)

        # skip if already exists
        if option["skipExistingDownloadedResource"] and os.path.isfile(destDownload):
            print("Already downloaded. Skipping.")
            continue

        # spinebackground, spinecharacters and spinelobbies only
        character_name = ''.join(fname.split("spinecharacters-")[1].split("-")[0] if "spinecharacters" in fname else fname.split(
            "spinelobbies-")[1].split("-")[0] if "spinelobbies" in fname else fname.split("spinebackground-")[1].split("-")[0])
        destExtract = f"./assets/spine/{character_name}"

        # skip if already exists
        if option["skipExistingAssets"] and os.path.isfile(destExtract):
            print("Already extracted. Skipping.")
            continue

        if not(os.path.isdir(destExtract)):
            os.makedirs(destExtract)

        downloadFile(model, destDownload)
        # extract
        extractCharacter(destDownload, destExtract)
