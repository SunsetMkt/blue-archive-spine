import os

import requests
import UnityPy

# conf
option = {
    # will skip resources that already downloaded.
    "skipExistingDownloadedResource": True,
    # will skip assets that already exists.
    "skipExistingAssets": True
}

ba_api = "https://yostar-serverinfo.bluearchiveyostar.com/r60_826142735o1hiici1puy.json"

ba_api2 = "https://prod-noticeindex.bluearchiveyostar.com/prod/index.json"


def getVersion():
    '''
    Return latest version of Blue Archive Japan
    Unused for now
    '''
    data = requests.get(ba_api2).json()
    return data["LatestClientVersion"]


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
    # parse the object data
    data = object.read()

    # create destination path
    dest = os.path.join(dest, data.name)

    # touch folder
    os.makedirs(os.path.dirname(dest), exist_ok=True)

    # just save
    with open(dest, "wb") as f:
        f.write(data.script)


def extractTexture2D(object, dest):
    # parse the object data
    data = object.read()

    # create destination path
    dest = os.path.join(dest, data.name)

    # touch folder
    os.makedirs(os.path.dirname(dest), exist_ok=True)

    # make sure that the extension is correct
    # you probably only want to do so with images/textures
    dest, ext = os.path.splitext(dest)
    dest = dest + ".png"

    img = data.image
    img.save(dest)


def extractCharacter(src, dest):
    # load the bundle
    bundle = UnityPy.load(src)

    for obj in bundle.objects:
        # extract skel & atlas
        if obj.type.name == "TextAsset":
            data = obj.read()
            if ".atlas" in data.name or ".skel" in data.name:
                print(data.name)
                extractTextAsset(obj, dest)
        # extract texture
        elif obj.type.name == "Texture2D":
            data = obj.read()

            print(data.name + ".png")
            extractTexture2D(obj, dest)


if __name__ == "__main__":
    # make folder
    if not (os.path.isdir("./downloaded_resource")):
        os.makedirs("./downloaded_resource")
    if not (os.path.isdir("./assets")):
        os.makedirs("./assets")
    if not (os.path.isdir("./assets/spine")):
        os.makedirs("./assets/spine")
    if not (os.path.isdir("./data")):
        os.makedirs("./data")

    # There are several ResourceURL to a version
    ver = getBaseResourceURL() + "/Android/bundleDownloadInfo.json"
    print(ver)
    if (os.path.isfile("./data/version.txt")):
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

        if not (os.path.isdir(destExtract)):
            os.makedirs(destExtract)

        downloadFile(model, destDownload)
        # extract
        try:
            extractCharacter(destDownload, destExtract)
        except:
            print("Error occured. Skipping.")
            import traceback
            traceback.print_exc()
