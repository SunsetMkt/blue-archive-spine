# blue-archive-spine
Based on [respectZ/blue-archive-spine](https://github.com/respectZ/blue-archive-spine)

**Blue Archive is a registered trademark of NAT GAMES Co., Ltd. This repo is not affiliated with NEXON Korea Corp. & NEXON GAMES Co., Ltd. All game resources are copyrighted to the respective owners.**

## Quick Start
* Use this template
* Create `jp` and `global` branch from `resourceless`
* Enable GitHub Actions, manually trigger `Update-Global` and `Update-JP` at any branch (they will find the right branch, no matter where you trigger them) to get the first update
* `Update-Global` will run daily and fails when no update is available, `Update-JP` won't run automatically

`Update-JP` Needs to be triggered manually since there isn't a solution to get the latest update json link automatically (maybe there is, but I'm not going to write it now). `ba_api` in `getModelsJapan.py` needs to be updated manually (through reverse engineering or network capture) when there is a new update.

## About Japan version
The update json link is hard coded into the game OBB resources.

We can get `LatestClientVersion` from `https://prod-noticeindex.bluearchiveyostar.com/prod/index.json`, but how the random hash path (likes `r48_2q1alt6gvk5igdsj4hl2.json`) under `yostar-serverinfo.bluearchiveyostar.com` is generated?

BA Japan (Yostar) does not have a certain resource path API. And their developers hard code the resource link for a version into the game OBB resources. The game only checks for `LatestClientVersion` to see if it's outdated and asks the user to update the game from Google Play to get the latest resource link.

Does this mean the user has to update the game from Google Play every month to get the latest monthly in-game activity? -- Yes, this is what's happening. (BA Japan releases an update at Google Play about every month, while BA Global updates about every three months)

You can extract `GameMainConfig` from game OBB and decrypt it. Check the key `ServerInfoDataUrl` in `GameMainConfig` to get the resource link.

## About this repo
This repo is a fork of [respectZ/blue-archive-spine](https://github.com/respectZ/blue-archive-spine). Some contributors and I modified the code to make it work better.

`blue-archive-spine` is a tool to download and view the character arts and animations (Memorial Lobby) of the game [Blue Archive](https://bluearchive.nexon.com/home).

It's recommneded to use GitHub Actions to download the resources automatically. If you want to download the resources manually, please refer to the original README. Attention: Do not open `index.html` locally, all resource must be served with an HTTP server.

## License
This repo is based on the work of @respectZ and @LXY1226 . The original repo doesn't have a license, so I'm not sure if it can be used for any purpose.

## Disclaimer
**Blue Archive is a registered trademark of NAT GAMES Co., Ltd. This repo is not affiliated with NEXON Korea Corp. & NEXON GAMES Co., Ltd. All game resources are copyrighted to the respective owners.**

## The following is the original README.

*Please notice: some of the following information is outdated. Please refer to the Quick Start section above.*

This repo uses UnityPy (instead of unitypack in upstream) to extract files.

-----

# Informations
For viewing Blue Archive Spines.

Have a look at [this branch](https://github.com/respectZ/blue-archive-spine/tree/resourceless) for resourceless.

# Requirements
- [decrunch](https://github.com/HearthSim/decrunch/)
- [fsb5](https://github.com/HearthSim/python-fsb5)
- [lz4](https://github.com/python-lz4/python-lz4)
- [Pillow](https://python-pillow.org/)
- [astc_decomp](https://github.com/K0lb3/astc_decomp/)
- MSVC++ 14.0 Build Tools with Windows 10 SDK

# Setup
## Building UnityPack
```
setup.py build
```
## Installing UnityPack
```
setup.py install
```
or
```
setup.py install --user
```

# Downloading Models
```
py/getModels.py
```
Downloaded Models located at ./downloaded_resource

Assets (Spine and Audio) located at ./assets

# Generating JSON Data
## data/audio.json
```
py/generateAudioJson.py
```
This will download VOC_JP audio instead of playing it directly (cors issue ?)

To play audio directly from BA's server, change py/generateModelsJson.py
```python
_type = 1
```
to
```python
_type = 0
```
## data/models.json
```
py/generateModelsJson.py
```
## And you're done!
Just launch index.html

## Used Libraries
- [pixi.js](https://pixijs.com/)
- [pixi-spine](https://github.com/pixijs/spine)
- [howler.js](https://howlerjs.com/)
- [UIKit](https://getuikit.com/)

Big Kudos for awesome [UnityPack](https://github.com/HearthSim/UnityPack)