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
ba_ps = "https://play.google.com/store/apps/details?id=com.nexon.bluearchive"
ba_api = "https://api-pub.nexon.com/patch/v1.1/version-check"
ba_api_data = {
    "market_game_id": "com.nexon.bluearchive",
    "language": "en",
    "advertising_id": "636a7b75-5516-427b-b140-45318d3d51f0",
    "market_code": "playstore",
    "country": "US",
    "sdk_version": "187",
    "curr_build_version": "1.36.120365",
    "curr_build_number": 120365,
    "curr_patch_version": 0
}


def getVersion():
    '''
    Return Blue Archive build version and build number.
    '''
    # There are two ways to get the version.
    # 1. Get the version from BA API
    # 2. Get the version from BA Play Store page
    # We will try to get the version from BA API first.

    # Get the version from BA API
    try:
        r = requests.post(ba_api, json=ba_api_data)
        r.raise_for_status()
        data = r.json()
        build_version = data['latest_build_version']
        ver = build_version
        print(ver)
        # build_number = data['latest_build_number']
        # return (build_version, int(build_number))
    except:
        # Get the version from BA Play Store page
        print("Failed to get version from BA API.")
        src = requests.get(ba_ps).text
        # lmao python sucks
        try:
            ver = eval(src.split("AF_initDataCallback({key: 'ds:5', hash: ")[1].split("'")[2].split("data:")[1].split(
                ", sideChannel: {}")[0].replace("null", "None").replace("false", "False").replace("true", "True"))
            ver = ver[1][2][140][0][0][0]
            print(ver)
            # ver = src.split('<div class="IQ1z0d"><span class="htlgb">')[4].split('</span></div></span></div><div class="hAyfc">')[0]
        except:
            # Get the version from BA Play Store page with regex
            print('Fallback to regex')
            # Fallback
            import re

            # Find all [["*.*.*"]]
            ver = re.findall(r'\[\[\"+(\d+(.\d+)+(.\d+))+\"\]\]', src)
            print(ver)
            # Get the first one
            ver = ver[0][0]

    return (ver, int(ver.split(".")[-1]))


def updateBaData():
    global ba_api_data

    ba_api_data = {
        "market_game_id": "com.nexon.bluearchive",
        "language": "en",
        "advertising_id": "636a7b75-5516-427b-b140-45318d3d51f0",
        "market_code": "playstore",
        "country": "US",
        "sdk_version": "187",
        "curr_build_version": getVersion()[0],
        "curr_build_number": getVersion()[1],
        "curr_patch_version": 0
    }


def getResourceURL():
    '''
    Return resource url for Blue Archive
    '''
    data = requests.post(ba_api, json=ba_api_data).json()
    print(data)
    return data["patch"]["resource_path"]


def getModelsList():
    '''
    Return list of Blue Archive characters url path.
    '''
    data = []
    res_url = getResourceURL()
    res = requests.get(res_url).json()
    for asset in res["resources"]:
        if "spinecharacters-" in asset["resource_path"] or "spinelobbies-" in asset["resource_path"] or "spinebackground-" in asset["resource_path"]:
            # append url and path
            data.append('/'.join(res_url.split("/")
                        [0:-1]) + "/" + asset["resource_path"])
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

    ver = getResourceURL()  # There are several ResourceURL to a version
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

    # important
    updateBaData()

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
