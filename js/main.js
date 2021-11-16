let app;
let char;
let audioList = []
let audios;
let isCharacterLoaded = false;

function reCanvas() {
    audios = JSON.parse(httpGet("./data/audio.json"));
    app = new PIXI.Application(
        {
            width: window.innerWidth,
            height: window.innerHeight,
            view: document.getElementById("screen")
        }
    );
}

function loadChar(model="Shiroko_home/Shiroko_home.skel") {
    isCharacterLoaded = false;
    // remove previous spine
    if(app.stage.children.length > 0) {
        app.stage.children.pop();
        app.loader.resources = {};
    }
    // remove previous audio
    if(audioList.length != 0) {
        for(var i in audioList) {
            audioList[i].stop();
        }
        audioList = [];
    }

    // load new spine
    app.loader
        .add('char', `/blue-archive-spine/assets/${model}`)
        .load(onAssetsLoaded);
}

function onAssetsLoaded(loader,res) {
    if(audioList.length != 0) {
        for(var i in audioList) {
            audioList[i].stop();
        }
        audioList = [];
    }

    char = new PIXI.spine.Spine(res.char.spineData);

    // console.log(char)
    // console.log(char.spineData.height)
    // console.log(char.spineData.width)

    // Scaler
    char.scale.x = 0.5;
    char.scale.y = 0.5;

    // Centerize
    char.x = app.screen.width/2;
    char.y = app.screen.height/1;

    //Set option value
    option.scale.value = 0.5;
    option.x.value = char.x;
    option.y.value = char.y;

    // Insert animations to index.html
    const animations = res.char.spineData.animations;
    let check = 0;
    option.animations.innerHTML = "";
    for(var i in animations) {
        let a = document.createElement("option");
        a.value = a.innerHTML = animations[i].name;
        option.animations.append(a)
        if(animations[i].name == "Start_Idle_01")
            check = 1;
    }

    //Play Animation
    if(check) {
        char.state.setAnimation(0, "Start_Idle_01", option.loop.checked);
        optionAnimations.value = "Start_Idle_01";
    } else {
        char.state.setAnimation(0, animations[0].name, option.loop.checked);
    }
    app.stage.addChild(char);
    isCharacterLoaded = true;
}

function playAnimation(name) {
    if(!isCharacterLoaded)
        return;
    // remove previous audio
    if(audioList.length != 0) {
        for(var i in audioList) {
            audioList[i].stop();
        }
        audioList = [];
    }
    if(name.indexOf("Talk") != -1) {
        //Play Audio
        let audioIndex = parseInt(name.split("Talk_")[1].split("_")[0]) //01 to 1
        let files = {}
        //Get sounds from events, fk up for falsename
        // for(var i in char.spineData.events) {
        //     if(char.spineData.events[i].audioPath == null)
        //         continue;
        //     let parent = char.spineData.events[i].audioPath.split("/")[char.spineData.events[i].audioPath.split("/").length - 1].split("_")[0];
        //     let fname = char.spineData.events[i].audioPath.split("/")[char.spineData.events[i].audioPath.split("/").length - 1].split(".w")[0].replace(".ogg", "") + ".ogg"
        //     let audioIndex = parseInt(fname.split("MemorialLobby_")[1].split("_")[0])
        //     if(files[audioIndex] == undefined) {
        //         files[audioIndex] = [];
        //     }
        //     files[audioIndex].push(`./audio/JP_${parent}/${fname}`)
        // }
        // //Randomize
        // var audio = files[audioIndex][Math.floor(Math.random() * files[audioIndex].length)];
        // console.log(files)
        // //Play
        // var sound = new Howl({
        //     src: [audio],
        //     html5: true
        //   });
        // sound.once('load', function(){
        //     char.state.setAnimation(0, name, option.loop.checked);
        //     setTimeout(() => {
        //         sound.play();
        //     }, 400);
        //     audioList.push(sound);
        // });

        //Get sounds
        let charName = option.models.options[option.models.selectedIndex].text.replace("_home", "").toLowerCase().replace("_", "")
        let audioPool = audios[charName][audioIndex];
        //Play
        for(var i=0;i<audioPool.length;i++) {
            var sound = new Howl({
                src: [audioPool[i]]
              });
            audioList.push(sound);
        }
        for(var j=1;j<audioList.length;j++) {
            audioList[j-1].on('end', function() {
                audioList.splice(0, 1);
                setTimeout(() => {
                    audioList[0].play();
                }, 900);
            })
        }
        char.state.setAnimation(0, name, option.loop.checked);
        audioList[0].once('load', function() {
            setTimeout(() => {
                audioList[0].play();
            }, 387);
        });
    } else {
        char.state.setAnimation(0, name, option.loop.checked);
    }
}