let BASE_URL = "http://localhost:5000"

var lastInstructionShowed = 1

let instructions = [
    "Escolha uma imagem de fundo:",
    "Escolha a imagem que você deseja camuflar:",
    "Posicione-a sobre o fundo e quando estiver na posição correta, clique no botão abaixo:",
    "Aguarde um momento",
]

let extraHtml = [
    "<input id=\"background-input\" type=\"file\" onchange=\"didSelectBackground(this)\">",
    "<input id=\"overlay-input\" type=\"file\" onchange=\"didSelectOverlay(this)\">",
    "<input value=\"Camuflar\" type=\"submit\" onclick=\"didFinishEditing()\">",
    ""
]

var background = undefined
var overlay = undefined

function didSelectBackground(input) {
    
    var reader = new FileReader();
    
    reader.onload = function(e) {
        
        if (lastInstructionShowed < 2) {
            addInstruction(2);
        }
        
        background = e.target.result
        updateImages();
    }
    
    reader.readAsDataURL(input.files[0]);
    
}

function didSelectOverlay(input) {
    
    var reader = new FileReader();
    
    reader.onload = function(e) {
        
        if (lastInstructionShowed < 3) {
            addInstruction(3);
        }
        
        overlay = e.target.result
        updateImages();
        
    }
    
    reader.readAsDataURL(input.files[0]);
    
}

function didFinishEditing() {
    console.log("did finish");
    let konva = document.getElementsByClassName('konvajs-content')[0]
    let canvas = konva.children[0]
    
    removeAnchors();
    
    overlay = canvas.toDataURL();
    
    // document.getElementById('image').src = overlay
    
    // console.log("BACKGROUND: ", background.naturalWidth, background.naturalHeight);
    // console.log("OVERLAY: ", overlay.naturalWidth, overlay.naturalHeight);
    
    var backImg = new Image()
    var overImg = new Image()
    
    backImg.src = background
    overImg.src = overlay
    
    overImg.width = backImg.width
    overImg.height = backImg.height
    
    let url = BASE_URL + "/create"
    console.log(url);
    
    const formData = new FormData()

    formData.append('background', background)
    formData.append('overlay', overlay)

    fetch(url, {
      method: 'POST',
      body: formData,
    }).then(response => {
      console.log(response)
    })
    
    // postFiles(url, backImg, overImg, function(response) {
    //     console.log(response);
    //    // if (response != "erro") {
    //    //   getGraph(response);
    //    // } else {
    //    //
    //    //   alert(response)//"Algum erro ocorreu");
    //    // }
    //  })
}

function postFiles(url, bg, ov, callback) {
  var xhr = createCORSRequest('POST', url);
  
  if (!xhr) {
    throw new Error('CORS not supported');
  }
  
  xhr.setRequestHeader('Content-Type', 'application/json');
  
  xhr.onload = function() {
    let responseText = xhr.responseText;
    
    callback(responseText);
  }
  
  var data = {
    'background' : bg,
    'overlay' : ov
  }
  
  dataAsString = JSON.stringify(data)
  
  xhr.send(dataAsString);
}

function getImages() {
    let konva = document.getElementsByClassName('konvajs-content')[0]
    let canvas = konva.children[0]
    
    removeAnchors();
    
    overlay = canvas.toDataURL();
}

function updateImages() {
    
    if (lastInstructionShowed >= 3) {
        
        img = document.getElementById('image')
        img.src = background;
        
        img.onload = function() {
            showResize(overlay, img.width, img.height);
        }
        
    }
        
}

function addInstruction(index) {
    
    if (index < instructions.length) {
        
        var newElement = document.createElement('p');
        newElement.innerHTML = "<b>" + index + ". </b>" + instructions[index - 1] + extraHtml[index - 1];
        
        let instructionsDiv = document.getElementById('instructions-div')
        instructionsDiv.appendChild(newElement);
        
    }

    if (lastInstructionShowed < index) {
        lastInstructionShowed = index;
    }
    
}

window.onload = function () {
    addInstruction(1);
}

// ========================================================================
