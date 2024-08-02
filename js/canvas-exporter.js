// Main
function exportAnimation(FPS = 60) {
  let exportCanvas = document.createElement("canvas");
  exportCanvas.id = "export-canvas";
  exportCanvas.style.display = "none";
  document.body.appendChild(exportCanvas);
  let exportVideo = document.createElement("video");
  exportVideo.controls = true;
  exportVideo.id = "export-video";

  let appExport = new PIXI.Application({
    width: window.innerWidth,
    height: window.innerHeight,
    view: exportCanvas,
  });
  appExport.loader
    .add("char", `./${option.models.value}`)
    .load(function (loader, res) {
      let exportChar = new PIXI.spine.Spine(res.char.spineData);
      exportChar.scale.x = exportChar.scale.y = char.scale.x;
      exportChar.x = char.x;
      exportChar.y = char.y;
      exportChar.state.setAnimation(0, option.animations.value, 0);

      appExport.stage.addChild(exportChar);

      // Export Section
      let videoStream = exportCanvas.captureStream(FPS); //default to 60
      let mediaRecorder = new MediaRecorder(videoStream);

      let chunks = [];
      mediaRecorder.ondataavailable = function (e) {
        chunks.push(e.data);
      };

      mediaRecorder.onstop = function (e) {
        let blob = new Blob(chunks, { type: option.exportType.value });
        chunks = [];
        let videoURL = URL.createObjectURL(blob);
        exportVideo.src = videoURL;
      };
      mediaRecorder.ondataavailable = function (e) {
        chunks.push(e.data);
      };

      // Get Animation Length
      let animLength = 0;
      for (var i in char.spineData.animations) {
        if (char.spineData.animations[i].name == option.animations.value) {
          animLength = char.spineData.animations[i].duration;
          break;
        }
      }

      //Modal Popup
      document.getElementById("rendering").style.display = "block";
      document.getElementById("complete").style.display = "none";
      UIkit.modal(document.getElementById("modal-exporter")).show();
      // Progressbar
      document.getElementById("export-progress").value = 0;
      let progress = setInterval(function () {
        document.getElementById("export-progress").value += 1;
      }, animLength * 10);

      // Record
      mediaRecorder.start();
      setTimeout(function () {
        mediaRecorder.stop();
        //Free Resources
        appExport.stage.children.pop();
        appExport.loader.resources = {};
        exportCanvas.remove();
        clearInterval(progress);

        //Update modal
        document.getElementById("rendering").style.display = "none";
        document.getElementById("complete").style.display = "block";
        document.getElementById("result").appendChild(exportVideo);
      }, animLength * 1000);
    });
}

// char.state.setAnimation(0, "Idle_01", false);
// mediaRecorder.start();
// setTimeout(function (){ mediaRecorder.stop(); }, 4000);

function exportImage(exportAllModels, exportAllAnimations) {
    function renderModelAsImage(model, animation) {
        return loadCharPromise(model).then(() => {
            return playAnimationPromise(animation).then(() => {
            let canvas = app.renderer.extract.canvas(app.stage);
            let img = canvas.toDataURL("image/png");
            return img;
            });
        });
    }
    
    function loadCharPromise(model = "./assets/spine/shiroko_home/Shiroko_home.skel") {
        return new Promise((resolve, reject) => {
            isCharacterLoaded = false;
            if (app.stage.children.length > 0) {
            app.stage.children.pop();
            app.loader.resources = {};
            }
            if (audioList.length != 0) {
            for (var i in audioList) {
                audioList[i].stop();
            }
            audioList = [];
            }
        
            app.loader.resources = {};
            app.loader
            .add("char", `./${model}`)
            .load((loader, res) => {
                onAssetsLoaded(loader, res);
                resolve();
            })
            .on("error", (error) => {
                console.error(error);
                reject(error);
            });
        });
    }
    
    function playAnimationPromise(animation) {
        return new Promise((resolve, reject) => {
            try {
            playAnimation(animation);
            setTimeout(resolve, 2);
            } catch (error) {
            console.error("播放动画出错: ", error);
            reject(error);
            }
        });
    }
    
    function getModelFileName(filePath) {
        const parts = filePath.split("/");
        return parts[parts.length - 1].split(".")[0];
    }
    
    let zip = new JSZip();
    let models = exportAllModels
    ? [...option.models].map((o) => o.value)
    : [option.models.value]; // Export only the current model by default
    
    let chain = Promise.resolve();
    models.forEach(function (model, index) {
    chain = chain
        .then(() => loadCharPromise(model))
        .then(() => {
        if (exportAllAnimations) {
            let animations = char.spineData.animations.map((a) => a.name);
            console.log(`模型 ${model} 的动画列表：`, animations);
    
            let animationChain = Promise.resolve();
            animations.forEach(function (animation, aniIndex) {
            animationChain = animationChain
                .then(() => renderModelAsImage(model, animation))
                .catch((error) => {
                console.log(`读取模型动画失败 ${model} - ${animation}: `, error);
                })
                .then((img) => {
                if (img) {
                    zip.file(`${model}_animation_${aniIndex}.png`, img.split(",")[1], {
                    base64: true,
                    });
                }
                });
            });
            return animationChain;
        } else {
            return renderModelAsImage(model, char.spineData.animations[0].name)
            .catch((error) => {
                console.log(`读取模型初始状态失败 ${model}: `, error);
            })
            .then((img) => {
                if (img) {
                zip.file(`${model}.png`, img.split(",")[1], { base64: true });
                }
            });
        }
        })
        .catch((error) => {
            console.log(`读取模型失败 ${model}: `, error);
        });
    });
    
    chain.then(() => {
        zip.generateAsync({ type: "blob" }).then((content) => {
            var a = document.createElement("a");
            a.href = window.URL.createObjectURL(content);
            
            let baseFileName = exportAllModels ? "AllModels" : getModelFileName(option.models.value);
            
            if (exportAllAnimations) {
              baseFileName += "_Animation";
            }
            
            a.download = `${baseFileName}.zip`;
        
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
        });
    });
}
